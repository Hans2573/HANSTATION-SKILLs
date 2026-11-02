#!/usr/bin/env python3
"""
Video Transcription CLI
Extracts audio from video files and transcribes speech to structured Markdown with timestamps using Faster-Whisper.
"""

import os
import sys
import time
import shutil
import argparse
import tempfile
import subprocess
from pathlib import Path

# Ensure package modules can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import (
    check_ffmpeg,
    extract_audio,
    get_media_duration,
    format_seconds,
    load_vocabulary,
    build_markdown,
)


def resolve_model(model_name: str) -> str:
    """
    Resolves model path.
    1. Returns directly if model_name is an existing directory with model.bin.
    2. Checks ~/.cache/whisper-models/{model_name}. If present, returns it.
    3. If not present and curl is available, downloads seamlessly via hf-mirror.com into cache.
    4. Otherwise falls back to model_name string for faster-whisper default resolution.
    """
    if os.path.isdir(model_name) and os.path.exists(os.path.join(model_name, "model.bin")):
        return model_name

    cache_dir = os.path.expanduser(f"~/.cache/whisper-models/{model_name}")
    model_bin = os.path.join(cache_dir, "model.bin")
    if os.path.isfile(model_bin) and os.path.getsize(model_bin) > 1024 * 1024:
        return cache_dir

    # Known standard faster-whisper model sizes
    known_models = ["tiny", "base", "small", "medium", "large-v3"]
    if model_name in known_models and shutil.which("curl"):
        print(f"📥 正在快速下载/同步 Whisper 模型 `{model_name}` 到本地缓存...")
        os.makedirs(cache_dir, exist_ok=True)
        files = ["config.json", "tokenizer.json", "vocabulary.txt", "model.bin"]
        repo = f"Systran/faster-whisper-{model_name}"
        all_ok = True
        for f in files:
            target = os.path.join(cache_dir, f)
            if not os.path.exists(target) or os.path.getsize(target) == 0:
                url = f"https://hf-mirror.com/{repo}/resolve/main/{f}"
                print(f"   ⬇️ 下载 {f}...")
                res = subprocess.run(["curl", "-s", "-L", "-o", target, url])
                if res.returncode != 0:
                    all_ok = False
                    break
        if all_ok and os.path.isfile(model_bin) and os.path.getsize(model_bin) > 1024 * 1024:
            print(f"✅ 模型 `{model_name}` 下载完成并就绪。")
            return cache_dir

    return model_name


def parse_args():
    parser = argparse.ArgumentParser(
        description="从视频/音频中完整提取语音文字并输出带时间戳的 Markdown 文档"
    )
    parser.add_argument("input", help="输入视频或音频文件路径 (mp4, mov, mkv, webm, mp3, wav 等)")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="输出 Markdown 文件路径 (默认: 视频同级目录下的 {文件名}_transcript.md)"
    )
    parser.add_argument(
        "-m", "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper 模型规格 (默认: base，兼顾速度与准确度；可选 tiny, base, small, medium)"
    )
    parser.add_argument(
        "-l", "--language",
        default="zh",
        help="识别目标语言 (默认: zh 中文)"
    )
    parser.add_argument(
        "-v", "--vocab",
        default=None,
        help="专有名词/同音字校准词表 json 文件路径"
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=8,
        help="CPU 推理线程数 (默认: 8)"
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda", "auto"],
        help="推理设备 (默认: cpu)"
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        choices=["int8", "float16", "float32"],
        help="计算精度量化 (默认: int8)"
    )
    parser.add_argument(
        "--no-mirror",
        action="store_true",
        help="禁用国内 HF 镜像 (默认启用 https://hf-mirror.com)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # 1. Setup mirror environment if enabled
    if not args.no_mirror and "HF_ENDPOINT" not in os.environ:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"❌ 错误: 输入文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    # 2. Check ffmpeg
    try:
        ffmpeg_bin = check_ffmpeg()
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Determine output path
    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        stem = Path(input_path).stem
        parent = Path(input_path).parent
        output_path = os.path.join(parent, f"{stem}_transcript.md")

    # Create parent directory for output if not exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 4. Check media duration
    duration = get_media_duration(input_path)
    print(f"🎬 输入媒体: {input_path}")
    print(f"⏱️ 媒体时长: {format_seconds(duration)} ({int(duration)}s)")
    print(f"🤖 识别模型: faster-whisper ({args.model}, {args.compute_type}, {args.threads} threads)")

    t_start = time.time()

    # 5. Extract audio into temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print("🔊 [1/3] 正在提取 16kHz 单声道无损音频...")
        try:
            audio_path = extract_audio(input_path, temp_dir)
        except Exception as e:
            print(f"❌ 音频提取失败: {e}", file=sys.stderr)
            sys.exit(1)

        # 6. Load Faster-Whisper Model
        print(f"⏳ [2/3] 正在载入 Whisper 模型 `{args.model}`...")
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            print(
                "❌ 错误: 未安装 faster-whisper 库。\n"
                "请使用 uv 或 pip 安装: pip install faster-whisper",
                file=sys.stderr
            )
            sys.exit(1)

        t_load = time.time()
        model_target = resolve_model(args.model)
        model = WhisperModel(
            model_target,
            device=args.device,
            compute_type=args.compute_type,
            cpu_threads=args.threads
        )
        print(f"✅ 模型就绪 (耗时: {time.time() - t_load:.1f}s)")

        # 7. Transcribe
        print("📝 [3/3] 正在进行语音识别并对齐时序断句...")
        segments_data = []
        transcribe_kwargs = {
            "language": args.language,
            "beam_size": 5,
            "vad_filter": True,
            "vad_parameters": dict(min_silence_duration_ms=400)
        }
        if args.language == "zh":
            transcribe_kwargs["initial_prompt"] = "以下是普通话的句子，以简体中文输出。"

        seg_iter, info = model.transcribe(audio_path, **transcribe_kwargs)

        for s in seg_iter:
            raw_text = s.text.strip()
            from utils import to_simplified_chinese
            display_text = to_simplified_chinese(raw_text) if args.language == "zh" else raw_text
            segments_data.append({
                "start": s.start,
                "end": s.end,
                "text": display_text
            })
            # Real-time console progress
            print(f"  [{format_seconds(s.start)} -> {format_seconds(s.end)}] {display_text}")

        # 8. Post-processing and Markdown formatting
        vocab = load_vocabulary(args.vocab)
        markdown_content = build_markdown(
            video_path=input_path,
            segments=segments_data,
            duration_sec=duration,
            model_name=args.model,
            vocabulary=vocab,
            language=args.language
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

    total_time = time.time() - t_start
    print("-" * 50)
    print(f"🎉 转写完成！总耗时: {total_time:.1f} 秒")
    print(f"📄 输出文件: {output_path}")


if __name__ == "__main__":
    main()
