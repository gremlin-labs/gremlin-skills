#!/usr/bin/env node

import { readFile } from 'node:fs/promises';
import { extname, resolve } from 'node:path';

const path = resolve(process.argv[2] ?? '');
if (!process.argv[2]) {
  console.error('Usage: validate-deck.mjs <deck.json>');
  process.exitCode = 1;
} else if (extname(path).toLowerCase() !== '.json') {
  console.error('Deck validation accepts declarative JSON only; executable JavaScript modules are refused.');
  process.exitCode = 1;
} else {
  try {
    const deck = JSON.parse(await readFile(path, 'utf8'));
    const slides = deck.slides;
    const roles = deck.layoutRoles;
    if (!Array.isArray(slides) || slides.length === 0) throw new Error('Deck must contain a non-empty slides array.');
    if (!roles || typeof roles !== 'object' || Array.isArray(roles)) throw new Error('Deck must contain layoutRoles.');
    const failures = [];
    const ids = new Set();
    for (const [index, slide] of slides.entries()) {
      const label = slide.id || `slide ${index + 1}`;
      if (!slide.id || ids.has(slide.id)) failures.push(`${label}: id must be present and unique.`);
      ids.add(slide.id);
      if (typeof slide.claim !== 'string' || !slide.claim.trim()) failures.push(`${label}: one semantic claim is required.`);
      if (typeof slide.title !== 'string' || !slide.title.trim()) failures.push(`${label}: selectable title text is required.`);
      if (!roles[slide.layout]) failures.push(`${label}: unknown layout role ${slide.layout}.`);
      if (!roles[slide.layout]?.landscape || !roles[slide.layout]?.portrait) failures.push(`${label}: layout role needs landscape and portrait recipes.`);
      if (!slide.motion) failures.push(`${label}: a semantic motion role is required.`);
      if (!Number.isInteger(slide.intensity) || slide.intensity < 0 || slide.intensity > 4) failures.push(`${label}: intensity must be an integer from 0 through 4.`);
      if (!slide.contentBudget || !Number.isFinite(slide.contentBudget.minBodyPx)) failures.push(`${label}: measurable contentBudget.minBodyPx is required.`);
      if (!Array.isArray(slide.assets)) failures.push(`${label}: assets must be an array, even when empty.`);
      if (!Array.isArray(slide.sources)) failures.push(`${label}: sources must be an array, even when empty.`);
      for (const asset of slide.assets ?? []) if (!asset.path || !asset.provenance || !asset.focalPoint) failures.push(`${label}: every asset needs path, provenance, and focalPoint.`);
    }
    if (failures.length) throw new Error(`Deck validation failed:\n- ${[...new Set(failures)].join('\n- ')}`);
    console.log(`Presentation deck verified: ${slides.length} semantic slides, ${Object.keys(roles).length} dual-aspect layout roles, unique IDs, content budgets, provenance arrays, and intensity bounds.`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
