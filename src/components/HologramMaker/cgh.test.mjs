// node src/components/HologramMaker/cgh.test.mjs  --  same check as test_cgh_ifta.py, plus a parseable PDF
import assert from 'node:assert';
import { writeFileSync } from 'node:fs';
import { ifta, makePdf, shift } from './cgh.js';

const n = 64, T = new Float64Array(n * n), W = new Uint8Array(n * n);
for (let y = 4; y < 28; y++) for (let x = 4; x < 60; x++) {
  W[y * n + x] = 1;
  T[y * n + x] = +((y < 10 && x > 12 && x < 52) || (x > 28 && x < 36)); // a "T" in the upper half
}
const { mask, intensity } = ifta(shift(T, n), shift(W, n), n);
const I = shift(intensity, n);
let on = 0, nOn = 0, off = 0, nOff = 0, ones = 0;
for (let k = 0; k < n * n; k++) {
  ones += mask[k];
  if (W[k] && T[k]) { on += I[k]; nOn++; } else if (W[k]) { off += I[k]; nOff++; }
}
const contrast = on / nOn / (off / nOff);
assert(Math.abs(ones / (n * n) - 0.5) < 0.01, 'toner not 50 %');
assert(contrast > 10, `contrast ${contrast}`);
if (process.argv[2]) writeFileSync(process.argv[2], Buffer.from(await (await makePdf(mask, n, 1200)).arrayBuffer()));
console.log(`contrast ${contrast.toFixed(0)}:1, toner ${(100 - ones / n / n * 100).toFixed(1)} %`);
