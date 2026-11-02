import os
import re
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def check_ffmpeg() -> str:
    """Check if ffmpeg is available in system PATH or common locations."""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # Common locations on macOS / Linux
    for fallback in ["/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg", "/usr/bin/ffmpeg"]:
        if os.path.exists(fallback) and os.access(fallback, os.X_OK):
            return fallback
            
    raise FileNotFoundError(
        "FFmpeg is required but not found in PATH or standard locations.\n"
        "Please install it via Homebrew (`brew install ffmpeg`) or package manager."
    )


def extract_audio(video_path: str, temp_dir: str) -> str:
    """
    Extracts audio from video file to a 16kHz mono WAV file using ffmpeg.
    16kHz mono WAV is the native format for Whisper, requiring zero resample during inference.
    """
    ffmpeg_bin = check_ffmpeg()
    video_path = os.path.abspath(video_path)
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Input video file not found: {video_path}")

    stem = Path(video_path).stem
    out_audio = os.path.join(temp_dir, f"{stem}_audio_16k.wav")

    cmd = [
        ffmpeg_bin,
        "-y",
        "-i", video_path,
        "-vn",               # Disable video recording
        "-acodec", "pcm_s16le", # Uncompressed 16-bit PCM WAV
        "-ar", "16000",      # 16kHz sample rate
        "-ac", "1",          # Mono channel
        out_audio
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg audio extraction failed:\n{result.stderr}")

    return out_audio


def get_media_duration(file_path: str) -> float:
    """Retrieve duration of media file in seconds using ffprobe."""
    ffprobe_bin = shutil.which("ffprobe") or "/usr/local/bin/ffprobe" or "/opt/homebrew/bin/ffprobe"
    if not os.path.exists(ffprobe_bin):
        return 0.0

    cmd = [
        ffprobe_bin,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return float(res.stdout.strip())
    except Exception:
        pass
    return 0.0


def format_seconds(seconds: float) -> str:
    """Convert seconds to mm:ss format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def load_vocabulary(vocab_path: str = None) -> dict:
    """Load vocabulary replacement dictionary from json."""
    if not vocab_path or not os.path.isfile(vocab_path):
        # Fallback to default vocabulary in config
        default_config = Path(__file__).resolve().parent.parent / "config" / "vocabulary.json"
        if default_config.is_file():
            vocab_path = str(default_config)
        else:
            return {}

    try:
        with open(vocab_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Warning: Failed to load vocabulary config: {e}")
        return {}


try:
    from opencc import OpenCC
    _t2s_converter = OpenCC("t2s")
except ImportError:
    _t2s_converter = None


def to_simplified_chinese(text: str) -> str:
    """Convert traditional Chinese characters to simplified Chinese."""
    if _t2s_converter and text:
        return _t2s_converter.convert(text)
    return text


def apply_corrections(text: str, vocabulary: dict, language: str = "zh") -> str:
    """Apply vocabulary corrections to transcribed text."""
    if not text:
        return text

    if language == "zh":
        text = to_simplified_chinese(text)

    if vocabulary:
        # Iterate through target word -> list of homophones / typos
        for correct_term, aliases in vocabulary.items():
            if isinstance(aliases, list):
                for alias in aliases:
                    # Use case-insensitive substitution
                    text = re.sub(re.escape(alias), correct_term, text, flags=re.IGNORECASE)
            elif isinstance(aliases, str):
                text = re.sub(re.escape(aliases), correct_term, text, flags=re.IGNORECASE)

    # Basic whitespace cleanup
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_markdown(
    video_path: str,
    segments: list,
    duration_sec: float,
    model_name: str,
    vocabulary: dict,
    language: str = "zh"
) -> str:
    """
    Format transcribed segments into a clean, human-readable Markdown file.
    Groups close utterances into coherent paragraphs.
    """
    video_file = os.path.basename(video_path)
    duration_str = format_seconds(duration_sec)
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    doc = []
    doc.append(f"# 视频文字转写记录：{video_file}\n")
    doc.append(f"> **媒体文件**：`{video_file}`  ")
    doc.append(f"> **视频时长**：{duration_str}（{int(duration_sec)} 秒）  ")
    doc.append(f"> **转写时间**：{today_str}  ")
    doc.append(f"> **识别引擎**：Faster-Whisper (`{model_name}`) + INT8 加速  \n")
    doc.append("---\n")

    if not segments:
        doc.append("*（未检测到有效语音内容）*\n")
        return "\n".join(doc)

    for seg in segments:
        cleaned_text = apply_corrections(seg["text"], vocabulary, language=language)
        if not cleaned_text:
            continue
        start_fmt = format_seconds(seg["start"])
        end_fmt = format_seconds(seg["end"])
        doc.append(f"- **`[{start_fmt} - {end_fmt}]`**：{cleaned_text}")

    return "\n".join(doc)
