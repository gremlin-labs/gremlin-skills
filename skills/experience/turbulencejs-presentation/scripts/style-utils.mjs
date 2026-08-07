import { access, readFile, readdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const styleRoot = fileURLToPath(new URL('../styles/', import.meta.url));
const topLevelKeys = ['id', 'name', 'bestFor', 'communicationTraits', 'mood', 'designSoul', 'narrative', 'visual', 'motion', 'aspects', 'guardrails'];
const entrypoints = new Set(['turbulencejs', 'turbulencejs/subtle', 'turbulencejs/cinematic', 'turbulencejs/cartoon', 'turbulencejs/effects', 'turbulencejs/surfaces']);

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

function nonEmptyStrings(value, minimum = 1) {
  return Array.isArray(value) && value.length >= minimum && value.every(item => typeof item === 'string' && item.trim().length > 0);
}

function requiredObject(value, keys) {
  return value && typeof value === 'object' && !Array.isArray(value) && keys.every(key => key in value);
}

export function validateStyle(style, label = style?.id ?? 'unknown') {
  const failures = [];
  if (!style || typeof style !== 'object' || Array.isArray(style)) return [`${label}: style must be an object.`];
  for (const key of topLevelKeys) if (!(key in style)) failures.push(`${label}: missing ${key}.`);
  for (const key of Object.keys(style)) if (!topLevelKeys.includes(key)) failures.push(`${label}: unsupported top-level key ${key}.`);
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/u.test(style.id ?? '')) failures.push(`${label}: id must be kebab-case.`);
  if (typeof style.name !== 'string' || !style.name.trim()) failures.push(`${label}: name must be non-empty.`);
  if (!nonEmptyStrings(style.bestFor)) failures.push(`${label}: bestFor must contain at least one string.`);
  if (!nonEmptyStrings(style.communicationTraits, 2)) failures.push(`${label}: communicationTraits must contain at least two strings.`);
  if (!nonEmptyStrings(style.mood, 2)) failures.push(`${label}: mood must contain at least two strings.`);
  if (typeof style.designSoul !== 'string' || style.designSoul.length < 16) failures.push(`${label}: designSoul is too short.`);

  if (!requiredObject(style.narrative, ['suggestedSlideRange', 'densityCurve', 'arc'])) {
    failures.push(`${label}: narrative is incomplete.`);
  } else {
    const range = style.narrative.suggestedSlideRange;
    if (!Array.isArray(range) || range.length !== 2 || range.some(value => !Number.isInteger(value) || value < 1) || range[0] > range[1]) failures.push(`${label}: suggestedSlideRange must be two ordered positive integers.`);
    if (!nonEmptyStrings(style.narrative.densityCurve, 3)) failures.push(`${label}: densityCurve must contain at least three strings.`);
    if (!nonEmptyStrings(style.narrative.arc, 3)) failures.push(`${label}: arc must contain at least three strings.`);
  }

  if (!requiredObject(style.visual, ['paletteRoles', 'typography', 'layoutAffinities', 'decorationDNA', 'assetTreatment', 'codeTreatment'])) {
    failures.push(`${label}: visual is incomplete.`);
  } else {
    if (!style.visual.paletteRoles || Object.keys(style.visual.paletteRoles).length < 5 || !Object.values(style.visual.paletteRoles).every(value => typeof value === 'string' && value.trim())) failures.push(`${label}: paletteRoles must contain at least five named string roles.`);
    if (!nonEmptyStrings(style.visual.typography, 3)) failures.push(`${label}: typography must contain at least three rules.`);
    for (const key of ['layoutAffinities', 'decorationDNA', 'assetTreatment', 'codeTreatment']) if (!nonEmptyStrings(style.visual[key])) failures.push(`${label}: visual.${key} must contain strings.`);
  }

  if (!requiredObject(style.motion, ['preferredEntrypoints', 'intensityRange', 'signatureMove', 'forbiddenMotion', 'interruption', 'cleanup', 'reducedEndpoint'])) {
    failures.push(`${label}: motion is incomplete.`);
  } else {
    if (!nonEmptyStrings(style.motion.preferredEntrypoints) || style.motion.preferredEntrypoints.some(value => !entrypoints.has(value))) failures.push(`${label}: preferredEntrypoints contains an unknown public entrypoint.`);
    const range = style.motion.intensityRange;
    if (!Array.isArray(range) || range.length !== 2 || range.some(value => !Number.isInteger(value) || value < 0 || value > 4) || range[0] > range[1]) failures.push(`${label}: intensityRange must be two ordered integers from 0 through 4.`);
    for (const key of ['signatureMove', 'interruption', 'cleanup', 'reducedEndpoint']) if (typeof style.motion[key] !== 'string' || !style.motion[key].trim()) failures.push(`${label}: motion.${key} must be non-empty.`);
    if (!nonEmptyStrings(style.motion.forbiddenMotion)) failures.push(`${label}: forbiddenMotion must contain strings.`);
  }

  if (!requiredObject(style.aspects, ['landscape', 'portrait', 'stacking', 'safeAreas', 'focalPoint', 'prohibitedBehavior'])) {
    failures.push(`${label}: aspects is incomplete.`);
  } else {
    for (const key of ['landscape', 'portrait', 'stacking', 'focalPoint']) if (!nonEmptyStrings(style.aspects[key])) failures.push(`${label}: aspects.${key} must contain strings.`);
    if (!requiredObject(style.aspects.safeAreas, ['landscape', 'portrait'])) failures.push(`${label}: safeAreas must name landscape and portrait rules.`);
    if (!nonEmptyStrings(style.aspects.prohibitedBehavior, 2)) failures.push(`${label}: prohibitedBehavior must contain at least two rules.`);
  }

  if (!requiredObject(style.guardrails, ['required', 'forbidden', 'qa'])) {
    failures.push(`${label}: guardrails are incomplete.`);
  } else {
    for (const key of ['required', 'forbidden', 'qa']) if (!nonEmptyStrings(style.guardrails[key])) failures.push(`${label}: guardrails.${key} must contain strings.`);
  }
  return failures;
}

export async function loadStyleDirectory(directory, source) {
  if (!await exists(directory)) return [];
  const entries = (await readdir(directory, { withFileTypes: true }))
    .filter(entry => entry.isFile() && entry.name.endsWith('.json') && entry.name !== 'style.schema.json')
    .sort((a, b) => a.name.localeCompare(b.name));
  const styles = [];
  const ids = new Set();
  for (const entry of entries) {
    const path = resolve(directory, entry.name);
    let style;
    try {
      style = JSON.parse(await readFile(path, 'utf8'));
    } catch (error) {
      throw new Error(`${path}: invalid JSON: ${error.message}`);
    }
    const failures = validateStyle(style, path);
    if (failures.length) throw new Error(failures.join('\n'));
    if (ids.has(style.id)) throw new Error(`${directory}: duplicate style id ${style.id}.`);
    ids.add(style.id);
    styles.push({ ...style, source, path });
  }
  return styles;
}

export async function discoverStyles(projectRoot) {
  const builtIns = await loadStyleDirectory(styleRoot, 'built-in');
  const localDirectory = projectRoot ? resolve(projectRoot, '.turbulencejs/presentation-styles') : null;
  const locals = localDirectory ? await loadStyleDirectory(localDirectory, 'project-local') : [];
  const merged = new Map(builtIns.map(style => [style.id, style]));
  for (const style of locals) merged.set(style.id, style);
  return { builtIns, locals, styles: [...merged.values()].sort((a, b) => a.id.localeCompare(b.id)), localDirectory };
}

export { styleRoot };
