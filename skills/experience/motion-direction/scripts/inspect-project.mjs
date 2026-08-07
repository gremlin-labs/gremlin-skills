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

async function visibleDirectories(path) {
  if (!await exists(path)) return [];
  const entries = await readdir(path, { withFileTypes: true });
  return entries.filter((entry) => entry.isDirectory() && !entry.name.startsWith('.')).map((entry) => entry.name).sort();
}

function exportSpecifiers(exportsField) {
  if (!exportsField) return [];
  if (typeof exportsField === 'string' || Array.isArray(exportsField)) return ['turbulencejs'];
  return Object.keys(exportsField)
    .filter((key) => key === '.' || key.startsWith('./'))
    .map((key) => key === '.' ? 'turbulencejs' : `turbulencejs/${key.slice(2)}`)
    .sort();
}

const manifestPath = resolve(root, 'package.json');
if (!await exists(manifestPath)) {
  console.error(`No package.json found at ${manifestPath}`);
  process.exitCode = 1;
} else {
  const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
  const dependencies = { ...manifest.dependencies, ...manifest.devDependencies, ...manifest.peerDependencies };
  const frameworks = ['next', 'react', 'vue', 'svelte', '@angular/core', 'solid-js'].filter((name) => name in dependencies);
  const motionDependencies = [
    'turbulencejs', 'framer-motion', 'motion', 'gsap', 'animejs', '@react-spring/web',
    'react-spring', '@motionone/dom', 'lottie-web', '@lottiefiles/dotlottie-react',
  ].filter((name) => name in dependencies).map((name) => ({ name, version: dependencies[name] }));
  const packageManager = await exists(resolve(root, 'pnpm-lock.yaml')) ? 'pnpm'
    : await exists(resolve(root, 'yarn.lock')) ? 'yarn'
      : await exists(resolve(root, 'bun.lockb')) || await exists(resolve(root, 'bun.lock')) ? 'bun'
        : await exists(resolve(root, 'package-lock.json')) ? 'npm'
          : manifest.packageManager?.split('@')[0] ?? 'unknown';
  const electron = 'electron' in dependencies || 'electron-vite' in dependencies;
  const turbulenceManifestPath = resolve(root, 'node_modules', 'turbulencejs', 'package.json');
  let installedTurbulenceManifest = null;
  if (await exists(turbulenceManifestPath)) {
    installedTurbulenceManifest = JSON.parse(await readFile(turbulenceManifestPath, 'utf8'));
  }
  const sourceDirectories = [];
  for (const candidate of ['app', 'src', 'pages', 'components', 'renderer', 'main']) {
    if (await exists(resolve(root, candidate))) sourceDirectories.push(candidate);
  }
  const documentationDirectories = [];
  for (const candidate of ['docs', 'design', 'agent-work']) {
    if (await exists(resolve(root, candidate))) documentationDirectories.push(candidate);
  }

  console.log(JSON.stringify({
    root,
    name: manifest.name ?? basename(root),
    private: manifest.private === true,
    packageManager,
    moduleType: manifest.type ?? 'commonjs',
    typescript: 'typescript' in dependencies || await exists(resolve(root, 'tsconfig.json')),
    frameworks,
    electron,
    turbulenceVersion: dependencies.turbulencejs ?? null,
    installedTurbulenceVersion: installedTurbulenceManifest?.version ?? null,
    installedTurbulencePublicExports: exportSpecifiers(installedTurbulenceManifest?.exports),
    motionDependencies,
    scripts: Object.keys(manifest.scripts ?? {}).sort(),
    sourceDirectories,
    documentationDirectories,
    topLevelDirectories: await visibleDirectories(root),
    publicTurbulenceCandidates: [
      'turbulencejs', 'turbulencejs/runtime', 'turbulencejs/dom',
      ...(electron ? ['turbulencejs/main'] : []),
      'turbulencejs/subtle', 'turbulencejs/interact', 'turbulencejs/cartoon',
      'turbulencejs/cinematic', 'turbulencejs/extreme', 'turbulencejs/effects',
      'turbulencejs/surfaces', 'turbulencejs/surface-worker',
    ],
  }, null, 2));
}
