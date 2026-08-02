# Hardware – Cube-System (box-übergreifend)

> Dieses Dokument ist **box-übergreifend**: Es gilt für alle Discovery-Boxen und richtet sich an alle Zielgruppen – von Schüler\*innen bis hin zu Industrieingenieur\*innen. Es ist primär **Reference** mit Tutorial-Abschnitten für Einsteiger\*innen.

## Was sind Cubes?

Ein **Cube** ist das physische Grundelement aller openUC2-Setups. Jeder Cube ist ein 50×50×50 mm³ großes Aluminium- oder Kunststoffgehäuse, das ein optisches oder mechanisches **Insert** aufnimmt. Cubes werden über kompatible **Baseplates** zu beliebigen optischen Systemen zusammengesteckt.

Das Prinzip: *Ein Cube = Eine Funktion.* Tausche das Insert, ändere die Funktion.

## Seiten in diesem Abschnitt

| Datei | Inhalt | Diataxis-Typ | Zielgruppe |
|---|---|---|---|
| [cube-mechanics.md](cube-mechanics.md) | Öffnen, Drehen, Reinigen, Montieren | Tutorial + Reference | Alle |
| [cube-design-inserts.md](cube-design-inserts.md) | Eigene Inserts entwerfen & drucken | How-To + Reference | Maker, Industrie, Entwickler\*innen |
| [baseplates.md](baseplates.md) | Puzzle-Baseplate, Solid-Baseplate, Maße | Reference | Alle |
| `cubes/` | Ein File pro Cube-Typ (Linse, Spiegel, …) | Reference | Fortgeschrittene |

## Cube-Kategorien

| Kategorie | Beispiele | Erster Einsatz |
|---|---|---|
| Optische Passive | Linsen, Spiegel, Beamsplitter, Filter | CoreBox |
| Optische Aktive | LED-Array, Laser-Modul, Fiber-Launcher | Electronics / Fluorescence |
| Mechanische Stage | Z-Stage (manuell / motorisiert), XYZ | CoreBox / Electronics |
| Kamera / Detektion | Smartphone-Halter, USB3-Kamera | CoreBox / Infinity |
| Probenhalterung | Sample-Mount, Probenkammer | CoreBox / LightSheet |
| Elektronik | ESP32-Board 2×2, Iris | Electronics |
| Quantenoptik | Kinetischer Spiegel, PBS, Polarisator | QBox |

---

*Details zu jedem Cube-Typ: siehe `cubes/<slug>.md` bzw. die `modules/`-Ordner in den einzelnen Box-Ordnern. Die `cubes/`-Dateien hier sind die box-unabhängige Referenz; die `modules/`-Dateien in den Box-Ordnern enthalten den konkreten Einsatzkontext.*
