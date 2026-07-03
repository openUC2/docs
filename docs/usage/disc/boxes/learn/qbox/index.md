# QBox – Lernpfad (Quantenoptik & Interferometrie)

> **Status:** Skeleton. Quelle: [qbox.md](../../qbox.md). **Voraussetzung:** keine (eigenständig). Optional kombinierbar mit der CoreBox.

Die QBox ist das eigenständige Set für Wellen- und Quantenoptik: kinetische Spiegel, polarisations­optische Bauteile, ein 520 nm-Laser, ein ESP32-S3 mit Mikrowellen­anbindung und Mikrodiamanten für ODMR. Sie deckt ein breites Spektrum von der klassischen Interferometrie bis zu BB84 und ODMR ab.

## Lernpfad

```
Polarisation ─► Doppelspalt / Gitter ─► Michelson-Interferometer
                                                │
                                                ▼
                          Mach-Zehnder ─► Quantenradierer ─► BB84
                                                │
                                                ▼
                                              ODMR (NV-Zentren)
```

## Experimente

### 1. Polarisation – Grundlagen

**Einstieg / Phänomen**
- *Was siehst du, wenn du zwei Polarisationsfilter hintereinander hältst und einen davon drehst?*
- *Warum wird das Bild durch eine Sonnenbrille mit Polarisationsfilter bei schräger Draufsicht auf Wasser dunkler?*

**Messung / Quantifizierung**
- *Miss die Intensität als Funktion des Drehwinkels θ und überprüfe das Malus-Gesetz $I = I_0 \cos^2(\theta)$.*
- *Wie bestimmst du den Extinktionsgrad (Verhältnis maximaler zu minimaler Transmission) des Filters?*

**Variation**
- *Was passiert, wenn du eine Zuckerlösung zwischen zwei Polarisatoren stellst – und warum dreht sie die Polarisationsebene?*
- *Wie verhält sich eine Glasscheibe bei Brewster-Winkel (Reflexionspolarisation)?*

**Fehleranalyse**
- *Warum ist die Intensität bei 90° nicht exakt Null (Streulicht, unvollkommener Filter)?*

**Physikalischer Hintergrund**
- *Was ist lineare, zirkulare und elliptische Polarisation, und wie beschreibt der Stokes-Vektor den Zustand?*

**Alltagsbezug / Differenzierung**
- *Sek I: Erkläre, wie ein 3D-Kino-Brillen-System auf Polarisation basiert.*
- *Sek II / Vertiefung: Miss mit dem Malus-Gesetz drei Daten­punkte und berechne $\chi^2$ für das Modell.*

- → `experiments/01_polarisation.md`

### 2. Doppelspalt- und Gitter-Experiment

**Einstieg / Phänomen**
- *Was siehst du auf dem Schirm hinter einem Einfachspalt, einem Doppelspalt, einem Gitter – und warum werden die Maxima schmaler?*
- *Welche Farben siehst du mit weißem Licht am Gitter, und warum?*

**Messung / Quantifizierung**
- *Miss den Abstand der Hauptmaxima und berechne den Spaltabstand $d$ aus $d \sin\theta = m\lambda$.*
- *Wie hängen Spaltabstand, Wellenlänge und Schirm-Abstand zusammen?*

**Variation**
- *Wie ändert sich das Muster, wenn du einen breiteren oder schmaleren Spalt einsetzt?*
- *Was siehst du, wenn du den Spalt mit einem Polarisationsfilter kombinierst?*

**Fehleranalyse**
- *Warum erscheinen die Maxima bei großem Schirmabstand unschärfer (Kohärenzlänge des Lasers)?*

**Physikalischer Hintergrund**
- *Welches Modell erklärt das Doppelspaltmuster: Huygens-Fresnel-Prinzip, Superposition zweier Kugelwellen?*
- *Warum erfordert dieses Experiment einen Modellwechsel von Strahlen- zu Wellenoptik?*

**Alltagsbezug / Differenzierung**
- *Sek I: Berechne den Spaltabstand einer CD (bekannte Wellenlänge und Beobachtungswinkel).*
- *Sek II / Vertiefung: Was ändert sich im Doppelspaltmuster, wenn ein Photon das System durchläuft (Quantenmechanik)?*

- → `experiments/02_doppelspalt.md`

### 3. Michelson-Interferometer

**Einstieg / Phänomen**
- *Was siehst du auf dem Schirm, wenn du einen Arm des Interferometers mit dem Finger berührst – und warum bewegen sich die Ringe?*
- *Was passiert mit dem Muster, wenn du eine Glasscheibe in einen Arm einbringst?*

**Aufbau**
- *In welcher Reihenfolge richtest du Laser, Strahlteiler, zwei Spiegel und Schirm aus?*
- *Wie feinjustierst du einen der kinetischen Spiegel, bis du konzentrische Ringe siehst?*

**Messung / Quantifizierung**
- *Miss die Wellenlänge des Lasers: Zähle die vorbeiziehenden Maxima bei bekannter Armlängenänderung.*
- *Wie berechnet sich der Gangunterschied $\Delta = 2\Delta L$ und das zugehörige Muster?*

**Variation**
- *Was siehst du, wenn du die Kohärenzlänge des Lasers überschreitest (sehr verschiedene Armlängen)?*

**Fehleranalyse**
- *Was tust du, wenn das Muster „wandert" (thermische Drift, Vibrationen)?*
- *Wie erkennst du, dass Spiegel nicht plan sind (verbogene Ringe)?*

**Physikalischer Hintergrund**
- *Wie erklärt die Zwei-Strahl-Interferenz das Muster: $I = I_0(1 + \cos(k\Delta))$?*
- *Wie wurde das Michelson-Morley-Experiment genutzt, um den Äther zu falsifizieren?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: Wie funktioniert ein Laser-Interferometer in LIGO für Gravitationswellen-Detektion?*

- → `experiments/03_michelson.md`

### 4. Mach-Zehnder-Interferometer

**Einstieg / Phänomen**
- *Warum teilt das Mach-Zehnder den Strahl in zwei räumlich getrennte Wege – was ist der Vorteil gegenüber Michelson?*
- *Was siehst du im Ausgangspfad, wenn beide Wege exakt gleich lang sind?*

**Aufbau**
- *Welche Cubes brauchst du: zwei Strahlteiler, zwei Spiegel, und wie ordnest du sie an?*
- *Wie justierst du die Ausgänge so, dass du ein Streifenmuster siehst?*

**Messung / Quantifizierung**
- *Wie verändert sich das Muster, wenn du ein transparentes Objekt (Deckglas, Prüfglas) in einen Arm bringst?*
- *Wie quantifizierst du die Phasenverschiebung aus dem Streifen-Versatz?*

**Variation**
- *Wie wirkt ein schief gestellter Strahlteiler auf das Muster (Verkippungsfehler)?*

**Physikalischer Hintergrund**
- *Was ist der Unterschied zwischen Amplituden- und Phasen-Objekt, und warum sieht man Letzeres im Hellfeld kaum?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: Wie wird Mach-Zehnder in der optischen Kohärenztomographie (OCT) und in photonischen Chips für schnelle Datenkommunikation eingesetzt?*

- → `experiments/04_mach_zehnder.md`

### 5. Quantenradierer

**Einstieg / Phänomen**
- *Was passiert mit dem Interferenzmuster am Doppelspalt, wenn du jedem Spalt eine orthogonale Polarisation zuordnest?*
- *Was passiert, wenn du anschließend einen dritten Polarisator bei 45° davor stellst – und warum kehrt das Muster zurück?*

**Aufbau**
- *Wie kombinierst du Doppelspalt, polarisierende Folien und Analyser-Polarisator in einem Aufbau?*
- *Wie überzeugst du dich, dass die Polarisationen wirklich orthogonal sind (gekreuzte Filter, kein Durchgang)?*

**Messung / Quantifizierung**
- *Wie ändert sich die Sichtbarkeit (Visibility) $V = (I_\text{max} - I_\text{min})/(I_\text{max} + I_\text{min})$ mit und ohne Welcher-Weg-Markierung?*

**Fehleranalyse**
- *Warum ist das Muster auch ohne Markierung nicht perfekt (Kohärenz, Detektorlimit)?*

**Physikalischer Hintergrund**
- *Was ist „Welcher-Weg"-Information im quantenmechanischen Sinne, und warum hebt sie die Kohärenz auf (Komplementaritätsprinzip)?*
- *Wie erklärt der Dichte-Matrix-Formalismus den Übergang von kohärentem zu gemischtem Zustand?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: Formuliere das Experiment im Bra-Ket-Formalismus und zeige, warum das Spurieren über den Weg-Freiheitsgrad die Interferenz löscht.*

- → `experiments/05_quantenradierer.md`

### 6. Polarisations-Strahlteiler & Cube-Setup

**Einstieg / Phänomen**
- *Was siehst du an den zwei Ausgängen eines PBS mit linear polarisiertem Eingangsstrahl bei 0°, 45°, 90°?*
- *Wie verhält sich das Intensitätsverhältnis der zwei Ausgänge als Funktion des Eingangspolarisationswinkels?*

**Aufbau**
- *Wie montierst du den PBS-Cube und richtest den Eingangsstrahl auf die Teilerfläche aus?*
- *Wie kombinierst du PBS mit einem λ/2-Plättchen, um die Intensitätsaufteilung kontinuierlich einzustellen?*

**Messung / Quantifizierung**
- *Miss das Intensitätsverhältnis der zwei Ausgänge als Funktion des λ/2-Winkels.*

**Variation**
- *Was passiert, wenn du zirkulär polarisiertes Licht (λ/4) in den PBS einstrahlst?*

**Physikalischer Hintergrund**
- *Welche Symbole und Diagramme nutzen Quantenoptiker für Zustände und Operationen (Bloch-Kugel, Ket-Notation)?*
- *Wie funktioniert das PBS-Prinzip auf Basis von Dünnschicht-Beschichtungen?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: Wie nutzt man PBS + λ/2 + λ/4 als Variables Beam-Splitter-Ratio-Element in Experimenten zur Quantenkommunikation?*

- → `experiments/06_pbs.md`

### 7. BB84 – Quantenkryptographie (Demo)

**Einstieg / Phänomen**
- *Wie kannst du mit Polarisationszuständen eine „1" und eine „0" kodieren – ohne dass ein Lauscher es sicher lesen kann?*
- *Was passiert mit dem Schlüssel, wenn ein Lauscher (Eve) jeden Photonenzustand misst?*

**Aufbau**
- *Welche Komponenten spielen Alice, Bob und Eve in deinem Aufbau (Laser, Polarisatoren, PBS, Detektoren)?*
- *Wie simulierst du zufällige Basiswahl (Würfel, Zufallsgenerator, Schaltlogik)?*

**Messung / Quantifizierung**
- *Wie groß ist die Fehlerrate (QBER = Quantum Bit Error Rate) ohne und mit aktivem Lauscher?*
- *Ab welchem QBER-Wert würde Alice und Bob abbrecchen (typisch > 11 %)?*

**Physikalischer Hintergrund**
- *Warum kann ein Quantenzustand nicht ohne Störung geklont werden (No-Cloning-Theorem)?*
- *Welche Schritte des BB84-Protokolls führen von zufälligen Messergebnissen zu einem sicheren Schlüssel (Sifting, Error-Correction, Privacy Amplification)?*

**Fehleranalyse**
- *Welche nicht-idealen Effekte (Polfilter-Crosstalk, Quellenrauschen) erhöhen den QBER auch ohne Lauscher?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: Berechne theoretisch die maximale sichere Schlüsselrate für eine 11 %-QBER-Linie.*
- *Erweiterung: Was ist QKD mit Glasfaser vs. Free-Space, und welche kommerziellen Produkte gibt es (ID Quantique, Toshiba)?*

- → `experiments/07_bb84.md`

### 8. ODMR – Optisch detektierte Magnetresonanz (NV-Zentren)

**Einstieg / Phänomen**
- *Was passiert mit der Fluoreszenz-Helligkeit des NV-Zentrums, wenn du Mikrowellen einstrahlen – und warum ändert sie sich?*
- *Wie sieht das ODMR-Spektrum (Fluoreszenz vs. Mikrowellenfrequenz) ohne externes Magnetfeld aus?*

**Aufbau**
- *Wie positionierst du den Mikrodiamond unter dem 520-nm-Laser und stellst die Mikrowellen-Antenne des ESP32-S3 dazu?*
- *Wie konfigurierst du den ESP32-S3 für einen Frequenz-Sweep (Start, Stop, Schritte) und die Fluoreszenz-Detektion?*

**Messung / Quantifizierung**
- *Miss die Resonanzfrequenz (ca. 2.87 GHz ohne Feld) und die Zeeman-Aufspaltung mit einem externen Magneten.*
- *Wie berechnet man die Magnetfeldstärke aus der Aufspaltung $\Delta f = 2 g_e \mu_B B / h$?*

**Variation**
- *Wie ändert sich die Aufspaltung, wenn du den Magneten näher oder weiter weg hältst?*
- *Was siehst du, wenn du zwei Magnete mit verschiedener Orientierung nutzt?*

**Fehleranalyse**
- *Was tust du, wenn das ODMR-Signal sehr schwach ist (falsche Fokus-Position, Diamant verschoben)?*
- *Wie unterscheidest du ODMR-Signal von Rauschen (Mittelwert mehrerer Scans)?*

**Physikalischer Hintergrund**
- *Was ist ein NV-Zentrum: Defektstruktur, Spin-Triplett-Grundzustand, ISC (Intersystem Crossing)?*
- *Wie erklärt der Spin-abhängige Zerfallspfad, warum Spinresonanz die Fluoreszenzintensität ändert?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: NV-Zentren als Quanten-Sensor – wie werden sie für Nano-MRT und Magnetfeld-Kartierung in Biologie eingesetzt?*

- → `experiments/08_odmr.md`

## Cube-Module / Komponenten

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| Kinetischer Spiegel 45°/90° (×2) | Justierbarer Strahlweg | `modules/kinetic_mirror.md` |
| Fester Spiegel 45°/90° | Strahlumlenkung | `modules/mirror_fixed.md` |
| 16 mm Linse | Kurzbrennweite, Strahlformung | `modules/lens_16.md` |
| 28 mm Linse | Strahlformung | `modules/lens_28.md` |
| Polarisations­filter, drehbar (×4) | Polarisations­experimente | `modules/polarizer.md` |
| Polarisations-Strahlteiler (×2) | Strahlteilung nach Polarisation | `modules/pbs.md` |
| Dichroit-Halter | Halterung für Dichroit | `modules/dichroic_holder.md` |
| Laser 520 nm (Cube) | Kohärente Lichtquelle | `modules/laser_520.md` |
| Magnet | ODMR – Magnetfeld | `modules/magnet.md` |
| Einzelspalt | Beugung | `modules/single_slit.md` |
| Doppelspalt | Interferenz | `modules/double_slit.md` |
| XYZ-Stage | Diamant-Justage | `modules/xyz_stage_diamond.md` |
| ESP32-S3 (Mikrowelle, Steuerung) | Elektronik | `modules/esp32_s3_qbox.md` |
| Solid Baseplate 4×5 | Mechanische Basis | `modules/solid_baseplate_4x5_q.md` |

## Didaktische Anker

- Sichtbarer Übergang Strahlen- → Wellen- → Quantenoptik.
- Konkretes Erleben von „nicht-klassischen" Phänomenen (Quantenradierer, BB84).
- Brücke Physik ↔ Informatik ↔ Materialwissenschaft (NV-Zentren).

## Offene Fragen / TODO

- Klare Lasersicherheits-Sektion (520 nm Klasse, Brille, Beschilderung).
- Workflow-Diagramm für Mikrowellen-Kalibrierung des ESP32-S3.
- Mathematischer Anhang (Malus, Beugungsformel, Visibility, BB84-Schlüsselrate).
