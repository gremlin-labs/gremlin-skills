#!/usr/bin/env node
import { access, readFile, readdir } from 'node:fs/promises';
import { basename, resolve } from 'node:path';

const root = resolve(process.argv[2] ?? process.cwd());

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

async function fileNames(directory) {
  if (!await exists(directory)) return [];
  return (await readdir(directory, { withFileTypes: true })).filter(entry => entry.isFile()).map(entry => entry.name).sort();
}

const manifestPath = resolve(root, 'package.json');
if (!await exists(manifestPath)) {
  console.error(`No package.json found at ${manifestPath}`);
  process.exitCode = 1;
} else {
  const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
  const dependencies = { ...manifest.dependencies, ...manifest.devDependencies, ...manifest.peerDependencies };
  const packageManager = await exists(resolve(root, 'pnpm-lock.yaml')) ? 'pnpm'
    : await exists(resolve(root, 'yarn.lock')) ? 'yarn'
      : await exists(resolve(root, 'bun.lockb')) || await exists(resolve(root, 'bun.lock')) ? 'bun'
        : await exists(resolve(root, 'package-lock.json')) ? 'npm'
          : manifest.packageManager?.split('@')[0] ?? 'unknown';
  const sourceDirectories = [];
  for (const candidate of ['src', 'app', 'pages', 'slides', 'presentation']) {
    if (await exists(resolve(root, candidate))) sourceDirectories.push(candidate);
  }
  const styleDirectory = resolve(root, '.turbulencejs/presentation-styles');
  const styleFiles = (await fileNames(styleDirectory)).filter(name => name.endsWith('.json'));
  const scripts = Object.keys(manifest.scripts ?? {}).sort();
  const frameworks = ['vite', 'next', 'react', 'vue', 'svelte', '@angular/core', 'astro', 'electron'].filter(name => name in dependencies);

  console.log(JSON.stringify({
    root,
    name: manifest.name ?? basename(root),
    private: manifest.private === true,
    packageManager,
    moduleType: manifest.type ?? 'commonjs',
    frameworks,
    turbulenceVersion: dependencies.turbulencejs ?? (manifest.name === 'turbulencejs' ? manifest.version ?? 'workspace' : null),
    scripts,
    relevantScripts: scripts.filter(name => /(?:test|build|lint|type|present|slide|playwright)/iu.test(name)),
    sourceDirectories,
    customStyleDirectory: styleDirectory,
    customStyleFiles: styleFiles,
    candidateEntrypoints: ['turbulencejs', 'turbulencejs/subtle', 'turbulencejs/cinematic']
  }, null, 2));
}
