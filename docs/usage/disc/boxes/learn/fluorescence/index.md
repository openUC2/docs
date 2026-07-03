# Fluorescence Add-On – Lernpfad (LED & Laser)

> **Status:** Skeleton. Quellen: [fluoled.md](../../fluoled.md), [fluolaser.md](../../fluolaser.md). **Voraussetzung:** CoreBox + Electronics + Infinity Add-On.

Das Fluorescence Add-On gibt es in zwei Varianten:

- **LED-Edition** – einfacher, sicherer (480 nm Hochleistungs-LED, keine Laserschutz-Vorgaben).
- **Laser-Edition** – höhere Brillanz und Kohärenz (488 nm fasergekoppelt, ~35 mW, TTL).

Beide nutzen denselben Strahlteiler-Cube (Dichroit + Emissionsfilter) und dasselbe Detektions­konzept; sie unterscheiden sich in Beleuchtung und Beam-Shaping.

## Lernpfad

```
Was ist Fluoreszenz? ─► Dichroit & Filter verstehen ─► Anregung aufbauen (LED oder Laser)
                                                                   │
                                                                   ▼
                                Köhler-Beleuchtung ─► Erste Fluoreszenz-Probe ─► Spektrale Sauberkeit prüfen
```

## Experimente

### 1. Fluoreszenz sichtbar machen (Demo)

**Einstieg / Phänomen**
- *Was siehst du, wenn du einen Textmarker-Strich unter normalem Licht und unter UV-/Blaulicht vergleichst?*
- *Welche Farbe hat das emittierte Licht im Vergleich zur Anregungsfarbe – und warum ist es immer langwelliger?*

**Physikalischer Hintergrund**
- *Was ist der Jablonski-Energieniveauplan, und welche Übergänge (Absorption, interne Relaxation, Emission) finden dort statt?*
- *Was beschreibt der Stokes-Shift quantitativ – Wellenlängen- vs. Energiedifferenz?*

**Variation**
- *Vergleiche die Fluoreszenz von Fluorescein, Rhodamin und GFP in Lösung: Farbe, Helligkeit, Abklingzeit.*
- *Was passiert, wenn du die Anregungsintensität verdoppelst – verdoppelt sich auch das Signal?*

**Alltagsbezug**
- *Welche Alltagsanwendungen nutzen Fluoreszenz: Geldschein-Sicherheitsmerkmale, Waschmittel-Aufheller, Diagnostik-Streifen?*
- *Was ist GFP (Green Fluorescent Protein), und warum bekam es den Nobelpreis 2008?*

**Fehleranalyse**
- *Warum leuchtet die Probe im Durchlicht kaum, aber durch den Dichroit-Cube stark?*
- *Wie erkennst du, dass Streulicht der Anregungsquelle und nicht echte Fluoreszenz beobachtet wird?*

**Differenzierung**
- *Sek I: Beobachte und beschreibe qualitativ – welche Stoffe fluoreszieren, welche nicht?*
- *Sek II / Vertiefung: Berechne die Stokes-Verschiebung in nm und in eV für Fluorescein (Anregung 480 nm, Emission 520 nm).*

- → `experiments/01_fluoreszenz_demo.md`

### 2. Dichroit und Emissionsfilter im Strahlengang

**Einstieg / Phänomen**
- *Halte den Dichroit gegen das Raumlicht: Welche Farbe siehst du in Reflexion, welche in Transmission?*
- *Was würde passieren, wenn du den Dichroit weglässt – könnte das Kameraobjektiv beschädigt werden?*

**Aufbau**
- *In welche Richtung wird der Dichroit eingebaut (45° zur Achse), und wo sitzt der Emissionsfilter?*
- *Wie verifizierst du die korrekte Einbaurichtung ohne Laser (z. B. mit einer LED-Taschenlampe)?*

**Messung / Quantifizierung**
- *Miss die Sperrtiefe (OD): Wie viel Anregungslicht (480 nm) lässt der Emissionsfilter durch (qualitativ mit dem Auge)?*
- *Wie ändert sich der Hintergrund (ohne Probe) mit und ohne Emissionsfilter?*

**Variation**
- *Was siehst du, wenn du Anregungs- und Emissionsfilter vertauschst?*
- *Welche Auswirkung hat die Neigung des Dichroits von 45° auf die Wellenlängen-Cut-off-Position?*

**Fehleranalyse**
- *Wie erkennst du Streulicht-Durchschlag im Bild (heller Hintergrund ohne Fluorophor)?*
- *Was tust du, wenn das Fluoreszenz-Signal sehr schwach ist (falsche Filterposition, zu niedrige Anregungsintensität)?*

**Physikalischer Hintergrund**
- *Wie funktioniert ein dichroitischer Spiegel auf Basis von Dünnschicht-Interferenz?*
- *Was bedeutet OD4 Sperrwirkung – welchen Faktor beschreibt das?*

- → `experiments/02_dichroit_filter.md`

### 3a. Anregung mit Hochleistungs-LED (FluoBox LED)

**Einstieg / Phänomen**
- *Wie hell ist die 480-nm-LED im Vergleich zur gewöhnlichen Taschenlampe – und warum braucht sie eine Asphäre?*
- *Was passiert mit dem Strahl, wenn du die Asphäre entfernst?*

**Aufbau**
- *Wie setzt du LED-Cube, Anregungsfilter und Kollimations-Asphäre zusammen?*
- *Wo sitzt die Iris, und welche Rolle spielt sie für die Köhler-Beleuchtung?*

**Messung / Quantifizierung**
- *Wie gleichmäßig ist das Beleuchtungsfeld (Flat-Field-Messung mit homogener Probe)?*
- *Wie regulierst du die LED-Intensität (PWM-Duty-Cycle) über die REST-API?*

**Variation**
- *Wie verändert das Schließen der Iris das Gesichtsfeld und den Streulicht-Anteil?*
- *Vergleiche Signal-Hintergrund-Verhältnis bei 30 %, 60 %, 100 % LED-Leistung.*

**Fehleranalyse**
- *Was tust du, wenn das Beleuchtungsfeld Ringe oder Flecken zeigt (Staub auf Asphäre, Dejustage)?*

**Sicherheit**
- *Darf man direkt in die 480-nm-LED blicken – was sagen die Sicherheitsregeln für blaues Licht?*

**Physikalischer Hintergrund**
- *Was ist der Unterschied zwischen kollimiertem Licht (Asphäre) und kritischer Beleuchtung (Probe direkt beleuchtet)?*

- → `experiments/03a_anregung_led.md`

### 3b. Anregung mit fasergekoppeltem Laser (FluoBox Laser)

**Einstieg / Phänomen**
- *Warum ist der Laserstrahl viel schmaler und heller als der LED-Strahl bei gleicher Eingangsleistung?*
- *Was siehst du am Faserausgang, wenn du ihn nicht kollimierst (divergentes Kegel-Licht)?*

**Aufbau / Justage**
- *Wie positionierst du den Fiber-Launcher so, dass die Faser-Endfläche in der hinteren Brennebene der 18-mm-Linse liegt?*
- *Wie erkennst du ein sauber kollimiertes Bündel (Strahlprofil, Divergenz)?*

**Messung / Quantifizierung**
- *Wie mächtig ist der kollimierte Strahl im Objektiv-Rückstrahl – mit einem Leistungsmessgerät?*
- *Wie justierst du die TTL-Modulation (Ein/Aus) des Lasers über das ESP32-Board?*

**Sicherheit**
- *Welche Laserklasse hat der 488-nm-Laser mit ~35 mW – und welche Schutzbrille ist Pflicht?*
- *Wie beschilderst du den Arbeitsplatz, und wann musst du alle anwesenden Personen informieren?*

**Variation**
- *Wie ändert sich das Fluoreszenz-Bild (Helligkeit, Bleaching-Rate) im Vergleich zur LED-Edition?*

**Fehleranalyse**
- *Was tust du, wenn der Fiber-Launcher kein Licht durchlässt (Stecker nicht gereinigt, Faser beschädigt)?*

**Physikalischer Hintergrund**
- *Was ist Laserkohärenz, und warum führt sie zu Speckle-Rauschen im Fluoreszenzbild?*

- → `experiments/03b_anregung_laser.md`

### 4. Köhler-Beleuchtung im Fluoreszenzmikroskop

**Einstieg / Phänomen**
- *Was siehst du im Bild, bevor und nachdem du die Köhler-Justage durchgeführt hast?*
- *Welches klassische Merkmal zeigt eine nicht-Köhler-beleuchtete Probe (Filamentschatten im Bild)?*

**Aufbau / Justage**
- *Welche Schritte führst du der Reihe nach durch: Kondensor-, Aperturblende-, Feldblende-Position?*
- *Wie erkennst du anhand der Feldblenden-Schärfe, dass die Justage stimmt?*

**Messung / Quantifizierung**
- *Wie homogen ist die Beleuchtung nach der Justage? Miss das Intensitätsprofil über das Bildfeld.*
- *Wie viel Streulicht-Hintergrund bleibt, wenn du Aperturblende schließt vs. öffnest?*

**Variation**
- *Was verändert sich, wenn du die Aperturblende zu weit schließt (Beugungsartefakte, erhöhter Kontrast)?*
- *Vergleiche Köhler- mit kritischer Beleuchtung bei derselben Fluoreszenz-Probe.*

**Fehleranalyse**
- *Was tun, wenn das Bild nach der Justage noch ungleichmäßig ist (Dejustage der Asphäre, verschmutzte Optik)?*

**Physikalischer Hintergrund**
- *Warum erzeugt Köhler-Beleuchtung einen kohärenzreduzierten, gleichmäßigen Beleuchtungskegel im Objekt?*

**Alltagsbezug**
- *Welche kommerziellen Mikroskop-Marken haben eine fest eingebaute Köhler-Justage-Konfiguration?*

- → `experiments/04_koehler.md`

### 5. Erste Fluoreszenz-Probe abbilden (GFP, Fluoresceine, Pollen)

**Einstieg / Phänomen**
- *Welche Probe leuchtet sofort, welche braucht mehr Anregungsintensität?*
- *Wie sieht eine Fluorescein-Lösung vs. ein fixierter Pollen-Objektträger im Bild aus?*

**Aufbau**
- *Wie präparierst du eine einfache Fluorescein-Probe auf einem Objektträger?*
- *Wie findet man den Fokus – erst Durchlicht, dann Fluoreszenz?*

**Messung / Quantifizierung**
- *Wie bestimmst du Signal-Hintergrund-Verhältnis (SNR) aus dem Histogramm?*
- *Wie wählst du Belichtungszeit und Gain optimal (kein Überbelichten, kein Rauschen)?*

**Variation**
- *Wie verändert sich das Bild bei verschiedenen Objektiv-Vergrößerungen (4× vs. 10×)?*
- *Was passiert mit dem SNR, wenn du die Probe in Wasser statt Luft beobachtest?*

**Fehleranalyse**
- *Was tust du, wenn du nur Hintergrund siehst (kein Signal): Probe falsch präpariert, Filter falsch, LED aus?*
- *Wie erkennst du Überbelichtung, und was tust du dagegen?*

**Alltagsbezug / Erweiterung**
- *Wie werden GFP-markierte Organismen in der biologischen Forschung präpariert und lebendig abgebildet?*
- *Sek II / Vertiefung: Miss die Fluoreszenz-Intensität als Funktion der Fluorescein-Konzentration (Lambert-Beer im Fluoreszenz-Regime).*

- → `experiments/05_erste_probe.md`

### 6. Bleaching und Phototoxizität

**Einstieg / Phänomen**
- *Wie verändert sich das Fluoreszenz-Signal in einem Zeitraffer-Video über 5 Minuten bei konstanter Beleuchtung?*
- *Was siehst du, wenn du nach einem Bleach-Experiment die Beleuchtung kurz unterbrichst – erholt sich das Signal?*

**Messung / Quantifizierung**
- *Wie schnell fällt die Intensität ab (Halbwertszeit)? Passe eine exponentielle Kurve an.*
- *Wie ändert sich die Bleaching-Rate, wenn du die Intensität halbierst?*

**Variation**
- *Welche Anti-Bleaching-Reagenzien (DABCO, ProLong Gold) verlängern die Lebensdauer messsbar?*
- *Wie unterscheidet sich Bleaching bei LED- vs. Laser-Beleuchtung?*

**Fehleranalyse**
- *Wie unterscheidest du Bleaching von Probendrift (fokus oder xy-Versatz)?*

**Physikalischer Hintergrund**
- *Was passiert chemisch beim Photobleaching (reaktive Sauerstoffspezies, kovalente Modifikation des Fluorophors)?*
- *Was ist FRAP (Fluorescence Recovery After Photobleaching), und warum ist Bleaching dort ein Feature?*

**Alltagsbezug / Erweiterung**
- *Warum bleichen Farben an Textilien und Gemälden aus – ist das derselbe Mechanismus?*

- → `experiments/06_bleaching.md`

### 7. Spektrale Trennung prüfen

**Einstieg / Phänomen**
- *Wie sieht das Bild aus, wenn du den Emissionsfilter entfernst – was ändert sich am Hintergrund?*
- *Kannst du mit dem bloßen Auge den Unterschied zwischen Anregungs-Streulicht und echtem Fluoreszenzsignal erkennen?*

**Aufbau / Messung**
- *Wie testest du qualitativ mit einer Weißlicht-LED, ob der Filter die Anregungswellenlänge (480 nm) sperrt?*
- *Wie bestimmst du quantitativ die Sperrwirkung mit dem Kamera-Histogramm (Probe ohne Fluorophor)?*

**Variation**
- *Was passiert, wenn du Anregungs- und Emissionsfilter durch Filter mit versetzten Cut-off-Wellenlängen ersetzt?*
- *Wie sieht das Bild aus, wenn du zwei Fluorophore (z. B. Fluorescein + Rhodamin) gleichzeitig anregst – gibt es Übersprechung (Crosstalk)?*

**Fehleranalyse**
- *Wie erkennst du Streulicht-Durchschlag (helles Rauschen im Hintergrund trotz Filter)?*
- *Was tust du, wenn der Hintergrund nicht gleichmäßig schwarz ist (Reflexionen, Kamera-Dunkelstrom)?*

**Physikalischer Hintergrund**
- *Was bedeutet OD (Optische Dichte) als Maß für Filterdämpfung, und wie berechnet man die Transmission daraus?*

**Alltagsbezug / Erweiterung**
- *Wie werden Multispektral- und Hyperspektral-Detektoren in der Konfokal-Mikroskopie und der Satelliten-Fernerkundung eingesetzt?*

- → `experiments/07_spektrale_trennung.md`

## Cube-Module

### Gemeinsam (beide Editionen)

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| Beamsplitter-Cube (Dichroit + EM-Filter) | Trennung Anregung / Emission | `modules/beamsplitter_dichroic.md` |

### LED-Edition

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| 480 nm Hochleistungs-LED + Asphäre | Anregung | `modules/led_480.md` |
| Anregungsfilter | Spektrale Reinigung der LED | `modules/excitation_filter.md` |

### Laser-Edition

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| 488 nm fasergekoppelter Laser (~35 mW, TTL) | Anregung | `modules/laser_488_fc.md` |
| Fiber Launcher | FC/PC → Cube | `modules/fiber_launcher.md` |
| 18 mm Linse | Faser-Kollimation | `modules/lens_18.md` |

## Didaktische Anker

- Brücke Optik ↔ Biologie / Chemie.
- Konkretes Beispiel für *frequenzselektive* Optik (Filter, Dichroit).
- Kontrast Sicherheit & Performance: LED vs. Laser als bewusste Wahl.

## Offene Fragen / TODO

- Standard-Probenset für Schulen definieren (Fluorescein-Lösung, fixierte Pollen, …).
- Lasersicherheits-Merkblatt als Anhang.
- Vergleichs­experiment „dieselbe Probe mit LED vs. Laser".
