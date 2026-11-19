// THE WORLD TODAY — Thursday 19 November 2026.
//
// Entry for make.fun's news-image-20261119 bounty ($250 in USDC).
// render.py (Python + Pillow) draws the front page from stories.json
// and ships it here as entry.png. All this program does is copy that
// file to the grader's output directory, so the run is deterministic:
// same input bytes, same output bytes, every time. No network, no
// randomness, no clock, no environment beyond the output directory.
// The image is 1024x1024 and under 256 KiB, inside the bounty limits.
//
// Local equivalent of the grader run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

function main() {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const here = dirname(fileURLToPath(import.meta.url));
  const bytes = readFileSync(join(here, 'entry.png'));
  const target = join(outDir, 'entry.png');
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, bytes);
}

main();
