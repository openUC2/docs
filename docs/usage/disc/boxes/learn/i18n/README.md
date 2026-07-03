# Mehrsprachigkeit (i18n) – Strategie und Arbeitsregeln

> Dieses Dokument ist **kein Inhalt für Nutzer\*innen**, sondern eine **interne Arbeitsregel** für Autor\*innen und Contributor\*innen.

---

## Grundsatz: Englisch ist die Quell­sprache

Alle Inhalte in `learn/` werden **zuerst auf Englisch** geschrieben. Englisch ist:

- die Arbeitssprache der Forschung und Industrie,
- am leichtesten in andere Sprachen zu übersetzen (maximale Reichweite),
- konsistent mit dem Rest der openUC2-Dokumentation.

**Ausnahme:** Inhalte, die explizit für den deutschen Schulbetrieb gedacht sind (z. B. Stundenverläufe, Arbeitsblätter, Lehrerhandreichungen), können primär auf Deutsch entstehen. Eine englische Übersetzung wird dann als Folgeaufgabe markiert.

---

## Technische Umsetzung in Docusaurus

Docusaurus unterstützt i18n nativ. Übersetzungen liegen **außerhalb** von `docs/`, im Stammverzeichnis des Repos:

```
i18n/
├── de/
│   └── docusaurus-plugin-content-docs/
│       └── current/
│           └── usage/disc/boxes/learn/   ← Spiegel von docs/usage/disc/boxes/learn/
│               ├── README.md             ← deutsche Übersetzung
│               ├── corebox/
│               │   └── index.md
│               └── ...
├── fr/
├── es/
└── ...
```

Regeln:
- **Dateinamen und Verzeichnisnamen** sind identisch mit der Englisch-Quelle.
- **Bilder** werden nicht übersetzt (Dateinamen bleiben, Alt-Texte im Markdown werden übersetzt).
- **Frontmatter** (`title`, `description`) wird übersetzt.

---

## Übersetzungs-Prioritäten

| Abschnitt | Priorität | Begründung |
|---|---|---|
| Tutorial-Abschnitte in `experiments/` | **Hoch (DE zuerst)** | Schüler\*innen und Lehrkräfte; Kernnutzen der Discovery-Boxen |
| `concept.md` (Didaktikkonzept) | **Hoch (DE zuerst)** | Direkt für Lehrkräfte in DE/AT/CH |
| Box `index.md` | **Mittel** | Navigation; ohne Übersetzung trotzdem nutzbar |
| `hardware/` (Cube-Mechanik) | **Mittel** | Wichtig für Maker und Schüler; Fachbegriffe oft international |
| `modules/*.md` (Reference) | **Niedrig** | Technische Spezifikationen; Englisch in Industrie/Forschung üblich |
| `advanced/` | **Niedrig** | Forschungskontext; Englisch reicht |

---

## Workflow für Autor\*innen

### Neuen Inhalt schreiben

1. Datei auf Englisch unter `learn/…` anlegen.
2. Wenn der Inhalt **primär für Schulen (DE)** ist: gleichzeitig deutsche Version unter `i18n/de/…` anlegen; englische Version als TODO markieren.
3. Am Ende der Datei-Kommentarblock einfügen:

```markdown
<!-- i18n status: source=en | de=TODO | fr=TODO -->
```

### Bestehenden Inhalt übersetzen

1. Englische Quelldatei lesen.
2. Entsprechende Datei unter `i18n/<lang>/…` anlegen (Pfad 1:1 spiegeln).
3. Status-Kommentar aktualisieren: `de=done`.
4. Pull Request mit Label `translation`.

---

## Was tun mit den bestehenden deutschen Inhalten?

Das Didaktikkonzept `Didaktikkonzept CoreBox - Version 1 (1).md` ist bereits auf Deutsch. Migration:

1. Englische `concept.md` aus dem Template befüllen → das ist dann die Quelle.
2. Deutschen Text aus dem Originaldokument als `i18n/de/…/corebox/concept.md` ablegen.
3. Originalfile **nicht löschen**, bis Migration abgeschlossen und geprüft.

---

## Häufige Fragen

**Kann ich direkt auf Deutsch schreiben, wenn ich kein Englisch mag?**
Ja – schreibe auf Deutsch, lasse den Abschnitt `<!-- i18n status: source=de | en=TODO -->` stehen. Ein anderer Contributor übernimmt die Englisch-Version.

**Brauche ich eine Übersetzung, bevor ich einen PR merge?**
Nein. Die englische Quelle muss vorhanden sein; Übersetzungen sind optional und können nachgereicht werden.

**Wie übersetze ich Abbildungstexte?**
Bilder bleiben unverändert. Alt-Text und Bildunterschriften im Markdown werden übersetzt. Bei Grafiken mit eingebettetem Text (z. B. Strahlengang-Diagramme) wird eine separate, lokalisierte Version des Bildes unter `static/img/<lang>/…` abgelegt.
