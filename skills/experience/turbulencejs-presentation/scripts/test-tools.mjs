#!/usr/bin/env node

import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const validator = new URL('./validate-deck.mjs', import.meta.url);

function run(path) {
  return spawnSync(process.execPath, [validator.pathname, path], { encoding: 'utf8' });
}

function validDeck() {
  return {
    layoutRoles: {
      proof: { landscape: 'claim left', portrait: 'claim top' },
    },
    slides: [{
      id: 'proof-1',
      claim: 'The package is independently installable.',
      title: 'Portable proof',
      layout: 'proof',
      motion: 'explain',
      intensity: 1,
      contentBudget: { minBodyPx: 24 },
      assets: [],
      sources: [],
    }],
  };
}

test('validates a declarative JSON deck', async () => {
  const root = await mkdtemp(join(tmpdir(), 'gremlin-deck-'));
  const deck = join(root, 'deck.json');
  await writeFile(deck, `${JSON.stringify(validDeck())}\n`);
  const result = run(deck);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Presentation deck verified/);
});

test('rejects executable modules without importing them', async () => {
  const root = await mkdtemp(join(tmpdir(), 'gremlin-deck-'));
  const marker = join(root, 'executed.txt');
  const deck = join(root, 'deck.mjs');
  await writeFile(deck, `import { writeFileSync } from 'node:fs';\nwriteFileSync(${JSON.stringify(marker)}, 'executed');\nexport default ${JSON.stringify(validDeck())};\n`);
  const result = run(deck);
  assert.notEqual(result.status, 0);
  await assert.rejects(readFile(marker), /ENOENT/);
  assert.match(result.stderr, /JSON/i);
});
