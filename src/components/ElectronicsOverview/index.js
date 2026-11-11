import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

// Clickable wiring overview of the FRAME electronics.
// Geometry is in viewBox units (1000 x 640); edit the numbers here to move things.
const BASE = '/dev/hw/electronics';

const img = {
  hat: require('@site/docs/dev/hw/electronics/hat-plus/img/hatplus-for-raspberrypi-5-iso.webp').default,
  panel: require('@site/docs/dev/hw/electronics/hat-panelboard/img/hat-panelboard-iso.webp').default,
  hub: require('@site/docs/dev/hw/electronics/wiring-boards/img/XH-connector-hub-iso.webp').default,
  motor: require('@site/docs/dev/hw/electronics/stepper-backpack/img/stepper-backpack-iso.webp').default,
  laser: require('@site/docs/dev/hw/electronics/laser-interface/img/laser-interface-iso.webp').default,
  led: require('@site/docs/dev/hw/electronics/illumination/img/illumination-iso.webp').default,
  galvo: require('@site/docs/dev/hw/electronics/galvo-interface/img/galvo-interface-iso.webp').default,
  gpio: require('@site/docs/dev/hw/electronics/can-gpio/img/can-gpio-esp-iso.webp').default,
};

const TRUNK_X = 560;
const satellites = [
  {y: 70, to: 'stepper-backpack', src: img.motor, title: 'Stepper backpack ×4', sub: 'TMC2209, endstops, encoder', node: 'nodes 10–13 (A, X, Y, Z)'},
  {y: 195, to: 'laser-interface', src: img.laser, title: 'Laser interface', sub: '4 × PWM behind an interlock', node: 'node 20'},
  {y: 320, to: 'illumination', src: img.led, title: 'Illumination board', sub: 'RGB rings, white LED', node: 'node 30'},
  {y: 445, to: 'galvo-interface', src: img.galvo, title: 'Galvo interface', sub: 'DAC, ±10 V, triggers', node: 'node 40'},
  {y: 570, to: 'can-gpio', src: img.gpio, title: 'CAN GPIO board', sub: 'E-stop, sensors, I2C', node: 'node 60'},
];

function Board({to, src, x, y, w, h, title, sub, node, labelX, labelY, anchor = 'start'}) {
  return (
    <Link to={`${BASE}/${to}/`} className={styles.board} aria-label={title}>
      <rect x={x - 6} y={y - 6} width={w + 12} height={h + 12} rx="8" className={styles.hit} />
      <image href={src} x={x} y={y} width={w} height={h} preserveAspectRatio="xMidYMid meet" />
      <text x={labelX} y={labelY} textAnchor={anchor} className={styles.title}>{title}</text>
      {sub && <text x={labelX} y={labelY + 19} textAnchor={anchor} className={styles.sub}>{sub}</text>}
      {node && <text x={labelX} y={labelY + 37} textAnchor={anchor} className={styles.node}>{node}</text>}
    </Link>
  );
}

export default function ElectronicsOverview() {
  return (
    <figure className={styles.wrap}>
      <svg viewBox="0 0 1000 640" className={styles.svg} role="group"
           aria-label="How the FRAME electronics are connected. Every board is a link to its page.">
        {/* Raspberry Pi: not one of our boards, drawn as a plain box */}
        <rect x="20" y="30" width="200" height="74" rx="8" className={styles.box} />
        <text x="120" y="62" textAnchor="middle" className={styles.title}>Raspberry Pi 5</text>
        <text x="120" y="82" textAnchor="middle" className={styles.sub}>ImSwitch OS</text>

        {/* Pi <-> HAT+ */}
        <line x1="120" y1="104" x2="120" y2="165" className={styles.wire} />
        <text x="130" y="131" className={styles.note}>40-pin header</text>
        <text x="130" y="147" className={styles.note}>5 V, UART, SPI</text>

        {/* HAT+ -> panel board */}
        <line x1="105" y1="372" x2="105" y2="440" className={styles.wire} />
        <text x="115" y="412" className={styles.note}>7-pin cable</text>

        {/* bus: HAT+ -> hub -> trunk -> satellites */}
        <path d={`M215 245 H340 M470 270 H${TRUNK_X} M${TRUNK_X} 70 V570`} className={styles.bus} />
        {satellites.map((s) => (
          <path key={s.to} d={`M${TRUNK_X} ${s.y} H604`} className={styles.bus} />
        ))}
        <text x="278" y="234" textAnchor="middle" className={styles.busLabel}>12 V + CAN</text>

        <Board to="hat-plus" src={img.hat} x={20} y={165} w={195} h={160}
               title="HAT+" sub="power, safety, CAN master" node="node 1"
               labelX={20} labelY={342} />
        <Board to="hat-panelboard" src={img.panel} x={20} y={440} w={170} h={110}
               title="Panel board" sub="camera trigger, fan, LEDs, I2C"
               labelX={20} labelY={572} />
        <Board to="wiring-boards" src={img.hub} x={340} y={205} w={130} h={110}
               title="Connector hub" sub="one bus in, eight out"
               labelX={405} labelY={336} anchor="middle" />
        {satellites.map((s) => (
          <Board key={s.to} to={s.to} src={s.src} x={608} y={s.y - 50} w={125} h={100}
                 title={s.title} sub={s.sub} node={s.node} labelX={748} labelY={s.y - 14} />
        ))}
      </svg>
      <figcaption className={styles.caption}>
        The electronics of a FRAME. Click a board to open its page. Every board with a controller
        also has a USB port for flashing and for testing it without the bus.
      </figcaption>
    </figure>
  );
}
