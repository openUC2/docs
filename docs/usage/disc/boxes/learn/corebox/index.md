# CoreBox – Lernpfad

> **Status:** Skeleton. Quelle für Komponenten: [corebox.md](../../corebox.md). Quelle für Didaktik: [Didaktikkonzept CoreBox - Version 1 (1).md](../../Didaktikkonzept%20CoreBox%20-%20Version%201%20%281%29.md).

Die CoreBox ist der Einstieg in alle Discovery-Boxen. Sie deckt die geometrische Optik vollständig ab – von der Lupe bis zum Smartphone-Mikroskop – und ist Voraussetzung für Electronics, Infinity, Fluorescence und LightSheet.

## Lernpfad (empfohlen)

```
Lupe ─► Linsen ─► Projektor ─► Galilei-Teleskop ─► Kepler-Teleskop
                                                       │
                                                       ▼
                                Endlich-Mikroskop ─► Unendlich-Mikroskop ─► Smartphone-Mikroskop
```

## Experimente

Jeder Eintrag folgt dem [Experiment-Template](../templates/experiment.md). Solange ein Experiment noch keine eigene Datei hat, dient der Abschnitt hier als Sammelort für Notizen und Leitfragen.

### 1. Lupe (Tutorial-Einstieg)

**Einstieg / Phänomen**
- *Was passiert, wenn du ein Objekt langsam näher an die Linse heranbewegst – ab wann wechselt es von vergrößert zu unscharf?*
- *Welches allägliche Werkzeug nutzt dasselbe Prinzip (Leseglas, Uhrmacherlupe, Handylens)?*

**Aufbau**
- *Welche Teile brauchst du für die einfachste Lupe, und wie setzt du sie in den Cube ein?*
- *An welcher Position muss das Objekt relativ zur Linse sitzen, damit du ein aufrechtes virtuelles Bild siehst?*

**Messung / Quantifizierung**
- *Wie findest du die Brennweite einer unbekannten Linse mit Hilfe eines Schirms und einer Lichtquelle?*
- *Wie berechnet sich die Winkelvergrößerung $M = 250\,\text{mm} / f$, und was bedeutet „25 cm Nahpunktabstand"?*

**Variation**
- *Was beobachtest du, wenn du die Linse gegen eine mit f = 100 mm oder f = 25 mm austauschst?*
- *Wie ändert sich das Gesichtsfeld, wenn du die Pupille näher an die Linse hältst?*

**Fehleranalyse**
- *Wann und warum entsteht chromatische Aberration (Farbrand), und bei welcher Linsenform ist sie stärker?*
- *Warum ist das Bild am Rand schärfer als in der Mitte (oder umgekehrt) – was ist sphärische Aberration?*

**Physikalischer Hintergrund**
- *Wie beschreibt die Abbildungsgleichung $\frac{1}{f} = \frac{1}{b} - \frac{1}{g}$ (für das virtuelle Bild) den Sachverhalt?*

**Alltagsbezug / Differenzierung**
- *Sek I: Erkläre, warum eine Lupe vergrößert, mit einer selbst gezeichneten Strahlenkonstruktion.*
- *Sek II / Vertiefung: Bestimme die Brennweite durch Messung von drei Objekt-Bild-Abstandspaaren und trage $1/g$ gegen $1/b$ auf.*

- → Datei: `experiments/01_lupe.md` (noch anzulegen)

### 2. Sammel- vs. Zerstreuungslinsen

**Einstieg / Phänomen**
- *Was passiert mit einem Lichtstrahl, der parallel zur optischen Achse auf eine Sammellinse trifft – und was bei einer Zerstreuungslinse?*
- *Hältst du eine −50-mm-Linse vor eine Lichtquelle: Wo entsteht das Bild, und warum kann es nicht auf einem Schirm erscheinen?*

**Aufbau**
- *Wie unterscheiden sich die Randformen der +50-mm- und der −50-mm-Linse visuell, und was schließt man daraus?*
- *Wie setzt du beide Linsen hintereinander in Cubes, um den Parallelstrahl zu testen?*

**Messung / Quantifizierung**
- *Wie bestimmst du die Brennweite der Sammellinse direkt (Schirmmethode) und die der Zerstreuungslinse indirekt (Kombination mit bekannter Sammellinse)?*
- *Welche kombinierte Brennweite ergibt sich aus $1/f_\text{ges} = 1/f_1 + 1/f_2$ für +50 mm und −50 mm?*

**Variation**
- *Was siehst du, wenn du eine +50-mm- vor eine −50-mm-Linse schaltest – ist das System konvergent oder divergent?*
- *Ändert sich etwas, wenn du die Reihenfolge der Linsen vertauschst?*

**Fehleranalyse**
- *Warum liegt das Bild einer Sammellinse bei weißem Licht nicht exakt in einem Punkt (chromatische Aberration)?*

**Physikalischer Hintergrund**
- *Erkläre mithilfe des Brechungsgesetzes, warum eine Randkante dicker Linsen den Strahl zur Mitte hin bricht.*
- *Was bedeutet Diopter als Maß: $D = 1/f[\text{m}]$?*

**Alltagsbezug / Differenzierung**
- *Sek I: Welche Linsenform steckt in einer Lesebrille, welche in einem Brillenglas für Kurzsichtige?*
- *Sek II / Vertiefung: Leite die Linsenmacherformel her und erkläre den Einfluss der Krümmungsradien.*

- → `experiments/02_linsen.md`

### 3. Projektor

**Einstieg / Phänomen**
- *Wann entsteht auf einem Schirm ein scharfes, reelles, umgekehrtes Bild – und wann nicht?*
- *Was ist der Unterschied zwischen dem Bild im Zimmerprojektor und dem in einer Lupe?*

**Aufbau**
- *Welche Komponenten (Lichtquelle, Dia/Maske, Linse, Schirm) brauchst du, und in welcher Reihenfolge?*
- *Wie weit muss das Objekt (Maske) von der Linse entfernt sein, damit das Bild auf dem 50-cm-Schirm scharf ist?*

**Messung / Quantifizierung**
- *Miss Objekt- und Bildweite, und überprüfe $\frac{1}{f} = \frac{1}{g} + \frac{1}{b}$ quantitativ.*
- *Wie groß ist der Abbildungsmaßstab $\beta = b/g$, und wie ändert er sich beim Verschieben des Schirms?*

**Variation**
- *Was passiert, wenn du eine Kondensorlinse vor die Lichtquelle setzt – warum wird das Bild heller?*
- *Wie beeinflusst eine Lochblende (kleines Loch statt Linse) Schärfe und Helligkeit?*

**Fehleranalyse**
- *Woran erkennst du unscharfes Bild durch falsche Objekt- vs. Bildweite, und wie korrigierst du es?*
- *Warum zeigt weißes Licht am Bildrand Farbsäume?*

**Physikalischer Hintergrund**
- *Wie beschreibt die Linsengleichung den Übergang von $g > 2f$ (verkleinertes Bild) über $g = 2f$ (1:1) zu $f < g < 2f$ (vergrößertes Bild)?*

**Alltagsbezug / Differenzierung**
- *Sek I: Zeichne den Strahlengang für drei ausgezeichnete Strahlen (Parallelstrahl, Brennpunktstrahl, Mittelpunktstrahl).*
- *Sek II / Vertiefung: Berechne die nötige Linsenbrennweite für einen Kino-Projektor (Bildschirm 10 m, Dia 35 mm).*

- → `experiments/03_projektor.md`

### 4. Galilei-Teleskop

**Einstieg / Phänomen**
- *Wie stark vergrößert das Galilei-Teleskop, wenn du aus dem Fenster schaust?*
- *Warum steht das Bild aufrecht – und bei Kepler auf dem Kopf?*

**Aufbau**
- *Welche zwei Linsen (welche Brennweiten) brauchst du, und wie groß ist der Abstand?*
- *Wie veränderst du den Abstand, um ein scharfes Bild für dein Auge zu erzeugen (Akkommodation)?*

**Messung / Quantifizierung**
- *Wie berechnet sich die Vergrößerung $M = -f_\text{Obj} / f_\text{Ok}$ aus den Brennweiten?*
- *Miss den Abstand zwischen Objektiv und Okular bei Scharfstellung auf Unendlich.*

**Variation**
- *Was ändert sich, wenn du Okular und Objektiv vertauschst?*
- *Welche Vergrößerung erreichst du maximal mit den vorhandenen Linsen?*

**Fehleranalyse**
- *Warum ist das Gesichtsfeld (Sehfeld) des Galilei-Teleskops kleiner als das des Kepler-Teleskops?*
- *Was bedeutet „Vignettierung", und wann tritt sie auf?*

**Physikalischer Hintergrund**
- *Wie erklärt das Strahlendiagramm (zwei Brennebenen zusammenfallen) das aufrechte Bild?*

**Alltagsbezug / Differenzierung**
- *Sek I: Nenne drei Geräte, die das Galilei-Prinzip nutzen (Oper, Theater, Fernglas-Typ).*
- *Sek II / Vertiefung: Leite die Vergrößerungsformel aus dem Strahlendiagramm her.*

- → `experiments/04_galilei_teleskop.md`

### 5. Kepler-Teleskop

**Einstieg / Phänomen**
- *Warum dreht das Kepler-Teleskop das Bild um – und warum akzeptieren Astronomen das?*
- *Kannst du mit dem Kepler einen Zwischenbildpunkt erzeugen und ihn auf einem Papier sehen?*

**Aufbau**
- *Welche zwei Sammellinsen brauchst du, und wie lang ist das Tubus-System?*
- *Wo genau liegt das Zwischenbild, und wie kannst du es durch Verschieben zeigen?*

**Messung / Quantifizierung**
- *Miss die Vergrößerung durch Vergleich: Halte beide Augen offen und schätze ab.*
- *Berechne die Vergrößerung aus den Brennweiten und vergleiche mit deiner Messung.*

**Variation**
- *Was passiert mit Vergrößerung und Sehfeld, wenn du das Okular gegen ein kürzeres (f = 25 mm) tauschst?*
- *Wie baust du aus dem Kepler-Teleskop mit einer dritten Linse ein terrestrisches Teleskop (aufrechtes Bild)?*

**Fehleranalyse**
- *Warum wird das Bild bei zu starker Vergrößerung dunkel und unscharf?*
- *Was bewirkt es, die Austrittspupille nicht mit der eigenen Pupille zur Deckung zu bringen?*

**Physikalischer Hintergrund**
- *Erkläre den Unterschied zwischen Austrittspupille, Sehfeld und Dämmerungszahl als teleskopische Kenngrößen.*

**Alltagsbezug / Differenzierung**
- *Sek I: Wo wird das Kepler-Prinzip genutzt (Astro-Fernrohr, Marine-Fernrohr mit Umkehrlinse)?*
- *Sek II / Vertiefung: Berechne die nötige Öffnung, um den Jupiterdurchmesser von 50 Bogensekunden auf 1° zu vergrößern.*

- → `experiments/05_kepler_teleskop.md`

### 6. Endlich-korrigiertes Lichtmikroskop

**Einstieg / Phänomen**
- *Wie viel größer erscheint eine Zelle, wenn du durch das 4×-Objektiv mit dem Okular schaust?*
- *Was siehst du anders als beim Smartphone-Foto derselben Probe?*

**Aufbau**
- *Welche Teile bauen Beleuchtung, Objektiv, Zwischenbild und Okular auf?*
- *Wie positionierst du die Z-Stage, um den Fokus zu finden?*

**Messung / Quantifizierung**
- *Wie groß ist die Gesamt-Vergrößerung (Objektiv × Okular)?*
- *Wie misst du die effektive Vergrößerung mit einem Linienraster oder Maßstab?*

**Variation**
- *Was ändert sich im Bild, wenn du den Beleuchtungsabstand variierst (kritische vs. Köhler-artige Beleuchtung)?*
- *Wie wirkt eine Lochblende statt der Taschenlampe?*

**Fehleranalyse**
- *Woran erkennst du, dass Objekt, Objektiv und Okular nicht auf derselben Achse sitzen?*
- *Warum erscheint das Bild eines endlich-korrigierten Objektivs unscharf, wenn du einen Filter in den Strahlengang bringst?*

**Physikalischer Hintergrund**
- *Was bedeutet „fixe Tubuslänge 160 mm", und wie hängt das mit der Korrektionsoptik im Objektiv zusammen?*
- *Welche Grenzen setzt die numerische Apertur (NA 0.1) der Auflösung (Abbe-Formel)?*

**Alltagsbezug / Differenzierung**
- *Sek I: Zeichne den zweistufigen Strahlengang (Objektiv → Zwischenbild → Okular → Auge).*
- *Sek II / Vertiefung: Warum kann ein endliches Objektiv keinen Filter ohne Bildversatz aufnehmen – leite es geometrisch her.*

- → `experiments/06_mikroskop_endlich.md`

### 7. Unendlich-korrigiertes Lichtmikroskop

**Einstieg / Phänomen**
- *Was siehst du, wenn du das Infinity-Objektiv ohne Tubuslinse vor eine Probe hältst – und warum gibt es kein Bild?*
- *Woran merkst du im Alltag, dass moderne Mikroskope „infinity-corrected" sind (modulare Filterblöcke)?*

**Aufbau**
- *Welche Reihenfolge haben Objektiv, freier paralleler Raum und Tubuslinse?*
- *Wie groß darf der Abstand zwischen Objektiv und Tubuslinse sein, ohne das Bild zu verschlechtern?*

**Messung / Quantifizierung**
- *Wie beeinflusst die Wahl der Tubuslinsen-Brennweite (100 mm vs. 50 mm) die Gesamtvergrößerung?*
- *Miss und berechne: Wenn das Objektiv auf $f_\text{Obj}$ ausgelegt ist und die Tubuslinse $f_\text{TL}$ hat, wie lautet die Vergrößerung $M = f_\text{TL}/f_\text{Obj}$?*

**Variation**
- *Schiebe einen Farbfilter in den parallelen Strahl – ändert sich die Bildlage?*
- *Was passiert, wenn du die Tubuslinse schräg stellst?*

**Fehleranalyse**
- *Warum erscheint das Bild unscharf, wenn du ein endliches Objektiv mit einem Infinity-Tubus kombinierst?*

**Physikalischer Hintergrund**
- *Was bedeutet „hintere Brennebene des Objektivs liegt im Unendlichen", und warum vereinfacht das die Konstruktion modularer Mikroskope (z. B. Filter, Strahlteiler, DIC-Prismen)?*

**Alltagsbezug / Erweiterung**
- *Wie nutzen kommerzielle Mikroskop-Marken (Zeiss, Leica, Nikon) unterschiedliche Standard-Tubuslängen (200 mm / 160 mm / 180 mm)?*
- *Sek II / Vertiefung: Berechne den Strahlengang für eine Kombination aus 10×/NA 0.25-Objektiv und 100-mm-Tubuslinse auf einem 1/2"-Sensor.*

- → `experiments/07_mikroskop_unendlich.md`

### 8. Smartphone-Mikroskop

**Einstieg / Phänomen**
- *Was siehst du auf deinem Handybildschirm, wenn du die Probe fokussierst – was fehlt im Vergleich zum Okular?*
- *Warum reicht das Smartphone-Objektiv allein nicht aus, um Zellen zu zeigen?*

**Aufbau**
- *Wie setzt du Objektiv-Cube, Probenhalter, Taschenlampe und Smartphone-Halter zusammen?*
- *Wie richtest du das Smartphone aus, damit sein Objektiv mit der optischen Achse fluchtet?*

**Messung / Quantifizierung**
- *Wie kalibrierst du die Vergrößerung mit einem Linienraster (Millimeterpapier oder Strichplatte)?*
- *Wie rechnest du Pixel in Mikrometer um, wenn du die Pixelgröße deines Sensors kennst?*

**Variation**
- *Was ändert sich, wenn du auf den 10×-Objektivblock wechselst?*
- *Wie beeinflusst die Beleuchtungsfarbe (weißes vs. blaues Licht) den Kontrast biologischer Proben?*

**Fehleranalyse**
- *Warum erscheint das Bild am Rand dunkler als in der Mitte (Vignettierung durch Smartphone-Linse)?*
- *Wann „säubert" die automatische HDR-Funktion das Bild, und warum ist das für wissenschaftliche Aufnahmen problematisch?*

**Physikalischer Hintergrund**
- *Wie funktioniert ein CMOS-Bildsensor auf Pixelebene, und warum ist Quantenrauschen bei wenig Licht relevant?*

**Alltagsbezug / Differenzierung**
- *Sek I: Dokumentiere eine selbst gesammelte Probe (Blütenstaub, Salzkristall) mit Foto und Beschriftung.*
- *Sek II / Vertiefung: Vergleiche Signal-Rausch-Verhältnis und Dynamikbereich des Smartphones mit der Industrie­kamera aus dem Infinity Add-On.*

- → `experiments/08_smartphone_mikroskop.md`

### Exkurs: Einen Würfel auseinanderbauen

**Aufbau und Mechanik**
- *Welche Schrauben löst du in welcher Reihenfolge, ohne das Insert zu beschädigen?*
- *Welche Werkzeuge (Inbus-Schlüssel, weiche Unterlage) brauchst du?*
- *Wie erkennst du die Ausrichtungsmarkierung, und was passiert, wenn du sie ignorierst?*

**Beobachten und Verstehen**
- *Was siehst du im Inneren des Cubes – Schienen, Klemmsystem, optische Flächen?*
- *Wie ist das Insert gefertigt (3D-Druck, Spritzguss) und wo sitzt es im Cube?*

**Variation / Kreativität**
- *Kannst du das Insert um 90° rotieren, und welche neue Funktion hat der Cube dann?*
- *Wie entwirfst du ein eigenes einfaches Insert (z. B. Filterhalter) nach dem Demontage-Verständnis?*

**Fehleranalyse**
- *Welche typischen Montagefehler entstehen beim Wiedereinbauen (verkippt, zu fest, optische Achse versetzt)?*

**Physikalischer Hintergrund**
- *Was ist Toleranz in der Optik, und warum müssen Insert-Maße auf ±0.1 mm genau sein?*

**Alltagsbezug / Erweiterung**
- *Wie gehen professionelle Hersteller (z. B. Thorlabs, Newport) bei modularen optischen Systemen mit denselben Herausforderungen um?*

- → `experiments/exkurs_cube.md`

## Cube-Module der CoreBox

Quelle: Komponentenliste in [corebox.md](../../corebox.md). Jeder Eintrag folgt dem [Modul-Template](../templates/module.md).

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| 45°-Spiegel (fest, frontbeschichtet) | Strahlumlenkung 90° | `modules/mirror_45_fixed.md` |
| 50 mm Linse | Kurzbrennweite, Lupe, Okular | `modules/lens_50.md` |
| 100 mm Linse | Tubuslinse, Projektor | `modules/lens_100.md` |
| −50 mm Linse | Zerstreuungslinse (Galilei) | `modules/lens_minus50.md` |
| Okular | Visuelle Beobachtung | `modules/eyepiece.md` |
| Smartphone-Halter (universal) | Bildaufnahme via Handy | `modules/smartphone_carrier.md` |
| Probenhalter | Aufnahme Objektträger | `modules/sample_mount.md` |
| Z-Stage (manuell, 25 mm) | Fokussierung | `modules/z_stage_manual.md` |
| Objektiv 4× / NA 0.1 (endlich) | Mikroskop-Objektiv | `modules/objective_4x.md` |
| Taschenlampe | Beleuchtung Durchlicht | `modules/torch.md` |

## Didaktikkonzept

Bestehend, sehr ausführlich: [Didaktikkonzept CoreBox - Version 1 (1).md](../../Didaktikkonzept%20CoreBox%20-%20Version%201%20%281%29.md).

Migrationsplan: Inhalte abschnittsweise in `concept.md` übernehmen, sobald die Struktur stabil ist.

## Offene Fragen / TODO

- Bildmaterial pro Experiment vereinheitlichen (Foto + Strahlengang-Skizze).
- Arbeitsblätter und Lösungsblätter als separate Dateien.
- Lehrplan-Mapping je Bundesland (Anhang in `concept.md`).
