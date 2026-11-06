import React, {useEffect, useRef, useState} from 'react';
import demo from '@site/docs/usage/disc/holobox/tutorials/IMAGES/CGH/uc2.png';
import {ifta, makePdf, shift} from './cgh';
import styles from './styles.module.css';

// Binarized picture in the upper half of an n x n far field, see make_target() in cgh_ifta.py
function makeTarget(img, n, invert) {
  const gap = Math.floor(n / 16);
  const f = Math.min((n - 2 * gap) / img.width, (n / 2 - 2 * gap) / img.height);
  const w = Math.max(1, Math.round(img.width * f)), h = Math.max(1, Math.round(img.height * f));
  const canvas = Object.assign(document.createElement('canvas'), {width: w, height: h});
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, w, h);
  ctx.drawImage(img, 0, 0, w, h);
  const px = ctx.getImageData(0, 0, w, h).data;
  const grey = Float64Array.from({length: w * h}, (_, k) => px[4 * k] + px[4 * k + 1] + px[4 * k + 2]);
  const mean = grey.reduce((a, b) => a + b) / grey.length;
  let lit = grey.map((v) => +(v > mean));
  const share = lit.reduce((a, b) => a + b) / lit.length;
  if ((share > 0.5) !== invert) lit = lit.map((v) => 1 - v); // light up the minority: black logo -> bright logo
  if (share === 0 || share === 1) throw new Error('No contrast left after binarizing. Try a picture with bold black and white shapes.');
  const T = new Float64Array(n * n), W = new Uint8Array(n * n);
  const r0 = Math.floor(n / 4) - Math.floor(h / 2), c0 = Math.floor(n / 2) - Math.floor(w / 2);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    T[(r0 + y) * n + c0 + x] = lit[y * w + x];
    W[(r0 + y) * n + c0 + x] = 1;
  }
  return {T, W};
}

function draw(canvas, values, n, vmax, rgb = [255, 255, 255]) {
  canvas.width = canvas.height = n;
  const ctx = canvas.getContext('2d'), im = ctx.createImageData(n, n);
  values.forEach((v, k) => {
    const g = Math.min(1, v / vmax);
    im.data.set([rgb[0] * g, rgb[1] * g, rgb[2] * g, 255], 4 * k);
  });
  ctx.putImageData(im, 0, 0);
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('Could not read this file as an image.'));
    img.src = src;
  });
}

export default function HologramMaker() {
  const [src, setSrc] = useState(demo);
  const [name, setName] = useState('uc2');
  const [opt, setOpt] = useState({dpi: 1200, dots: 1, size: 128, tiles: 8, invert: false});
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const refs = [useRef(), useRef(), useRef()];

  useEffect(() => {
    let cancelled = false;
    setBusy(true);
    const timer = setTimeout(async () => { // let the "calculating" message render first
      try {
        const n = opt.size, img = await loadImage(src);
        const {T, W} = makeTarget(img, n, opt.invert);
        const {mask, intensity} = ifta(shift(T, n), shift(W, n), n);
        if (cancelled) return;
        const I = shift(intensity, n);
        const above = Array.from(I.subarray(0, (n / 2 - n / 32) * n)).sort((a, b) => a - b); // the zero order would outshine the picture
        draw(refs[0].current, T, n, 1);
        draw(refs[1].current, mask, n, 1);
        draw(refs[2].current, I, n, above[Math.floor(0.999 * (above.length - 1))], [80, 255, 80]);
        let inWindow = 0;
        W.forEach((w, k) => { inWindow += w * I[k]; });
        setResult({mask, efficiency: inWindow / n ** 4});
        setError(null);
      } catch (e) {
        if (!cancelled) { setResult(null); setError(e.message); }
      }
      if (!cancelled) setBusy(false);
    }, 30);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [src, opt]);

  async function download() {
    const {size: n, tiles, dots, dpi} = opt, w = n * tiles * dots;
    const sheet = new Uint8Array(w * w);
    for (let y = 0; y < w; y++) for (let x = 0; x < w; x++) {
      sheet[y * w + x] = result.mask[(Math.floor(y / dots) % n) * n + (Math.floor(x / dots) % n)];
    }
    const a = document.createElement('a');
    a.href = URL.createObjectURL(await makePdf(sheet, w, dpi));
    a.download = `${name}_cgh_${dpi}dpi.pdf`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  const set = (key, cast = Number) => (e) => setOpt({...opt, [key]: cast(e.target.value)});
  const pitch = (25.4 / opt.dpi) * opt.dots; // mm per hologram pixel

  return (
    <div className={styles.maker}>
      <div className={styles.controls}>
        <label>Picture <input type="file" accept="image/*" onChange={(e) => {
          const file = e.target.files[0];
          if (file) { setSrc(URL.createObjectURL(file)); setName(file.name.replace(/\.[^.]*$/, '')); }
        }} /></label>
        <label>Printer <select value={opt.dpi} onChange={set('dpi')}>
          <option value={1200}>1200 dpi</option><option value={600}>600 dpi</option>
        </select></label>
        <label>Dots per pixel <select value={opt.dots} onChange={set('dots')}>
          {[1, 2, 3].map((v) => <option key={v} value={v}>{v}</option>)}
        </select></label>
        <label>Tile <select value={opt.size} onChange={set('size')}>
          {[64, 128, 256].map((v) => <option key={v} value={v}>{v} px</option>)}
        </select></label>
        <label>Tiles <input type="number" min={1} max={32} value={opt.tiles} onChange={set('tiles', (v) => Math.min(32, Math.max(1, Number(v) || 1)))} /></label>
        <label><input type="checkbox" checked={opt.invert} onChange={(e) => setOpt({...opt, invert: e.target.checked})} /> Invert</label>
      </div>
      {error && <p className={styles.error}>{error}</p>}
      <div className={styles.panels}>
        {['Binarized picture', 'One tile of the mask', 'What the wall shows'].map((title, i) => (
          <figure key={title}><canvas ref={refs[i]} /><figcaption>{title}</figcaption></figure>
        ))}
      </div>
      <p className={styles.info}>
        {busy ? 'Calculating…' : result && <>
          Pixel {(pitch * 1000).toFixed(1)} µm, tile {(opt.size * pitch).toFixed(2)} mm,
          print <b>{(opt.size * opt.tiles * pitch).toFixed(1)} mm square</b> (check with a ruler).
          The pattern repeats every {(0.532 / pitch).toFixed(0)} mm per metre to the wall (532 nm).
          Light in the picture: {(result.efficiency * 100).toFixed(1)} %.
        </>}
      </p>
      <button className="button button--primary" disabled={busy || !result} onClick={download}>Download PDF</button>
    </div>
  );
}
