# Electronics Add-On – Lernpfad

> **Status:** Skeleton. Quelle: [electronics.md](../../electronics.md). **Voraussetzung:** CoreBox.

Das Electronics Add-On bringt Bewegung und programmierbare Beleuchtung in das CoreBox-System: ein ESP32-basiertes Board, eine motorisierte Z-Stage (NEMA 11, < 1 µm) und ein LED-Array für digitale Kontrasttechniken.

## Lernpfad

```
Inbetriebnahme ESP32 ─► Motor-Z-Stage manuell ─► PS4-Controller / Joystick
                                                        │
                                                        ▼
                           LED-Array Beleuchtung ─► Software (ImSwitch / Python) ─► Autofokus
```

## Experimente

### 1. Inbetriebnahme der Elektronik

**Einstieg / Phänomen**
- *Was passiert, wenn du den ESP32 per USB anschließt – welche LEDs leuchten, was erscheint im seriellen Monitor?*
- *Welche Sicherheitsregeln (12 V Netzteil, Kurzschluss, ESD) solltest du kennen, bevor du anfängst?*

**Aufbau**
- *Wie verbindest du ESP32-Board, TMC2209-Treiber und LED-Array im Cube-System?*
- *Welche Kabel und Stecker brauchst du (USB-C, JST, Netzteil-Buchse)?*

**Firmware flashen**
- *Wie flashst du die UC2-eSP-Firmware über PlatformIO oder den UC2-Installer?*
- *Wie überprüfst du die Firmware-Version im seriellen Monitor?*

**Messung / Diagnose**
- *Welchen HTTP-Endpunkt (z. B. `/motors`) oder seriellen Befehl nutzt du, um den Motor und die LEDs zu testen?*
- *Wie erkennst du im seriellen Log einen fehlerhaften Treiber vs. falsches Kabel?*

**Fehleranalyse**
- *Was tust du, wenn der Rechner den ESP32 nicht erkennt (Treiber, COM-Port, Kabel-Typ)?*
- *Wie reagierst du auf einen Motor, der zuckt aber nicht dreht (Strom zu niedrig, Schrittmodus falsch)?*

**Erweiterung**
- *Wie öffnest du die ImSwitch-Oberfläche und bindest das Board als UC2-REST-Gerät ein?*

- → `experiments/01_inbetriebnahme.md`

### 2. Motorisierte Z-Stage – erste Bewegungen

**Einstieg / Phänomen**
- *Wie viele Schritte braucht die Stage, um 1 mm zu fahren – und was hörst du dabei?*
- *Was siehst du im Live-Bild, wenn du die Stage zu schnell verfahrst (Vibrations-Blur)?*

**Aufbau**
- *Wie montierst du NEMA-11-Motor, Spindel und Gleiter in den Z-Stage-Cube?*
- *Wie schließt du die Motorkabel sicher an den TMC2209-Slot an?*

**Messung / Quantifizierung**
- *Wie viele Mikrometer pro Schritt ergibt sich aus Spindelsteigung (z. B. 1 mm/U) und Microstepping (1/16)?*
- *Miss die tatsächliche Verfahrstrecke mit einem Messschieber und vergleiche mit dem Sollwert.*

**Variation**
- *Wie ändert sich das Geräusch, wenn du von 1/4 auf 1/16 Microstepping wechselst?*
- *Was passiert mit Bildschärfe und Geräusch, wenn du den Strom am Treiber erhöhst oder senkst?*

**Fehleranalyse**
- *Woran erkennst du Backlash (Loses Spiel in der Spindel), und wie kompensierst du ihn in Software?*
- *Was tun, wenn die Stage an den Endlagen schleift – gibt es einen Software-Endschalter?*

**Physikalischer Hintergrund**
- *Wie funktioniert ein Schrittmotor (Magnetpole, Spulensequenz), und was ist der Unterschied zwischen Vollschritt und Microstepping?*

**Alltagsbezug / Erweiterung**
- *Wo werden Schrittmotoren mit Sub-Mikrometer-Präzision eingesetzt (Halbleiterfertigung, MRT-Bett, 3D-Drucker)?*

- → `experiments/02_zstage_motorisiert.md`

### 3. Steuerung per PS4-Controller

**Einstieg / Phänomen**
- *Was passiert, wenn du den Joystick des Controllers leicht neigst vs. ganz durchdrückst – ändert sich die Geschwindigkeit?*
- *Welchen Vorteil hat haptisches Feedback (Vibration) beim Fokussieren im Unterricht?*

**Aufbau / Pairing**
- *Wie koppelst du den PS4-Controller per Bluetooth mit dem Rechner oder dem ESP32?*
- *Welche Software (ImSwitch, eigenes Skript) nimmt Joystick-Events entgegen?*

**Mapping**
- *Wie konfigurierst du, welcher Stick oder welche Taste welche Stage-Achse und welche Geschwindigkeit steuert?*
- *Wie sicherst du, dass ein versehentlicher Knopfdruck nicht in die Endlage fährt?*

**Variation**
- *Wie änderst du die Empfindlichkeit (µm/Joystick-Einheit)?*
- *Kannst du zusätzlich die LED-Array-Helligkeit per Trigger steuern?*

**Fehleranalyse**
- *Was tust du, wenn der Controller verbunden scheint, aber die Stage sich nicht bewegt (Treiber, Port-Konflikte)?*

**Alltagsbezug / Erweiterung**
- *Wie werden Gamepad-Controller in der Robotik (Fernerkundung, Chirurgie-Roboter) eingesetzt?*
- *Sek II / Vertiefung: Schreibe einen eigenen Joystick-Handler in Python (pygame oder evdev).*

- → `experiments/03_joystick_steuerung.md`

### 4. LED-Array & Hellfeld-/Dunkelfeld-Beleuchtung

**Einstieg / Phänomen**
- *Was siehst du im Bild, wenn nur die äußersten LEDs leuchten – und was, wenn nur die zentralen?*
- *Welche Probe profitiert von Dunkelfeld-Beleuchtung (z. B. transparente Diatomeen)?*

**Aufbau**
- *Wie setzt du das LED-Array so ein, dass es auf die hintere Brennebene des Objektivs abbildet?*
- *Welchen Abstand braucht das Array zum Objekt, um Kohler-ähnliche Beleuchtung zu erzielen?*

**Messung / Quantifizierung**
- *Wie misst du den Kontrast im Hellfeld- vs. Dunkelfeld-Bild (normierte Graustufendifferenz)?*
- *Wie hängt der Dunkelfeld-Ring-Radius mit der NA des Objektivs zusammen?*

**Variation**
- *Welche Muster (obere Halbkreis, untere Halbkreis, Diagonal) erzeugst du für DPC?*
- *Wie ändert sich der Kontrast transparenter Proben mit dem Beleuchtungsmuster?*

**Fehleranalyse**
- *Was tust du, wenn einzelne LEDs nicht leuchten (Adressierungsfehler, I²C-Timeout)?*

**Physikalischer Hintergrund**
- *Wie erklärt die Fourier-Optik, dass axiale Beleuchtung Strukturen anders betont als schiefe Beleuchtung?*

**Alltagsbezug / Erweiterung**
- *Welche Prinzipien des LED-Arrays findet man in Licht-Feld-Kameras und Computational Photography?*

- → `experiments/04_led_array.md`

### 5. Differential Phase Contrast (DPC)

**Einstieg / Phänomen**
- *Warum erscheinen transparente, ungefärbte Proben im Hellfeld fast unsichtbar – und wie hilft DPC?*
- *Was zeigt ein DPC-Bild im Vergleich zu einem normalen Hellfeldbild an denselben Zellen?*

**Aufbau / Software**
- *Welche vier Halbkreis-Muster (links, rechts, oben, unten) musst du nacheinander aufnehmen?*
- *Wie berechnest du das DPC-Bild: $\text{DPC}_\text{LR} = (I_L - I_R)/(I_L + I_R)$?*

**Messung / Quantifizierung**
- *Wie quantifizierst du das Phasengradient-Signal im Vergleich zum Hellfeldkontrast?*
- *Welche Ortsfrequenzen werden durch DPC besonders betont?*

**Variation**
- *Wie kombinierst du LR und TB-DPC zu einem Phasenbild?*
- *Was verändert sich bei unterschiedlichen Beleuchtungs-NAs?*

**Fehleranalyse**
- *Was tust du, wenn die vier Bilder nicht gleich hell sind (LED-Intensitätsungleichmäßigkeit)?*
- *Warum entstehen Artefakte an Probenkanten, und wie minimierst du sie?*

**Physikalischer Hintergrund**
- *Wie beschreibt die optische Transfer-Funktion (OTF) den Übergang von Phasenobjekt zu DPC-Bild?*

**Alltagsbezug / Erweiterung**
- *Welche Rolle spielt DPC in der computergestützten Pathologie und in Smartphone-Mikroskopen?*

- → `experiments/05_dpc.md`

### 6. Autofokus über Kontrastkurve

**Einstieg / Phänomen**
- *Wie sieht die Kontrastkurve über einen Z-Scan aus – hat sie eine klare Spitze oder ein breites Plateau?*
- *Warum funktioniert Kontrastautofokus nicht bei einer gleichmäßig grauen Probe?*

**Aufbau / Software**
- *Wie schreibst du einen Z-Scan-Loop: Motor schrittweise fahren, Bild aufnehmen, Metrik berechnen?*
- *Welche Schärfemetrik nutzt du (Varianz, Laplace-Varianz, Tenengrad), und warum?*

**Messung / Quantifizierung**
- *Wie breit ist die Schärfentiefe deines Objektivs in µm, und wie viele Schritte entsprechen ihr?*
- *Wie schnell ist dein Autofokus (Scans/s) im Vergleich zu einem kommerziellen System?*

**Variation**
- *Wie verbessert ein grob-fein-Suchalgorithmus die Geschwindigkeit?*
- *Wie wirkt sich Rauschen im Bild auf die Metrik und damit auf die Fokusgenauigkeit aus?*

**Fehleranalyse**
- *Was tun, wenn der Autofokus konsequent in einer Randzone festhängt (lokales Maximum)?*

**Physikalischer Hintergrund**
- *Was ist der Zusammenhang zwischen Schärfentiefe, NA und Wellenlänge: $\text{DOF} \approx \lambda / \text{NA}^2$?*

**Alltagsbezug / Erweiterung**
- *Wie funktioniert der Autofokus einer DSLR oder eines Handy-Kamerasystems (Phasendetektion, Kontrastdetektion)?*
- *Sek II / Vertiefung: Implementiere einen Hill-Climbing- und einen Golden-Section-Suchalgorithmus und vergleiche.*

- → `experiments/06_autofokus.md` *(setzt Infinity-Add-On voraus)*

### 7. Programmierung – Python / JavaScript

**Einstieg / Phänomen**
- *Was passiert, wenn du im Browser `http://<ESP32-IP>/motor?steps=100` aufrufst?*
- *Was ist der Unterschied zwischen HTTP-REST und seriellem JSON-Protokoll?*

**Aufbau / Entwicklungsumgebung**
- *Wie installierst du `pyserial` / `requests` und testest die Verbindung in einem Jupyter-Notebook?*
- *Wie ist die UC2-REST-API aufgebaut (Endpunkte für Motor, LED, Kamera)?*

**Schreibe dein erstes Skript**
- *Schreibe ein „Hello, Motor"-Skript: Fahre 500 Schritte vor, dann 500 zurück, und messe die Zeit.*
- *Wie steuerst du die LED-Array-Farbe per RGB-Wert über die REST-API?*

**Integration in ImSwitch**
- *Wie registrierst du das UC2-Board als Hardware-Gerät in der ImSwitch-Konfigurationsdatei?*
- *Wie schreibst du ein einfaches ImSwitch-Plugin, das einen Z-Scan auslöst?*

**Fehleranalyse**
- *Was tust du bei HTTP-Timeout-Fehlern – ist das WLAN instabil, oder hat der ESP32 einen Absturz?*

**Physikalischer Hintergrund / Informatik**
- *Was ist REST (Representational State Transfer), und warum ist es für IoT-Hardware gut geeignet?*

**Alltagsbezug / Erweiterung**
- *Wie automatisierst du einen vollständigen Scan-Workflow: Motor fahren → Bild aufnehmen → Datei speichern?*
- *Sek II / Vertiefung: Baue einen einfachen Feedback-Loop (Autofokus als geschlossener Regelkreis).*

- → `experiments/07_programmierung.md`

## Cube-Module / Komponenten

| Modul | Kurzbeschreibung | Datei |
|---|---|---|
| Z-Stage NEMA 11 (RMS, 25 mm) | Motorisierte Fokussierung | `modules/z_stage_motor.md` |
| LED-Array Cube | Adressierbare Beleuchtung | `modules/led_array.md` |
| UC2-Elektronik 2×2 Cube | ESP32-Board mit TMC2209-Slots | `modules/esp32_board.md` |
| Objektiv 10× / NA 0.25 (endlich) | Mikroskop-Objektiv | `modules/objective_10x.md` |
| Netzteil 12 V | Stromversorgung | `modules/psu_12v.md` |
| PS4-Controller (drahtlos) | Manuelle Steuerung | `modules/ps4_controller.md` |

## Didaktische Anker

- Brückenschlag zur Informatik (Programmierung, Steuerung).
- Konkrete Erfahrung mit Schrittmotoren, PWM, TTL, USB.
- Übergang vom „Bauen" (CoreBox) zum „Automatisieren" (Electronics).

## Offene Fragen / TODO

- Vereinheitlichte Firmware-Versionsangabe.
- Eigene Workshop-Einheit „Mein erstes Python-Mikroskop-Skript".
- Sicherheitshinweise zu 12 V / Motorabwärme.
