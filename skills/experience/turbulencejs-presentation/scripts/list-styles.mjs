#!/usr/bin/env node
import { resolve } from 'node:path';
import { discoverStyles } from './style-utils.mjs';

function valueAfter(flag) {
  const index = process.argv.indexOf(flag);
  return index === -1 ? null : process.argv[index + 1];
}

const project = valueAfter('--project');
const json = process.argv.includes('--json');

try {
  const result = await discoverStyles(project ? resolve(project) : null);
  const menu = result.styles.map(style => ({
    id: style.id,
    name: style.name,
    bestFor: style.bestFor,
    communicationTraits: style.communicationTraits,
    mood: style.mood,
    intensityRange: style.motion.intensityRange,
    source: style.source,
    path: style.path
  }));
  if (json) {
    console.log(JSON.stringify({ styles: menu, projectLocalDirectory: result.localDirectory, precedence: 'project-local-over-built-in' }, null, 2));
  } else {
    for (const style of menu) console.log(`${style.id} [${style.source}] — ${style.communicationTraits.join(', ')}; intensity ${style.intensityRange.join('–')}; best for ${style.bestFor.join(', ')}`);
    console.log(`${menu.length} presentation styles discovered. Project-local files override built-ins with the same id.`);
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
