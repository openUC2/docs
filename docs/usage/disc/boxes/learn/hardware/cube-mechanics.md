# Cube-Mechanik – Öffnen, Drehen, Montieren, Reinigen

> **Diataxis:** Tutorial (Einsteiger\*innen) + Reference (Nachschlagen)

---

## Steckbrief

| | |
|---|---|
| **Gilt für** | Alle Cube-Typen aller Discovery-Boxen |
| **Werkzeug** | M3-Inbusschlüssel (mitgeliefert) |
| **Zeitaufwand** | < 2 min pro Cube |
| **Sicherheitshinweis** | Optische Flächen nie mit bloßen Fingern berühren |

---

## 1. Wie ist ein Cube aufgebaut?

*Was steckt in der Box, die ich in der Hand halte?*

Ein Standard-Cube besteht aus:

- **Außengehäuse** – 50×50×50 mm, Aluminium-Druckguss oder POM-Kunststoff. Vier Seiten haben M3-Gewinde für Schrauben; zwei Seiten (Lichteintritt / Lichtaustritt) sind offen oder verglaset.
- **Insert** – das aktive Element (Linse, Spiegel, Stage, LED …). Es sitzt im Inneren und wird durch die Gehäuseschrauben fixiert.
- **Deckelplatten** – halten das Insert in Position. Bei einfachen Linsencubes übernehmen Halteclips diese Aufgabe; bei mechanisch aufwendigeren Inserts gibt es Schrauben.

```
┌────────────────────────┐
│  Außengehäuse (50 mm)  │
│  ┌──────────────────┐  │
│  │     Insert       │  │
│  └──────────────────┘  │
│           ▼            │
│   (Licht tritt hier    │
│    ein und aus)        │
└────────────────────────┘
```

---

## 2. Cube öffnen (Tutorial)

*Wann öffne ich einen Cube? Wenn ich das Insert tauschen, reinigen oder justieren möchte.*

### Schritt 1 – Cube hinlegen

Lege den Cube mit einer Seite auf einer weichen Unterlage ab. Die optische Achse zeigt seitlich weg.

### Schritt 2 – Schrauben lösen

Löse mit dem mitgelieferten M3-Inbusschlüssel die vier Schrauben auf der Außenseite um **nicht mehr als 2 Umdrehungen**. Du musst sie nicht herausdrehen – nur soweit lockern, dass das Insert lose wird.

### Schritt 3 – Insert entnehmen

Kippe den Cube leicht, das Insert fällt heraus. **Nicht schütteln** – bei Linsencubes kann das Insert klappern und die optische Fläche beschädigen.

### Schritt 4 – Insert tauschen oder reinigen

Setze das neue (oder gereinigte) Insert ein. Achte auf die **Orientierungspfeile** oder die **abgeflachte Kante** am Insert – sie zeigen an, welche Richtung die optische Achse ist (→ Abschnitt 3).

### Schritt 5 – Schrauben gleichmäßig festziehen

Ziehe die vier Schrauben im **Kreuz­muster** gleichmäßig an. Nicht zu fest – M3 in Aluminium dreht sich bei ca. 0,5 Nm durch.

---

## 3. Insert drehen (Orientierung ändern)

*Warum? Bei Spiegeln, Beamsplittern und Linsen mit Orientierung (z. B. Zylinderlinse) ist die Drehrichtung im Strahlengang entscheidend.*

### Orientierungsmarkierungen

Jedes Insert hat mindestens eine Markierung:

| Markierung | Bedeutung |
|---|---|
| Pfeil „→" | Lichtaustritts­richtung; dieser Pfeil zeigt in Richtung des nächsten Cubes |
| Abgeflachte Kante | „Oben" in der Standardorientierung |
| Farbpunkt | Herstellerspezifisch; ggf. im Modul-Datenblatt nachschlagen |

### Schritte

1. Cube öffnen (s. o.).
2. Insert herausnehmen.
3. Insert um 90° oder 180° drehen.
4. Erneut einsetzen und Cube schließen.
5. Visuell prüfen: Zeigt der Pfeil in die gewünschte Richtung?

---

## 4. Cube in eine Baseplate einsetzen

*Baseplates (Puzzle oder Solid) halten Cubes in definierten Raster­positionen.*

### Puzzle-Baseplate

- Cubes werden **von oben eingedrückt**. Die Stifte rasten hörbar ein.
- Herausnehmen: Cube **schräg kippen** und nach oben ziehen; nie senkrecht reißen.
- Verbindung: mehrere Puzzle-Baseplates stecken an den Rändern zusammen (wie Lego-Platten).

### Solid-Baseplate (POM, 10 mm)

- Cubes werden über **M3-Schrauben von unten** fixiert. Für vibrations­empfindliche Setups (LightSheet, ODMR) empfohlen.
- Flexibler Umbau: einfach Schrauben lösen, Cube verschieben, neu fixieren.

---

## 5. Optische Flächen reinigen

*Wann? Wenn Staub, Fingerabdrücke oder Kondensation auf der Linse/dem Spiegel sichtbar sind.*

| Verschmutzung | Methode |
|---|---|
| Staub | Druckluft­blasebalg oder weiche Antistatic-Bürste. **Nie pusten** – Speichel hinterlässt Rückstände. |
| Fingerabdruck | Linsenpapier (mitgeliefert) + 1 Tropfen optisches Reinigungsmittel (Isopropanol 99 %). Kreisförmig von innen nach außen wischen. |
| Öl / Schmierfett | Wie Fingerabdruck, ggf. 2–3 Wischvorgänge. |

> **Niemals Küchenrolle, Taschentuch oder normales Papier verwenden** – diese verkratzen Beschichtungen.

---

## 6. Häufige Fehler

| Fehler | Folge | Vermeidung |
|---|---|---|
| Insert falsch herum eingesetzt | Strahlengang gespiegelt oder blockiert | Orientierungspfeil prüfen |
| Schraube zu fest angezogen | Gehäuse verzogen, Insert eingeklemmt, Linse unter Stress | Kreuz­muster, max. 0,5 Nm |
| Cube schütteln beim Öffnen | Insert fällt heraus, optische Fläche beschädigt | Langsam kippen |
| Puzzle-Baseplate senkrecht abziehen | Rastnasen brechen | Schräg kippen |

---

## 7. Weiterführende Links

- [cube-design-inserts.md](cube-design-inserts.md) – eigene Inserts konstruieren
- [baseplates.md](baseplates.md) – Baseplates im Detail
- UC2-Hardware-Repository (GitHub): CAD-Dateien aller Standardinserts
