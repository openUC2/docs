# Infinity Add-On – Lernpfad

> **Status:** Skeleton. Quelle: [infinitybox.md](../../infinitybox.md). **Voraussetzung:** CoreBox + Electronics Add-On.

Das Infinity Add-On hebt das CoreBox-Mikroskop auf Industrie­standard: unendlich-korrigiertes 10×-Objektiv, 100 mm CCTV-Tubuslinse, monochrome USB-3-Industrie­kamera (Sony IMX179) und Iris-Blende.

## Lernpfad

```
Wieso unendlich? ─► Objektiv + Tubuslinse zusammensetzen ─► Industriekamera anschließen
                                                                       │
                                                                       ▼
                            Vergrößerung kalibrieren ─► Blende & Auflösung ─► Live-Bild aufnehmen / speichern
```

## Experimente

### 1. Endlich vs. Unendlich – der Vergleich

**Einstieg / Phänomen**
- *Was passiert, wenn du ein Infinity-Objektiv ohne Tubuslinse benutzt – gibt es überhaupt ein Bild?*
- *Wie verschiebt sich die Bildschärfe, wenn du einen Glasblock (Filter) in den endlichen Strahlengang einschiebst?*

**Aufbau**
- *Wie baust du die endliche Konfiguration (Objektiv + feste Tubuslänge) neben der Infinity-Konfiguration auf?*
- *Welche Cubes brauchst du für den direkten Vergleich an derselben Probe?*

**Messung / Quantifizierung**
- *Miss die effektive Vergrößerung beider Systeme bei gleicher Probe – stimmen sie überein?*
- *Wie ändert sich die Bildposition auf dem Sensor, wenn du in der Endlich-Konfiguration einen 2 mm-Filter einschiebst?*

**Variation**
- *Setze denselben Filter in die Infinity-Konfiguration – ändert sich die Bildlage?*
- *Was passiert, wenn du die Tubuslinse aus dem Infinity-Pfad entfernst und durch eine mit anderer Brennweite ersetzt?*

**Physikalischer Hintergrund**
- *Warum erlaubt der parallele (kollimierte) Strahl zwischen Objektiv und Tubuslinse das beliebige Einschieben von Optiken ohne Bildversatz?*
- *Was bedeutet die Normtubuslänge von 200 mm (Nikon/Olympus) vs. 160 mm (endlich) für die Korrektionseigenschaften des Objektivs?*

**Alltagsbezug / Differenzierung**
- *Sek I: Erkläre mit einer Skizze den Unterschied zwischen endlichem und unendlichem Strahlengang.*
- *Sek II / Vertiefung: Berechne den Bildversatz für einen Glasblock der Dicke $d$ und Brechzahl $n$ im endlichen Strahlengang.*

- → `experiments/01_endlich_vs_unendlich.md`

### 2. Tubuslinsen-Brennweite & resultierende Vergrößerung

**Einstieg / Phänomen**
- *Was siehst du auf dem Sensor, wenn du die 100-mm-Tubuslinse gegen die 50-mm-CoreBox-Linse tauschst?*
- *Wie ändert sich das Sichtfeld (in µm) bei gleicher Sensorauflösung?*

**Aufbau**
- *Wie montierst du die CCTV-Tubuslinse in den Cube und sicherst den C-Mount-Anschluss?*
- *Welche maximale Freiheit hast du für Objekte zwischen Objektiv und Tubuslinse?*

**Messung / Quantifizierung**
- *Berechne und verifiziere die Gesamtvergrößerung $M = f_\text{TL} / f_\text{Obj}$ für drei verschiedene Tubuslinsen-Brennweiten.*
- *Wie misst du die Vergrößerung mit einem Strichraster (USAF-Target), und stimmt sie mit der Rechnung überein?*

**Variation**
- *Wie groß ist das Bildfeld (in µm × µm) auf dem 1/2"-Sensor bei 10× vs. 5× Gesamtvergrößerung?*
- *Welche Vergrößerung ist für Überblicks-Scans geeignet, welche für Detailaufnahmen?*

**Fehleranalyse**
- *Was tust du, wenn das Bild an den Rändern unscharf ist (Verzeichnung, Abbildungsfehler der CCTV-Tubuslinse)?*

**Physikalischer Hintergrund**
- *Wie leitet man aus dem Strahlengang her, dass $M = f_\text{TL}/f_\text{Obj}$ gilt?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: Welche Tubuslinsen-Brennweite ergibt eine Vergrößerung von 20×, sodass sie dem Olympus-Standard (180 mm) entspricht?*

- → `experiments/02_tubuslinse_vergroesserung.md`

### 3. Industriekamera in Betrieb nehmen

**Einstieg / Phänomen**
- *Was zeigt die Kamera im Live-Bild, bevor und nachdem du Belichtungszeit und Gain richtig eingestellt hast?*
- *Warum ist monochrom oft besser als Farbe für wissenschaftliche Mikroskopie?*

**Aufbau**
- *Wie installierst du den HIK-MVS-Treiber oder bindest die Kamera in ImSwitch ein?*
- *Wie sicherst du den C-Mount-Anschluss, ohne die Tubuslinse zu verkippen?*

**Messung / Diagnose**
- *Wie liest du Pixel-Auflösung, Bit-Tiefe, Sensorformat (1/2") und Pixelgröße (2.9 µm) aus der Kamera-Software?*
- *Wie überprüfst du mit einem homogenen Leuchtfeld (Flat-Field), ob der Sensor gleichmäßig empfindlich ist?*

**Variation**
- *Wie verändert sich das Signal-Rausch-Verhältnis, wenn du Gain von 0 auf Maximum erhöhst?*
- *Was zeigt sich im Differenzbild (Dunkelstrom-Offset), wenn du die Kamera mit geschlossenem Deckel aufnimmst?*

**Fehleranalyse**
- *Was tust du, wenn die Kamera nicht erkannt wird (USB-3 vs. USB-2 Problematik, fehlender Treiber)?*
- *Wie behebst du horizontale Streifen im Bild (Rolling-Shutter-Artefakte bei fluoreszierender Probe)?*

**Physikalischer Hintergrund**
- *Wie funktioniert ein CMOS-Sensor auf Pixel-Ebene (Photodiode, Quanteneffizienz, Read-out-Rauschen)?*

**Alltagsbezug / Differenzierung**
- *Sek II / Vertiefung: Berechne theoretische Detektionsschwelle (SNR = 1) für die Kamera bei gegebener QE und Photonenzahl.*

- → `experiments/03_industriekamera.md`

### 4. Vergrößerung quantitativ kalibrieren

**Einstieg / Phänomen**
- *Wie viele Pixel breit ist ein 10-µm-Strich auf dem Objektmikrometer – und stimmt das mit der berechneten Vergrößerung überein?*

**Aufbau**
- *Wie legst du ein Strichraster (USAF-Target oder Millimeter-Objektträger) auf den Probenhalter?*
- *Wie richtest du das Bild waagerecht aus, bevor du misst?*

**Messung / Quantifizierung**
- *Wie lautet die Kalibration in µm/Pixel, und wie trägst du sie in Fiji/ImageJ ein?*
- *Wie groß ist das Sichtfeld (Field of View) in µm bei deiner aktuellen Konfiguration?*

**Variation**
- *Wie ändert sich die Kalibration, wenn du die Tubuslinse wechselst oder näher an die Kamera verschiebst?*
- *Wie kontrollierst du die Wiederholbarkeit: Miss denselben Strich zehnmal und berechne die Standardabweichung.*

**Fehleranalyse**
- *Warum liefert eine nicht-senkrechte Kamera-Ausrichtung (Tilt) einen systematischen Kalibrierungsfehler?*

**Physikalischer Hintergrund**
- *Was ist Verzeichnung (Barrel vs. Kissen), und wie korrektierst du sie in Fiji mit dem „Distortion Correction"-Plugin?*

**Alltagsbezug / Erweiterung**
- *Wie kalibrieren kommerzielle Mikroskopsysteme (Zeiss ZEN, Leica LAS) automatisch und wozu dient ein NIST-zertifiziertes Strichraster?*

- → `experiments/04_kalibrierung.md`

### 5. Iris-Blende, Numerische Apertur, Auflösung

**Einstieg / Phänomen**
- *Was siehst du im Bild, wenn du die Iris bis auf ein kleines Loch schließt – heller oder dunkler, schärfer oder unschärfer?*
- *Kannst du am USAF-Target ablesen, welche Liniengruppe du noch auflöst vs. welche verschwimmt?*

**Aufbau**
- *Wie setzt du die SK23-Iris in den Beleuchtungspfad, und an welcher Position hat sie den größten Effekt?*

**Messung / Quantifizierung**
- *Miss die NA deines 10×-Objektivs (NA 0.25): Wie viele µm entsprechen dem Abbe-Limit $d = \lambda/(2\cdot\text{NA})$ bei 550 nm?*
- *Wie viele Linienpaare/mm erkennst du am USAF-Target bei vollständig geöffneter vs. halb geschlossener Iris?*

**Variation**
- *Wie wirkt sich das Schließen der Aperturblende auf Schärfentiefe und Kontrast aus (Abbe-Trade-off)?*
- *Was passiert, wenn du das 4×-Objektiv (NA 0.1) nimmst – wie ändert sich die erreichbare Auflösung?*

**Fehleranalyse**
- *Warum kann auch ein hochauflösendes Objektiv schlechte Bilder liefern, wenn die Beleuchtungs-NA kleiner ist als die Detektions-NA?*

**Physikalischer Hintergrund**
- *Leite die Abbe-Formel $d = \lambda/(2\cdot\text{NA})$ aus dem Beugungsargument her.*
- *Was ist die Rayleigh-Kriterium-Variante und wie unterscheidet es sich von Abbe?*

**Alltagsbezug / Differenzierung**
- *Sek I: Erkläre intuitiv, warum ein größeres Linsensystem besser auflöst.*
- *Sek II / Vertiefung: Berechne die Auflösung für NA 0.25, 0.45 und 1.25 (Öl) bei λ = 488 nm und trage sie tabellarisch auf.*

- → `experiments/05_blende_aufloesung.md`

### 6. Bildaufnahme, Speicherung, einfache Analyse

**Einstieg / Phänomen**
- *Was geht verloren, wenn du ein TIFF-Bild als JPEG speicherst – und woran erkennst du es im Histogramm?*
- *Welche Bildanalyse-Software ist kostenlos und in der Wissenschaft Standard?*

**Aufbau / Software**
- *Wie konfigurierst du ImSwitch für verlustfreie TIFF-Aufnahmen?*
- *Wie öffnest du das Bild in Fiji/ImageJ und siehst die Metadaten (Pixelgröße, Bit-Tiefe)?*

**Messung / Quantifizierung**
- *Wie misst du eine Struktur in µm in Fiji nach der Kalibrierung (Measure → Length)?*
- *Wie erstellst du einen Intensitätsprofil-Plot entlang einer Linie?*

**Z-Stack**
- *Wie nimmst du einen Z-Stack auf: Motor-Schrittweite festlegen, Stack-Anzahl, automatisches Speichern?*
- *Wie projizierst du den Z-Stack (Maximum Intensity Projection) in Fiji?*

**Fehleranalyse**
- *Was tust du bei Zitter-Artefakten im Z-Stack (Motor-Vibration, thermische Drift)?*

**Alltagsbezug / Erweiterung**
- *Welche weiteren Analyse-Schritte sind typisch in der Forschung: Segmentierung, Partikel-Tracking, Kolokalisierung?*
- *Sek II / Vertiefung: Schreibe ein Fiji-Makro, das automatisch einen Z-Stack aufnimmt und die Max-Projection speichert.*

- → `experiments/06_aufnahme_analyse.md`

## Cube-Module

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| HIK USB3 Mono-Kamera (IMX179) | Detektion | `modules/camera_hik_imx179.md` |
| 100 mm CCTV-Tubuslinse (C-Mount) | Tubuslinse | `modules/tube_lens_100_cctv.md` |
| 10× Infinity-Objektiv (RMS) | Mikroskop-Objektiv | `modules/objective_inf_10x.md` |
| SK23 Iris-Blende | Apertur / Beleuchtungs­steuerung | `modules/iris_sk23.md` |

## Didaktische Anker

- Übergang Schul- zu Forschungs­optik.
- Begriffe NA, Auflösung, Modulationstransfer praktisch erfahrbar.
- Software-Pipeline (Treiber → Capture → Analyse) als Realweltkette.

## Offene Fragen / TODO

- Vergleichstabelle Smartphone vs. Industriekamera.
- Empfohlene Standardproben (USAF-Target, Diatomeen).
- Eigene Seite für Treiberinstallation pro OS.
