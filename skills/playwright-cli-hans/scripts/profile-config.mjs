import { randomUUID } from "node:crypto";
import { mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { isAbsolute, join, parse, resolve } from "node:path";

const userHome = homedir();
const configDir = join(userHome, ".playwright-cli-hans");
const configFile = join(configDir, "edge.json");
const defaultProfile = ".playwright-cli-hans/edge-profile";
const defaultPort = 9222;

function readConfig() {
  try {
    return JSON.parse(readFileSync(configFile, "utf8"));
  } catch (error) {
    if (error.code === "ENOENT")
      return undefined;
    if (error instanceof SyntaxError)
      throw new Error(`Invalid JSON in ${configFile}`, { cause: error });
    throw error;
  }
}

function resolveConfig(config) {
  if (typeof config?.profileDir !== "string" || !config.profileDir.trim() || config.profileDir.includes("\0"))
    throw new Error("Choose a directory for the dedicated Edge profile.");

  const profilePath = config.profileDir.replace(/^~(?:[\\/]+|$)/, "");
  if (parse(profilePath).root && !isAbsolute(profilePath))
    throw new Error("Use an absolute path or a path relative to your home directory.");

  const profileDir = resolve(userHome, profilePath);
  if (profileDir === userHome || profileDir === parse(profileDir).root)
    throw new Error("Choose a dedicated Edge subdirectory.");

  const cdpPort = config.cdpPort ?? defaultPort;
  if (!Number.isInteger(cdpPort) || cdpPort < 1 || cdpPort > 65535)
    throw new Error("Choose a CDP port from 1 to 65535.");

  return { profileDir, cdpPort, cdpEndpoint: `http://127.0.0.1:${cdpPort}` };
}

function saveConfig(config) {
  mkdirSync(configDir, { recursive: true, mode: 0o700 });
  const temporaryFile = join(configDir, `edge-${randomUUID()}.tmp`);
  try {
    writeFileSync(temporaryFile, JSON.stringify(config, null, 2) + "\n", { flag: "wx", mode: 0o600 });
    renameSync(temporaryFile, configFile);
  } finally {
    rmSync(temporaryFile, { force: true });
  }
}

const [command, profileInput, portInput, ...extra] = process.argv.slice(2);
try {
  const validCommand = command === "get" || command === "setup";
  if (!validCommand || extra.length || (command === "get" && profileInput !== undefined))
    throw new Error("Use profile-config.mjs get or profile-config.mjs setup [directory] [port].");

  const current = readConfig();
  if (command === "setup") {
    const settings = {
      profileDir: profileInput ?? current?.profileDir ?? defaultProfile,
      cdpPort: portInput === undefined ? current?.cdpPort ?? defaultPort : Number(portInput),
    };
    const resolved = resolveConfig(settings);
    saveConfig(settings);
    console.log(JSON.stringify(resolved));
  } else if (current === undefined) {
    console.error(`Choose an Edge profile directory with setup. Settings will be stored in ${configFile}.`);
    process.exitCode = 2;
  } else {
    console.log(JSON.stringify(resolveConfig(current)));
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
