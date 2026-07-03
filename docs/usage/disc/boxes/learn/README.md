# Discovery Boxes – Lern- und Lehrstruktur

> **Status:** Parallele Struktur zum schrittweisen Befüllen. Die bestehenden Shop-/Übersichtsseiten unter `docs/usage/disc/boxes/*.md` bleiben unverändert. Inhalte werden hierher migriert und ergänzt, sobald sie ausgearbeitet sind.

Diese Dokumentation strukturiert die openUC2 Discovery-Boxen nach dem [Diataxis-Framework](https://diataxis.fr/). Ziel ist, dass Schüler\*innen, Lehrkräfte, Technik-Interessierte und Forschende jeweils den passenden Einstieg finden – vom geführten Bauen einer Lupe bis zum Verständnis der Köhler-Beleuchtung.

---

## 1. Diataxis – Wie hängt die Struktur mit dem Framework zusammen?

Das Diataxis-Diagramm spannt zwei Achsen auf:

```
                        ACTION (doing)
                              │
          TUTORIALS           │        HOW-TO GUIDES
          (Learning)          │        (Goals)
                              │
  ────── Acquisition ─────────┼─────── Application ──────
                              │
          EXPLANATION         │        REFERENCE
          (Understanding)     │        (Information)
                              │
                        COGNITION (thinking)
```

**Jedes Dokument in dieser Struktur lässt sich auf einem dieser vier Felder einordnen.** Die Felder schließen sich nicht aus – ein Experiment-Dokument enthält bewusst alle vier Abschnitte, aber mit klarer Gewichtung:

| Diataxis-Typ | Achsen-Position | Wer liest es? | Wann? | Dokument-Typ hier |
|---|---|---|---|---|
| **Tutorial** | Action + Acquisition | Einsteiger\*innen, Schüler\*innen | Beim ersten Kontakt, geführt | `experiments/0N_*.md` → Abschnitt „Schritt-für-Schritt" |
| **How-To Guide** | Action + Application | Maker, Forschende, Lehrkräfte | Konkrete Aufgabe lösen | `experiments/0N_*.md` → Abschnitt „Experimentieren & Variieren"; `advanced/` |
| **Explanation** | Cognition + Acquisition | Alle, die verstehen wollen | Nach dem Experiment, oder als Vorbereitung | `experiments/0N_*.md` → Abschnitt „Hintergrund"; `concept.md` |
| **Reference** | Cognition + Application | Industrie, Forschung, Entwickler\*innen | Beim Nachschlagen | `modules/*.md`; `hardware/cubes/` |

### Konsequenz für die Dateihierarchie

```
Box-Ordner (z. B. corebox/)
│
├── index.md         → Übersicht + Lernpfad         (kein eigener Diataxis-Typ, Navigation)
├── concept.md       → Didaktik, Theorie             (Explanation-lastig)
├── experiments/     → pro Experiment eine Datei    (alle vier Typen in Abschnitten)
└── modules/         → pro Cube-Modul eine Datei    (Reference + kurze Explanation)
```

Die `hardware/`- und `advanced/`-Ordner (siehe unten) folgen derselben Logik, sind aber Box-übergreifend.

---

## 2. Vollständige Ordnerstruktur

```
learn/
├── README.md                        ← dieses Dokument (Navigation + Architektur-Entscheidungen)
│
├── templates/
│   ├── experiment.md                ← Vorlage: alle vier Diataxis-Abschnitte
│   ├── module.md                    ← Vorlage: Reference + Explanation
│   └── box-concept.md               ← Vorlage: Didaktikkonzept (Explanation)
│
├── hardware/                        ← Box-übergreifend; für Bildung UND Industrie
│   ├── index.md                     ← Einstieg: Was sind Cubes? Welche Kategorien?
│   ├── cube-mechanics.md            ← Wie öffnet/dreht/montiert man einen Cube?
│   ├── cube-design-inserts.md       ← Wie designt man eigene Inserts? (FreeCAD/OpenSCAD)
│   ├── baseplates.md                ← Puzzle-Baseplate- und Solid-Baseplate-Arten
│   └── cubes/                       ← ein File pro Cube (= modules/ in Box-Ordnern,
│       └── ...                         hier box-unabhängige Referenzdokumentation)
│
├── advanced/                        ← Setups, die mehrere Boxen kombinieren
│   ├── index.md                     ← Übersicht aller Multi-Box-/Nicht-Produkt-Setups
│   ├── abbe-setup.md                ← Abbe-Auflösungslimit-Setup (multi-box)
│   ├── fluo-microscope-full.md      ← Vollständiges Fluoreszenzmikroskop (CoreBox+Elec+Inf+Fluo)
│   └── ...                          ← weitere Setups nach Bedarf
│
├── i18n/                            ← Sprachstrategie-Dokument (kein Inhalt, nur Regeln)
│   └── README.md
│
├── corebox/
├── electronics/
├── fluorescence/
├── infinity/
├── lightsheet/
└── qbox/
```

Jeder Box-Unterordner enthält:

- `index.md` – Überblick, Lernpfad, Liste der Experimente/Module
- `concept.md` – Didaktikkonzept (analog zur CoreBox-Vorlage)
- `experiments/` – ein File pro Experiment, basierend auf `templates/experiment.md`
- `modules/` – ein File pro Cube-Modul, basierend auf `templates/module.md`

---

## 3. Aufbaulogik der Boxen (Produktpfad)

```
CoreBox  ──►  Electronics  ──►  Infinity  ──►  Fluorescence  ──►  LightSheet
(Optik)       (Motoren,       (Industrie-     (LED oder Laser,    (3D-Imaging,
              ESP32, LED)     Kamera,         Dichroit, Filter)   Zylinderlinse,
                              Tubuslinse)                          Probenkammer)
```

`QBox` ist eigenständig und nicht Teil des linearen Pfads.

**Multi-Box-Setups**, die mehrere dieser Produkte kombinieren oder noch kein eigenes Produkt sind, landen unter `advanced/` (→ Abschnitt 6).

---

## 4. Zielgruppen und Lesepfade

| Zielgruppe | Einstieg | Diataxis-Schwerpunkt |
|---|---|---|
| Schüler\*innen (Sek I) | CoreBox → `experiments/` → Tutorial-Abschnitte | Tutorial |
| Schüler\*innen (Sek II) | CoreBox → `experiments/` → Hintergrund + Aufgaben | Tutorial + Explanation |
| Lehrkräfte | `concept.md` → Stundenverläufe | Explanation + How-To |
| Maker / Hobbyisten | `hardware/` → Box-`index.md` → `experiments/` How-To | How-To + Reference |
| Industrie / Forschung | `hardware/cubes/` → Box-`modules/` | Reference + Explanation |
| Entwickler\*innen | `hardware/cube-design-inserts.md` + `dev/` | Reference + How-To |
| Fortgeschrittene (multi-box) | `advanced/` | How-To + Explanation |

---

## 5. Hardware-Dokumentation (box-übergreifend) {#hardware}

> Datei: [hardware/index.md](hardware/index.md)

Cube-Mechanik und -Design sind für **alle** Boxen und alle Zielgruppen relevant. Deshalb sind sie **außerhalb** der einzelnen Box-Ordner abgelegt. Das vermeidet Duplizierung und erlaubt es, dieselbe Seite in verschiedenen Kontexten zu verlinken:

- Eine Lehrkraft liest es kurz als „Wissenswertes zum System".
- Eine Industrieingenieurin nutzt es als technische Referenz.
- Ein Schüler liest den Tutorial-Abschnitt „Wie baue ich einen Cube zusammen?".

Die Datei `hardware/cube-mechanics.md` enthält:
- Wie öffnet man einen Cube (Schrauben, Magnete)?
- Wie dreht man ein Insert (Orientierungspfeile)?
- Wie reinigt man optische Flächen?
- Wie montiert man Baseplates (Puzzle vs. Solid)?

Die Datei `hardware/cube-design-inserts.md` enthält:
- Maß­toleranzen, Cube-Innenmaß (CAD-Referenz).
- Empfohlene Werkstoffe (PLA, PETG, Resin) und deren Vor-/Nachteile.
- Schritt-für-Schritt: FreeCAD → STL → Drucken → Montieren.
- Wo liegen Vorlagen? (Link zu UC2-Toolbox / GitHub).

---

## 6. Nicht-Produkt-Setups und Multi-Box-Experimente {#advanced}

> Datei: [advanced/index.md](advanced/index.md)

Einige Setups existieren bereits als Aufbauten, sind aber (noch) kein eigenständiges Produkt oder erfordern mehr als eine Box. Diese landen unter `advanced/` – nicht unter einer einzelnen Box, weil sie:

- mehrere Boxen kombinieren (und sonst doppelt erscheinen würden),
- noch kein stabiles Produktangebot haben (Status: Prototyp / Community),
- eher für fortgeschrittene Nutzer\*innen gedacht sind.

**Entscheidungsbaum: Wo lege ich ein Setup ab?**

```
Ist das Setup ein einzelnes Produkt?
├── Ja  ──► Box-eigener experiments/-Ordner
└── Nein
    ├── Kombiniert es genau zwei Boxen?
    │   ├── Ja  ──► advanced/ + Hinweis in beiden Box-index.md
    │   └── Nein (3+ Boxen oder Prototyp)  ──► advanced/
```

Aktuelle und geplante `advanced/`-Seiten:

| Datei | Setup | Benötigte Boxen | Status |
|---|---|---|---|
| `abbe-setup.md` | Abbe-Auflösungslimit demonstrieren | CoreBox + Infinity | Prototyp |
| `fluo-microscope-full.md` | Vollständiges Fluoreszenzmikroskop | CoreBox + Elec + Inf + Fluo | Community-Build |
| *(mehr nach Bedarf)* | | | |

---

## 7. Mehrsprachigkeit (i18n) {#i18n}

> Strategie-Dokument: [i18n/README.md](i18n/README.md)

### Ist-Stand im Repo

Das Repo unterstützt bereits Mehrsprachigkeit in Teilen (z. B. `archive/minibox/` hat `de/`, `en/`, `es/`, `fr/`, `ar/`, `it/`). Docusaurus selbst hat ein i18n-Plugin (`i18n/` im Projektstamm).

### Strategie für `learn/`

**Kurzfassung: Englisch first, Übersetzungen per Pull Request.**

| Schicht | Sprache | Begründung |
|---|---|---|
| Quellwahrheit (`learn/`) | **Englisch** | Größte Reichweite, einfachere Reviews, Konsistenz mit Industrie/Forschung |
| Deutsche Übersetzung | Priorität 1 | Kernzielgruppe Schulen DE/AT/CH; Didaktikkonzept bereits auf DE |
| Weitere Sprachen | Community-getrieben | Kein fester Zeitplan; PRs willkommen |

### Technische Umsetzung (Docusaurus)

```
i18n/
├── de/
│   └── docusaurus-plugin-content-docs/
│       └── current/
│           └── usage/disc/boxes/learn/   ← deutsche Übersetzungen hier
├── fr/
└── ...
```

Jede Übersetzungsdatei ist eine 1:1-Kopie der englischen Quelle mit übersetztem Text. Bilder und Dateinamen bleiben unverändert (Docusaurus-Konvention).

### Priorität pro Zielgruppe

- **Tutorial-Abschnitte** (Schüler\*innen) → immer übersetzen, beginnend mit DE.
- **Reference / module.md** → Englisch reicht; Fachbegriffe sind international.
- **concept.md** (Didaktik) → DE primär, dann EN als Übersetzung.
- **advanced/** → Englisch reicht für Forscher\*innen.

### Hinweis für Autor\*innen

> Schreibe zuerst auf Englisch. Wenn ein Inhalt auf DE entstehen soll (z. B. Stundenverläufe für Schulen), erstelle ihn in `i18n/de/` und verlinke die englische Entsprechung als „TODO: translate to EN".

---

## 8. Migrationshinweise

- Original CoreBox-Didaktikkonzept: [Didaktikkonzept CoreBox - Version 1 (1).md](../Didaktikkonzept%20CoreBox%20-%20Version%201%20%281%29.md)
- Shop-Beschreibungen: [corebox.md](../corebox.md), [electronics.md](../electronics.md), [fluoled.md](../fluoled.md), [fluolaser.md](../fluolaser.md), [infinitybox.md](../infinitybox.md), [lightsheet.md](../lightsheet.md), [qbox.md](../qbox.md)
- Inhalte werden referenziert, aber **nicht gelöscht**, bis die neue Struktur stabil ist.
- Für Modul-Dokumentation, die bereits in `dev/hw/` oder GitHub existiert: **verlinken, nicht kopieren**, bis ein Review stattgefunden hat.
