#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { discoverStyles, styleRoot } from './style-utils.mjs';

function valueAfter(flag) {
  const index = process.argv.indexOf(flag);
  return index === -1 ? null : process.argv[index + 1];
}

try {
  const schema = JSON.parse(await readFile(resolve(styleRoot, 'style.schema.json'), 'utf8'));
  if (schema.$schema !== 'https://json-schema.org/draft/2020-12/schema' || !schema.properties || !Array.isArray(schema.required)) throw new Error('style.schema.json is not a usable draft 2020-12 schema.');
  const project = valueAfter('--project');
  const { builtIns, locals, styles } = await discoverStyles(project ? resolve(project) : null);
  if (builtIns.length === 0) throw new Error('No built-in presentation styles were found.');
  console.log(`Presentation styles verified: ${builtIns.length} built-in, ${locals.length} project-local, ${styles.length} active after precedence.`);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
