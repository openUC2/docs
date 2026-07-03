# Eigene Cube-Inserts entwerfen

> **Diataxis:** How-To (konkrete Aufgabe) + Reference (Maße)
> **Zielgruppe:** Maker, Industrie, Entwickler\*innen, Forschende – alle mit 3D-Drucker und Grundkenntnissen in CAD oder OpenSCAD/FreeCAD.

---

## Wann brauche ich ein eigenes Insert?

*Leitfragen: Welchen Anwendungsfall deckt kein Standard-Insert ab? Will ich eine eigene Linse, einen Sensor, ein Probenhalter-Sonderformat oder einen Aktor integrieren?*

Beispiele aus der Community:
- Halter für eine nicht-standardisierte Linse (z. B. 40 mm Durchmesser statt 25 mm)
- Probenhalter für Mikrotiterplatten
- Integrierter Temperatursensor für Inkubations-Experimente
- Custom-Strahlteiler für eine andere Wellenlänge

---

## 1. Maße und Toleranzen (Reference)

| Parameter | Wert | Hinweis |
|---|---|---|
| Cube-Innenmaß | 49,0 × 49,0 × 49,0 mm | Nach Druckschrumpfung ca. 49,2–49,4 mm → Insert muss Spiel haben |
| Insert-Außenmaß (Standard) | 48,0 × 48,0 × (variabel) mm | 0,5 mm Spiel auf jeder Seite |
| Optische Achse (Mitte) | 25,0 mm ab Cube-Boden | Gilt für alle Puzzle-Baseplate-Setups |
| Schrauben­abstand (Gehäuse) | 40 mm Lochkreis | M3, 4 Schrauben |
| Lichtapertur (offen) | ø 20 mm | Standard; anpassbar je nach Insert |
| RMS-Gewinde (Objektiv) | 0,8"-36 UNS | Nur für Objektivinserts |
| C-Mount | 1"-32 UNS | Nur für Kamera-/Tubuslinsencubes |

> **CAD-Referenz:** Alle Maßzeichnungen und STEP-Dateien sind im UC2-Toolbox-Repository auf GitHub verfügbar (`openUC2/UC2-GIT`).

---

## 2. Schritt-für-Schritt: Insert entwerfen (How-To)

### Schritt 1 – Vorlage laden

*Leitfragen: Welche CAD-Software nutze ich? Habe ich Erfahrung mit FreeCAD, Fusion 360, OpenSCAD oder Onshape?*

Empfehlung: **FreeCAD** (OpenSource) oder **Fusion 360** (kostenlos für Bildung).

1. Repository klonen: `git clone https://github.com/openUC2/UC2-GIT`
2. Ordner `CAD/CUBE_INSERT/` öffnen.
3. Vorlage `CUBE_INSERT_TEMPLATE.FCStd` (FreeCAD) laden.

### Schritt 2 – Vorlage anpassen

*Leitfragen: Was soll ins Insert? Welche Bohrungen, Schnitte, Gewinde brauche ich?*

- Das Template enthält bereits die korrekten Außenmaße und Montagebohrungen.
- Füge deine eigene Geometrie im Inneren hinzu (Bohrung für Linse, Haltenase, …).
- Beachte: Die optische Achse liegt bei Y = 25 mm ab Unterkante.

### Schritt 3 – STL exportieren

1. In FreeCAD: `Datei → Exportieren → STL`.
2. Qualität: 0,1 mm Abweichung (reicht für FDM).
3. Dateiname-Konvention: `UC2_INSERT_<Kurzname>_v<Version>.stl`

### Schritt 4 – Drucken

| Parameter | Empfehlung | Begründung |
|---|---|---|
| Material | PETG | Dimensionsstabiler als PLA; kein Warping bei ABS |
| Schicht­höhe | 0,2 mm | Gutes Detail für Einrastnasen |
| Füllung | 20–30 % | Reicht für mechanische Stabilität |
| Supports | Nur wenn nötig | Vermeiden an optischen Lichtöffnungen |
| Toleranz-Offset | +0,2 mm auf Außenmaße | Kompensiert Drucküberhang |

### Schritt 5 – Montieren und Testen

1. Insert in Cube einlegen (s. [cube-mechanics.md](cube-mechanics.md)).
2. Optisch prüfen: Liegt die optische Achse mittig?
3. Mechanisch prüfen: Insert sitzt spielfrei, ohne zu klemmen.
4. Falls nötig: Maße iterativ anpassen (±0,1 mm).

---

## 3. Design-Checkliste

Vor dem Drucken:

- [ ] Außenmaß ≤ 48,0 mm auf allen Seiten?
- [ ] Optische Öffnung auf der richtigen Achse (Y = 25 mm)?
- [ ] Montagebohrungen passend (M3, 40 mm Lochkreis)?
- [ ] Orientierungsmarkierung (Pfeil oder abgeflachte Kante) vorhanden?
- [ ] STL in mm exportiert (nicht cm!)?
- [ ] Gedrucktes Insert bei Raumtemperatur abgekühlt, bevor gemessen wird?

---

## 4. Beitragen (Community)

Gut getestete Inserts können ins UC2-Repository beigetragen werden:

1. Fork von `openUC2/UC2-GIT`.
2. Insert unter `CAD/CUBE_INSERT/<Kurzname>/` ablegen (CAD + STL + `README.md`).
3. Pull Request mit kurzer Beschreibung: Zweck, getestetes Material, verwendete Box.

---

## 5. Weiterführende Links

- [cube-mechanics.md](cube-mechanics.md) – Insert einbauen
- [baseplates.md](baseplates.md) – Welche Baseplate passt zum Setup?
- UC2-GIT Repository: CAD, Vorlagen, Community-Inserts
