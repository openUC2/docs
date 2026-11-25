import React, {useEffect, useRef, useState} from 'react';
import demo from '@site/docs/usage/disc/holobox/tutorials/IMAGES/CGH/uc2.png';
import {A4, ifta, makePdf, shift} from './cgh';

const MARGIN = 5; // mm, most printers can't print closer to the edge
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
  const [opt, setOpt] = useState({dpi: 1200, dots: 1, size: 128, tiles: 8, nm: 520, invert: false});
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [spot, setSpot] = useState(null); // centre of the print on the sheet in mm, null = page centre
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
  }, [src, opt.size, opt.invert]); // the other options only change the print and the numbers

  async function download() {
    const {size: n, tiles, dots, dpi} = opt, w = n * tiles * dots;
    const sheet = new Uint8Array(w * w);
    for (let y = 0; y < w; y++) for (let x = 0; x < w; x++) {
      sheet[y * w + x] = result.mask[(Math.floor(y / dots) % n) * n + (Math.floor(x / dots) % n)];
    }
    const a = document.createElement('a');
    a.href = URL.createObjectURL(await makePdf(sheet, w, dpi, place.x, place.y));
    a.download = `${name}_cgh_${dpi}dpi.pdf`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  const set = (key, cast = Number) => (e) => setOpt({...opt, [key]: cast(e.target.value)});
  const pitch = (25.4 / opt.dpi) * opt.dots; // mm per hologram pixel
  const side = opt.size * opt.tiles * pitch; // printed square in mm
  const clamp = (v, page) => Math.round(Math.min(page - MARGIN - side, Math.max(MARGIN, v - side / 2)));
  const place = {x: clamp(spot ? spot[0] : A4[0] / 2, A4[0]), y: clamp(spot ? spot[1] : A4[1] / 2, A4[1])}; // top-left in mm
  const fits = side <= A4[0] - 2 * MARGIN;

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
          {[1, 2, 3, 4].map((v) => <option key={v} value={v}>{v}</option>)}
        </select></label>
        <label>Tile <select value={opt.size} onChange={set('size')}>
          {[64, 128, 256].map((v) => <option key={v} value={v}>{v} px</option>)}
        </select></label>
        <label>Tiles <input type="number" min={1} max={32} value={opt.tiles} onChange={set('tiles', (v) => Math.min(32, Math.max(1, Number(v) || 1)))} /></label>
        <label>Laser <input type="number" min={350} max={1100} step={1} value={opt.nm} onChange={set('nm', (v) => Number(v) || 520)} /> nm</label>
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
          At {opt.nm} nm and 1 m to the wall, the picture centre sits {(opt.nm * 1e-6 / pitch / 4 * 1000).toFixed(1)} mm above
          the bright spot and the pattern repeats every {(opt.nm * 1e-6 / pitch * 1000).toFixed(1)} mm (both grow with the distance).
          Light in the picture: {(result.efficiency * 100).toFixed(1)} %.
        </>}
      </p>
      <div className={styles.placement}>
        <div className={styles.sheet} title="Click where the hologram should go"
          onClick={(e) => {
            const r = e.currentTarget.getBoundingClientRect();
            setSpot([((e.clientX - r.left) / r.width) * A4[0], ((e.clientY - r.top) / r.height) * A4[1]]);
          }}>
          <div className={styles.print} style={{left: `${(place.x / A4[0]) * 100}%`, top: `${(place.y / A4[1]) * 100}%`,
            width: `${(side / A4[0]) * 100}%`, height: `${(side / A4[1]) * 100}%`}} />
        </div>
        <div>
          <p>Click on the A4 sheet to choose where the hologram is printed, so you can use the rest of the foil for the next one.</p>
          <p>Top-left corner: <b>{place.x} mm</b> from the left edge, <b>{place.y} mm</b> from the top edge.</p>
          {!fits && <p className={styles.error}>The print is too big for A4. Use fewer tiles.</p>}
          <button className="button button--secondary button--sm" onClick={() => setSpot(null)}>Centre</button>{' '}
          <button className="button button--primary" disabled={busy || !result || !fits} onClick={download}>Download PDF</button>
        </div>
      </div>
    </div>
  );
}
