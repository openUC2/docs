# Abbe-Auflösungslimit demonstrieren

> **Status:** Prototyp
> **Diataxis:** Explanation + How-To
> **Benötigte Boxen:** CoreBox + Infinity Add-On (+ optional Electronics)
> **Zielgruppe:** Sek II, Hochschule, Forschung

---

## Steckbrief

| | |
|---|---|
| **Lernziel** | Verstehen, warum es eine physikalische Grenze für die optische Auflösung gibt |
| **Schlüsselbegriffe** | Abbe-Limit, Numerische Apertur, Beugung, Kohärenz, Raumfrequenz |
| **Dauer Aufbau** | ca. 30 min |
| **Sicherheitshinweis** | keine besonderen Anforderungen (keine Laser nötig) |

---

## 1. Worum geht es? (Explanation)

### Was ist das Abbe-Limit?

*Leitfragen: Warum kann man mit Licht nicht beliebig kleine Strukturen auflösen? Was hat das Beugungsbild damit zu tun?*

Ernst Abbe zeigte 1873, dass die minimale auflösbare Struktur $d$ eines Mikroskops von der **Wellenlänge** $\lambda$ und der **Numerischen Apertur** NA abhängt:

$$d = \frac{\lambda}{2 \cdot \text{NA}}$$

Das ist keine Geräteschranke, sondern eine **physikalische Fundamentalgrenze** – sie gilt unabhängig davon, wie gut die Optik gefertigt ist.

### Warum ist das wichtig?

*Leitfragen: Was bedeutet das für Biologie (Zellen, Viren), Halbleiterlithographie, Teleskope? Wie hat die STORM/STED-Nanoskopie dieses Limit umgangen?*

…

### Welches Modell beschreibt das?

*Leitfragen: Was ist die Fourier-Optik? Was ist der Zusammenhang zwischen dem Beugungsbild in der Brennebene und der Ortsfrequenz im Bild?*

…

---

## 2. Aufbau (How-To)

*Leitfragen: Wie wird ein Auflösungstest-Target (USAF 1951) in das Mikroskop gebracht? Wie wählt man das richtige Objektiv? Wie vergleicht man 10×/NA 0.1 vs. 10×/NA 0.25?*

### Benötigte Komponenten

- CoreBox: Z-Stage, Taschenlampe, Puzzle-Baseplates
- Infinity Add-On: 10×/NA 0.25 Objektiv, HIK-Kamera, Tubuslinse, Iris
- Optional: CoreBox Objektiv 4×/NA 0.1 (zum Vergleich)
- Target: USAF-1951-Testchart (Glasversion empfohlen, Papierausdruck als Notlösung)

### Aufbau-Schritte

1. Vollständiges Infinity-Mikroskop aufbauen (→ [infinity/experiments/01_endlich_vs_unendlich.md](../infinity/experiments/01_endlich_vs_unendlich.md)).
2. USAF-Target als Probe einlegen.
3. Grobe Fokussierung per Z-Stage.
4. Bild auf Kamera aufnehmen: Welche Liniengruppe ist noch aufgelöst?
5. Iris schrittweise schließen: NA sinkt → wie verändert sich die sichtbare Liniengruppe?
6. Objektiv wechseln (NA 0.1 statt 0.25): dieselbe Messung wiederholen.

---

## 3. Beobachtungs- und Auswertungsaufgaben

- Aufgabe A: Bestimme die kleinste aufgelöste Liniengruppe für NA 0.25 und NA 0.1. Stimmt das mit der Formel überein?
- Aufgabe B: Plotte Auflösung vs. NA. Ist der Zusammenhang linear?
- Aufgabe C: Schließe die Iris bis auf Minimum. Was passiert mit dem Kontrast? Mit der Auflösung?

---

## 4. Troubleshooting

| Symptom | Ursache | Lösung |
|---|---|---|
| Alle Liniengruppen unaufgelöst | Fokus falsch | Z-Stage feiner justieren |
| Bild sehr dunkel bei geschlossener Iris | Erwartet | Belichtungszeit erhöhen |
| Kein Unterschied NA 0.1 vs. 0.25 | Target-Qualität | Glasversion statt Papierausdruck verwenden |

---

## 5. Weiterführende Links

- Infinity Add-On → [infinity/experiments/05_blende_aufloesung.md](../infinity/experiments/05_blende_aufloesung.md)
- Theorie: Abbe (1873), Born & Wolf „Principles of Optics"
- Nanoskopie als Ausblick: Nobel­preis 2014 (Betzig, Hell, Moerner)
