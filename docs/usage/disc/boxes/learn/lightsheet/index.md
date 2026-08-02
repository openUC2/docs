# LightSheet Add-On – Lernpfad

> **Status:** Skeleton. Quelle: [lightsheet.md](../../lightsheet.md). **Voraussetzung:** CoreBox + Electronics + Infinity + Fluorescence (Laser) + Raspberry-Pi-Kit.

Das LightSheet Add-On erweitert das System um das openSPIM-inspirierte Konzept: Ein Laserstrahl wird über eine Zylinderlinse zu einem dünnen Lichtblatt geformt, das die Probe orthogonal zur Detektion beleuchtet. Damit sind sanfte 3D-Aufnahmen lebender Proben (z. B. Zebrafisch-Embryos) möglich.

## Lernpfad

```
Was ist ein Lichtblatt? ─► Zylinderlinse verstehen ─► Lichtblatt aufbauen & ausrichten
                                                                  │
                                                                  ▼
                       Probenkammer befüllen ─► Orthogonale Detektion ─► Z-Stack & 3D-Rekonstruktion
```

## Experimente

### 1. Lichtblatt – das Prinzip

**Einstieg / Phänomen**
- *Was siehst du, wenn du mit einer Taschenlampe ein Aquarium von der Seite beleuchtest – erkennst du eine Schicht?*
- *Wie unterscheidet sich das Epifluoreszenz-Bild einer 3D-Probe von einem Lichtblatt-Bild?*

**Physikalischer Hintergrund**
- *Warum reduziert die selektive Beleuchtung die Phototoxizität im Vergleich zur Epifluoreszenz um einen Faktor 10–100?*
- *Was bedeutet „optische Sektionierung", und wie hängt die Schnittdicke von Lichtblattdicke und Detektions-NA ab?*

**Alltagsbezug / Forschung**
- *Wie wird SPIM (Selective Plane Illumination Microscopy) genutzt, um ganze Zebrafisch-Embryos lebend abzubilden?*
- *Wo wird Lichtblatt-Mikroskopie kommerziell eingesetzt (Zeiss Lightsheet Z.1, Leica THUNDER)?*

**Variation**
- *Vergleiche: Was zeigt eine einzelne Z-Ebene im Epifluoreszenz-Modus vs. im Lichtblatt-Modus?*

**Differenzierung**
- *Sek I / Einstieg: Erkläre das Prinzip mit einer Laserpointer-Demonstration in einem Milch-Wasserglas.*
- *Sek II / Vertiefung: Leite die Lichtblattdicke aus der Gaussian-Beam-Optik (Rayleigh-Länge, Waist) her.*

- → `experiments/01_lichtblatt_prinzip.md`

### 2. Zylinderlinse – aus Strahl wird Blatt

**Einstieg / Phänomen**
- *Halte die Zylinderlinse vor eine Lichtquelle und drehe sie: Was siehst du auf dem Schirm?*
- *Was passiert, wenn du eine sphärische Linse verwendest – bekommst du auch ein Blatt?*

**Aufbau**
- *Wie setzt du die justierbare Zylinderlinse in den Cube ein, und nach welchem Kriterium richtest du sie aus?*
- *Welche Achse der Linse fokussiert, und warum bleibt die andere Achse kollimiert?*

**Messung / Quantifizierung**
- *Wie dünn ist das Lichtblatt am Fokuspunkt (Waist)? Miss es auf einem Schirm.*
- *Wie weit erstreckt sich die nutzbare Zone des Blatts (Rayleigh-Länge $z_R = \pi w_0^2 / \lambda$)?*

**Variation**
- *Wie ändert sich die Blattdicke, wenn du die Zylinderlinse gegen eine mit kürzerer Brennweite tauschst?*
- *Was siehst du, wenn du die Zylinderlinse um 90° rotierst?*

**Fehleranalyse**
- *Was tust du, wenn das Blatt nicht symmetrisch ist (eine Seite dicker als die andere)?*

**Physikalischer Hintergrund**
- *Erkläre astigmatische Fokussierung und warum der Gaussian-Beam-Waist in nur einer Raumdimension entsteht.*

- → `experiments/02_zylinderlinse.md`

### 3. Lichtblatt aufbauen & ausrichten

**Einstieg / Phänomen**
- *Was siehst du auf der Justage-Kamera, bevor das Lichtblatt richtig ausgerichtet ist?*
- *Wie erkennst du, dass Beleuchtungs- und Detektionsachse wirklich senkrecht stehen?*

**Aufbau / Justage-Workflow**
- *Welche Reihenfolge empfiehlt sich: Zylinderlinse, Spiegel, Objektiv, Kammer?*
- *Wie nutzt du die Justage-Kamera, um das Blatt in der Detektionsebene zu positionieren?*

**Messung / Qualitätskontrolle**
- *Welche Kriterien prüfst du: Blattdicke am Zentrum, Blattdicke am Rand, Verkippung, Lateralversatz?*
- *Wie misst du die Lichtblattdicke aus dem Kamerabild (Gaussian-Fit an Intensitätsprofil)?*

**Variation**
- *Was ändert sich im Fluoreszenz-Bild, wenn du das Lichtblatt um 5° verkippt ist?*
- *Wie justierst du nach, wenn das Lichtblatt nach einer Stunde thermal driftet?*

**Fehleranalyse**
- *Was tust du, wenn das Lichtblatt unsymmetrisch erscheint (Dejustage der Zylinderlinse)?*
- *Wie erkennst du, dass Reflexionen der Probenkammer störende Streifenmuster erzeugen?*

**Alltagsbezug**
- *Wie lösen kommerzielle Systeme das Ausrichtungsproblem (motorisierte Achsen, automatische Kalibrierung)?*

- → `experiments/03_lichtblatt_justage.md`

### 4. Probenkammer und Probenmontage

**Einstieg / Phänomen**
- *Was siehst du, wenn du die Kammer nicht vollständig entlüftest – welche Artefakte entstehen durch Luftblasen?*
- *Warum muss die Probe im Medium (Wasser, Agarose) hängen statt auf einem Objektträger zu liegen?*

**Aufbau**
- *Wie befüllst du die Kammer Blasen-frei (langsam von unten, Schräghalten)?*
- *Wie bereitest du eine Agarose-Probe vor: Konzentration, Einbettungsprotokoll, Spritzen-Halter?*

**Messung**
- *Wie kontrollierst du, ob der Brechungsindex der Einbettmediums zur verwendeten Optik passt?*
- *Wie findest du die Probe in der Kammer – zuerst im Durchlicht (NeoPixel) dann in Fluoreszenz?*

**Variation**
- *Wie ändert sich das Bild bei verschiedenen Agarose-Konzentrationen (0.5 %, 1 %, 2 %)?*
- *Was passiert, wenn du die Probe aus der Kammer herausragt (Randeffekte)?*

**Fehleranalyse**
- *Was tust du, wenn die Probe sich im Lichtblatt dreht (Konvektion, Agarose zu weich)?*

**Physikalischer Hintergrund**
- *Warum führt Brechungsindex-Mismatch zu Aberrationen und verminderter Lichtblattqualität tief im Gewebe?*

- → `experiments/04_probenkammer.md`

### 5. Orthogonale Detektion

**Einstieg / Phänomen**
- *Was würde passieren, wenn Detektion und Beleuchtung in dieselbe Richtung zeigten – warum verlieren wir den Schicht-Kontrast?*
- *Wie erkennst du im Bild, dass wirklich nur die beleuchtete Ebene sichtbar ist?*

**Aufbau**
- *Wie überprüfst du mit einem Winkelmesser, dass Detektionsobjektiv und Lichtblatt-Achse tatsächlich 90° bilden?*
- *Wo sitzt der Emissionsfilter im Detektionspfad, und wie sicherst du ihn?*

**Messung / Quantifizierung**
- *Miss die axiale Schnittdicke: Scan eine fluoreszierende Kugel (Bead) durch das Lichtblatt und bestimme die FWHM.*
- *Vergleiche den Signalabfall mit und ohne Emissionsfilter.*

**Variation**
- *Was siehst du im Bild, wenn du den Detektionspfad geringfügig verkippt (nicht exakt 90°)?*
- *Wie ändert sich der Out-of-Focus-Hintergrund, wenn du die Lichtblattdicke verdoppelst?*

**Physikalischer Hintergrund**
- *Wie beschreibt der optische Übertragungsterm die axiale Auflösung: $\Delta z \approx \lambda_\text{em} / \text{NA}_\text{det}^2$ (Beugungslimit)?*

**Alltagsbezug**
- *Welche medizinischen Bildgebungsverfahren nutzen orthogonale Geometrien (OCT, Lichtblatt-Endoskopie)?*

- → `experiments/05_orthogonale_detektion.md`

### 6. Z-Stack und 3D-Rekonstruktion

**Einstieg / Phänomen**
- *Wie sieht eine einzelne Z-Ebene aus, und was fehlt, bis du das 3D-Volumen erkennst?*
- *Was bedeutet Nyquist-Abtastrate hier: Wie fein muss der Z-Schritt im Vergleich zur Lichtblattdicke sein?*

**Aufbau / Software**
- *Wie konfigurierst du den Scan-Loop in ImSwitch: Starttposition, Endposition, Schrittweite, Trigger?*
- *Welches Format speichert du den Stack (OME-TIFF, HDF5 / Zarr) für spätere Analyse?*

**Messung / Quantifizierung**
- *Wie viele Ebenen brauchst du, um ein 500-µm-Volumen Nyquist-korrekt abzutasten (Lichtblattdicke = 5 µm)?*
- *Wie lange dauert der Scan, und was bestimmt die Geschwindigkeit (Kamera-Framerate, Motor-Speed, Fluoreszenz-Intensität)?*

**Visualisierung**
- *Wie erstellst du eine Maximum-Intensity-Projection (MIP) in Fiji?*
- *Wie visualisierst du das Volumen 3D in napari oder Fiji 3D Viewer?*

**Fehleranalyse**
- *Was tust du, wenn der Stack Streifen-Artefakte zeigt (Schattenstreifen durch Streuer im Lichtblatt)?*
- *Wie kompensierst du Drift zwischen dem ersten und letzten Bild des Stacks?*

**Alltagsbezug / Erweiterung**
- *Wie nutzt die moderne Entwicklungsbiologie Lichtblatt-Stacks für Cell-Tracking in Zebrafisch-Embryos?*

- → `experiments/06_zstack_3d.md`

### 7. NeoPixel-Durchlicht für Übersicht

**Einstieg / Phänomen**
- *Was siehst du im Durchlicht-Modus mit den NeoPixel-LEDs im Vergleich zum Fluoreszenz-Modus?*
- *Warum ist das Hellfeld-Übersichtsbild nützlich, bevor du zum Fluoreszenz-Scan wechselst?*

**Aufbau**
- *Wie adressierst du die NeoPixel-LEDs über das ESP32-Board für weiße Beleuchtung?*
- *Wie schaltest du zwischen Durchlicht und Fluoreszenz-Beleuchtung um, ohne die Probe zu bewegen?*

**Messung**
- *Wie nutzt du das Durchlichtbild, um die Probe zu navigieren und einen Interessensbereich (ROI) zu finden?*
- *Wie vergleichst du Durchlicht- und Fluoreszenz-Bild derselben Ebene (Overlay, Colourierung)?*

**Variation**
- *Welche Farbe der NeoPixel-LEDs eignet sich für welche Probe (weißes Licht vs. grünes vs. rotes)?*

**Fehleranalyse**
- *Was tust du, wenn die NeoPixel-LEDs unterschiedlich hell leuchten (Kalibration)?*

**Physikalischer Hintergrund**
- *Warum zeigt das Durchlichtbild einer transparenten Probe kaum Kontrast, während Phasenkontrast oder DPC hier helfen würden?*

**Alltagsbezug**
- *Wie nutzen multimodale Mikroskope (Durchlicht + Fluoreszenz) die Möglichkeit, Zellen gleichzeitig morphologisch und molekular zu charakterisieren?*

- → `experiments/07_neopixel_uebersicht.md`

## Cube-Module / Komponenten

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| Zylinderlinse 100 mm (justierbar) | Lichtblatt-Erzeugung | `modules/cylinder_lens_100.md` |
| Probenkammer (wassergefüllt, NeoPixel) | Probenhalter inkl. Durchlicht-LED | `modules/sample_chamber.md` |
| Mikrometer-XYZ-Stage | Probenpositionierung, Spritzen-Halter | `modules/xyz_micrometer_stage.md` |
| Emissionsfilter (steckbar) | Spektrale Trennung | `modules/em_filter_removable.md` |
| Justage-Kamera | Hilfe bei Ausrichtung | `modules/alignment_camera.md` |
| Solid Baseplate 10 mm POM, 4×5 | Stabile mechanische Basis | `modules/solid_baseplate_4x5.md` |

## Didaktische Anker

- Konkretes Beispiel für moderne biologische Bildgebung.
- Konzept „orthogonale Geometrie" als didaktisches Highlight.
- 3D-Daten als Brücke zu Bildverarbeitung / Informatik.

## Offene Fragen / TODO

- Beispiel-Probenprotokoll (Zebrafisch, fluoreszente Mikrosphären).
- Schritt-für-Schritt-ImSwitch-Konfiguration.
- Sicherheits- und Wassermanagement-Hinweise.
