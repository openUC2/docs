// Browser port of cgh_ifta.py (HoloBox repo, ComputerGeneratedHologram/). Plain JS, no dependencies.
// Arrays are n*n, row-major, in FFT order (zero order at index 0).

function fft1(re, im, inverse) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      [re[i], re[j]] = [re[j], re[i]];
      [im[i], im[j]] = [im[j], im[i]];
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const a = ((inverse ? 2 : -2) * Math.PI) / len, wr = Math.cos(a), wi = Math.sin(a);
    for (let i = 0; i < n; i += len) {
      let cr = 1, ci = 0;
      for (let k = 0; k < len / 2; k++) {
        const p = i + k, q = p + len / 2;
        const tr = re[q] * cr - im[q] * ci, ti = re[q] * ci + im[q] * cr;
        re[q] = re[p] - tr; im[q] = im[p] - ti;
        re[p] += tr; im[p] += ti;
        [cr, ci] = [cr * wr - ci * wi, cr * wi + ci * wr];
      }
    }
  }
}

// in place, n must be a power of two
export function fft2(re, im, n, inverse = false) {
  const r = new Float64Array(n), i = new Float64Array(n);
  for (const rows of [true, false]) {
    for (let a = 0; a < n; a++) {
      const at = (k) => (rows ? a * n + k : k * n + a);
      for (let k = 0; k < n; k++) { r[k] = re[at(k)]; i[k] = im[at(k)]; }
      fft1(r, i, inverse);
      for (let k = 0; k < n; k++) { re[at(k)] = r[k]; im[at(k)] = i[k]; }
    }
  }
  if (inverse) for (let k = 0; k < n * n; k++) { re[k] /= n * n; im[k] /= n * n; }
}

// centred <-> FFT order (the same for even n)
export function shift(a, n) {
  const out = new a.constructor(n * n), h = n / 2;
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) out[((y + h) % n) * n + ((x + h) % n)] = a[y * n + x];
  return out;
}

const median = (a) => Float64Array.from(a).sort()[a.length >> 1];

// Weighted Gerchberg-Saxton for a 0/1 amplitude mask, see ifta() in cgh_ifta.py.
// A: target amplitude, W: 1 inside the picture window. Returns the mask (1 = clear foil) and |FFT(mask)|^2.
export function ifta(A, W, n, iters = 100) {
  const N = n * n, weight = Float64Array.from(A), h = new Float64Array(N), g = new Float64Array(N);
  const re = new Float64Array(N), im = new Float64Array(N), Gr = new Float64Array(N), Gi = new Float64Array(N);
  for (let k = 0; k < N; k++) {
    const p = 2 * Math.PI * Math.random();
    re[k] = A[k] * Math.cos(p); im[k] = A[k] * Math.sin(p);
  }
  for (let it = 0; it < iters; it++) {
    fft2(re, im, n, true);
    const m = median(re);
    let sd = 0;
    for (let k = 0; k < N; k++) { re[k] -= m; sd += re[k] * re[k]; }
    const soft = Math.max(0, 1 - it / (0.7 * iters)) * Math.sqrt(sd / N);
    for (let k = 0; k < N; k++) h[k] = soft ? Math.min(1, Math.max(0, 0.5 + re[k] / (2 * soft))) : +(re[k] > 0);
    Gr.set(h); Gi.fill(0);
    fft2(Gr, Gi, n);
    let gOn = 0, nOn = 0;
    for (let k = 0; k < N; k++) {
      g[k] = Math.hypot(Gr[k], Gi[k]);
      if (W[k] && A[k] > 0) { gOn += g[k]; nOn++; }
    }
    let eG = 0, eW = 0;
    for (let k = 0; k < N; k++) {
      if (W[k] && A[k] > 0) weight[k] *= Math.sqrt(gOn / nOn / g[k]); // ask more from picture points that came out dim
      if (W[k]) { eG += g[k] * g[k]; eW += weight[k] * weight[k]; }
    }
    const scale = Math.sqrt(eG / eW); // the energy the mask really puts into the window
    for (let k = 0; k < N; k++) {
      if (W[k]) {
        const a = (weight[k] * scale) / (g[k] || 1);
        re[k] = Gr[k] * a; im[k] = Gi[k] * a;
      } else { re[k] = Gr[k]; im[k] = Gi[k]; }
    }
  }
  const mask = Uint8Array.from(h, (v) => +(v > 0.5));
  Gr.set(mask); Gi.fill(0);
  fft2(Gr, Gi, n);
  return { mask, intensity: Float64Array.from(Gr, (v, k) => v * v + Gi[k] * Gi[k]) };
}

// Single-page A4 PDF with the 1-bit pattern (1 = clear) at exact size, lossless (Flate).
export async function makePdf(bits, w, dpi) {
  const rowBytes = Math.ceil(w / 8), raw = new Uint8Array(rowBytes * w);
  for (let y = 0; y < w; y++) for (let x = 0; x < w; x++) if (bits[y * w + x]) raw[y * rowBytes + (x >> 3)] |= 0x80 >> (x & 7);
  const data = new Uint8Array(await new Response(new Blob([raw]).stream().pipeThrough(new CompressionStream('deflate'))).arrayBuffer());
  const s = ((w / dpi) * 72).toFixed(3), x0 = ((595.28 - s) / 2).toFixed(3), y0 = ((841.89 - s) / 2).toFixed(3);
  const draw = `q ${s} 0 0 ${s} ${x0} ${y0} cm /Im Do Q`;
  const objects = [
    ['<< /Type /Catalog /Pages 2 0 R >>'],
    ['<< /Type /Pages /Kids [3 0 R] /Count 1 >>'],
    ['<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Resources << /XObject << /Im 4 0 R >> >> /Contents 5 0 R >>'],
    [`<< /Type /XObject /Subtype /Image /Width ${w} /Height ${w} /ColorSpace /DeviceGray /BitsPerComponent 1 /Filter /FlateDecode /Length ${data.length} >>\nstream\n`, data, '\nendstream'],
    [`<< /Length ${draw.length} >>\nstream\n${draw}\nendstream`],
  ];
  const parts = ['%PDF-1.4\n'], offsets = [];
  let pos = parts[0].length;
  const add = (p) => { parts.push(p); pos += p.length; };
  objects.forEach((obj, i) => {
    offsets.push(pos);
    add(`${i + 1} 0 obj\n`);
    obj.forEach(add);
    add('\nendobj\n');
  });
  const xref = pos;
  add(`xref\n0 ${objects.length + 1}\n0000000000 65535 f \n${offsets.map((o) => `${String(o).padStart(10, '0')} 00000 n \n`).join('')}`);
  add(`trailer\n<< /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`);
  return new Blob(parts, { type: 'application/pdf' });
}
