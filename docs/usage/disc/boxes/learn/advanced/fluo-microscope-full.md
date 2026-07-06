# Vollständiges Fluoreszenzmikroskop

> **Status:** Community-Build
> **Diataxis:** Tutorial + How-To + Explanation
> **Benötigte Boxen:** CoreBox + Electronics Add-On + Infinity Add-On + Fluorescence Add-On (LED oder Laser)
> **Zielgruppe:** Fortgeschrittene Schüler\*innen (Sek II), Hochschule, Forschung, Maker

---

## Steckbrief

| | |
|---|---|
| **Lernziel** | Ein vollständiges Epi-Fluoreszenz-Mikroskop aus Modulen zusammenbauen und verstehen |
| **Schlüsselbegriffe** | Epi-Fluoreszenz, Dichroit, Emissionsfilter, Köhler-Beleuchtung, Signal/Rausch-Verhältnis |
| **Dauer Aufbau** | ca. 45–60 min |
| **Sicherheit** | Laser-Edition: Laserschutzbrillen, Klasse-3B-Regeln; LED-Edition: keine besonderen Anforderungen |

---

## 1. Worum geht es? (Explanation)

### Was ist Epi-Fluoreszenz?

*Leitfragen: Warum kommen Anregungs- und Detektionslicht beim Epi-Aufbau auf derselben Seite? Was unterscheidet das vom Durchlicht-Aufbau beim LightSheet?*

…

### Warum ist das Fluoreszenzmikroskop in der Biologie so wichtig?

*Leitfragen: Welche Strukturen in Zellen kann man mit Fluoreszenz sichtbar machen, die im Hellfeld unsichtbar sind? Was ist GFP? Welchen Nobelpreis hat das gewonnen?*

…

---

## 2. Aufbau (Tutorial)

*Leitfragen: In welcher Reihenfolge baue ich den Strahlengang auf? Was ist der Vorteil, mit der Detektion zu beginnen und die Anregung zuletzt einzufügen?*

### Benötigte Komponenten

**CoreBox:**
- Puzzle-Baseplates (10×)
- Z-Stage (manuell)

**Electronics Add-On:**
- ESP32-Board
- Z-Stage (motorisiert, NEMA 11) – optional für Autofokus
- LED-Array – optional für Durchlicht-Übersicht

**Infinity Add-On:**
- 10×/NA 0.25 Infinity-Objektiv
- 100 mm CCTV-Tubuslinse
- HIK USB3-Kamera (IMX179)
- Iris SK23

**Fluorescence Add-On (LED oder Laser):**
- Dichroit-Beamsplitter-Cube (+ Emissionsfilter)
- 480 nm LED-Modul + Asphäre + Anregungsfilter *(LED-Edition)*
- 488 nm Faserlaser + Fiber-Launcher + 18 mm Linse *(Laser-Edition)*

### Strahlengang (schematisch)

```
Lichtquelle (LED/Laser)
       │
       ▼
  Anregungsfilter
       │
       ▼
  Dichroit (Reflexion → Objektiv)
       │  ↑
       ▼  └──── emittiertes Fluoreszenzlicht (Transmission durch Dichroit)
   Objektiv                │
       │                   ▼
     Probe         Emissionsfilter
                           │
                           ▼
                      Tubuslinse
                           │
                           ▼
                        Kamera
```

### Schritt-für-Schritt

1. Infinity-Mikroskop ohne Fluoreszenz vollständig aufbauen und scharf stellen.
2. Durchlicht-LED-Array einschalten → Probe im Hellfeld fokussieren (leichter als direkt in Fluoreszenz).
3. Dichroit-Cube zwischen Objektiv und Tubuslinse einsetzen. Orientierung: Anregungsstrahl wird **reflektiert** → Richtung Probe; Fluoreszenz­emission wird **transmittiert** → Richtung Kamera.
4. Anregungs-Cube (LED oder Laser) auf der Seite des Dichroi einbauen. Beam entlang der Anregungsachse ausrichten.
5. Durchlicht abschalten. Anregung einschalten. Probe suchen.
6. Belichtungszeit auf Kamera anpassen (Fluoreszenz ist viel dunkler als Hellfeld: typisch 50–500 ms statt 1–10 ms).

---

## 3. Qualitätskontrolle und Optimierung (How-To)

### Wie erkenne ich ein gutes Fluoreszenzbild?

*Leitfragen: Wie sieht das Signal-Rausch-Verhältnis aus? Was sind typische Artefakte (Streulicht, Bleaching)?*

### Wie stelle ich Köhler-Beleuchtung ein?

→ Verweis auf `fluorescence/experiments/04_koehler.md` *(noch anzulegen)*

### Wie vergleiche ich LED- vs. Laser-Edition?

*Leitfragen: Gleiche Probe, gleiche Belichtungszeit. Wo ist der Unterschied in Helligkeit, Homogenität, Hintergrund?*

---

## 4. Troubleshooting

| Symptom | Ursache | Lösung |
|---|---|---|
| Kein Fluoreszenz­signal | Dichroit falsch orientiert | Reflektion muss in Richtung Probe zeigen |
| Sehr heller Hintergrund | Emissionsfilter fehlt oder falsch | Emissionsfilter prüfen, Streulicht abschirmen |
| Signal schwach | Belichtungszeit zu kurz, Verstärkung zu niedrig | Kameraeinstellungen anpassen |
| Bild unscharf | Fokus nicht auf Fluoreszenzebene | Hellfeld-Fokussierung vor Fluoreszenz |

---

## 5. Didaktische Einbettung

*Leitfragen: Für welche Unterrichtsform eignet sich dieses Setup? Ab wann ist es für Schüler\*innen sinnvoll (Sek II, Hochschulpraktikum)?*

- Sek II-Kontext: Nach CoreBox-Grundlagen und Infinity-Modul; als Krönung einer Projekt­woche.
- Hochschule: Als Praktikumsversuch zur Epi-Fluoreszenz (2–3 h).
- Forschung: Einstieg für Gruppen, die auf openUC2-Hardware umsteigen möchten.

---

## 6. Weiterführende Links

- [fluorescence/index.md](../fluorescence/index.md)
- [infinity/index.md](../infinity/index.md)
- `electronics/experiments/06_autofokus.md` *(noch anzulegen)* – motorisierter Autofokus für dieses Setup
