#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(repoRoot, relative), "utf8"));
const errors = [];

const packageJson = readJson("package.json");
const version = packageJson.version;
if (!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(version)) {
  errors.push(`package.json version is not semantic: ${version}`);
}
if (packageJson.license !== "MIT") {
  errors.push("package.json license must be MIT");
}

const lockPath = path.join(repoRoot, "package-lock.json");
if (!fs.existsSync(lockPath)) {
  errors.push("package-lock.json is missing");
} else {
  const lock = readJson("package-lock.json");
  if (lock.version !== version || lock.packages?.[""]?.version !== version) {
    errors.push("package-lock.json root version does not match package.json");
  }
}

const changelog = fs.readFileSync(path.join(repoRoot, "CHANGELOG.md"), "utf8");
if (!changelog.includes(`## ${version} —`)) {
  errors.push(`CHANGELOG.md has no ${version} release-candidate entry`);
}

const generated = [
  ["dist/claude-code-skills/manifest.json", "packageVersion"],
  ["dist/plugins/manifest.json", "version"],
  ["dist/plugins/codex/gremlin-skills/.codex-plugin/plugin.json", "version"],
  ["dist/plugins/claude/gremlin-skills/.claude-plugin/plugin.json", "version"],
];
for (const [relative, field] of generated) {
  const absolute = path.join(repoRoot, relative);
  if (!fs.existsSync(absolute)) {
    errors.push(`${relative} is missing; build release artifacts before checking versions`);
    continue;
  }
  const value = readJson(relative)[field];
  if (value !== version) {
    errors.push(`${relative} ${field} ${value} does not match ${version}`);
  }
}

if (errors.length) {
  for (const error of errors) console.error(`ERROR: ${error}`);
  process.exit(1);
}
console.log(`Validated package, archive, plugin, lockfile, and changelog version ${version}.`);
