# Protokollix 📊

**Protokollix** ist ein leichtgewichtiges Desktop-Werkzeug zur schnellen Datenauswertung, interaktiven Plot-Erstellung und automatisierten Größtfehlerberechnung – optimiert für physikalische Praktika und wissenschaftliche Laborberichte.

---

## Inhaltsverzeichnis
- [Installation & Download](#installation--download)
- [Schnellstart](#schnellstart)
- [Datenformat (Excel / CSV)](#datenformat-excel--csv)
- [Funktionen im Überblick](#funktionen-im-überblick)
- [Größtfehler-Rechner (Syntax)](#größtfehler-rechner-syntax)
- [Kontakt & Feedback](#kontakt--feedback)

---

## Installation & Download

### Option 1: Fertige Anwendung (Empfohlen – kein Python nötig)
Die fertigen Programme für Windows und macOS findest du rechts unter **[Releases](https://github.com/DEIN_NUTZERNAME/Protokollix/releases)**:

1. Lade für dein Betriebssystem das neueste Archiv herunter (`Protokollix_Windows.zip` oder `Protokollix_Mac.zip`).
2. Entpacke die Datei.
3. Starte die Anwendung per Doppelklick (keine Python-Installation erforderlich).

### Option 2: Direkt aus dem Quellcode ausführen (Python erforderlich)

Falls du Python bereits installiert hast oder den Quellcode anpassen möchtest:

1. Klone das Repository oder lade `script.py` herunter.
2. Installiere die benötigten Abhängigkeiten im Terminal:

   ```bash
   pip install PySide6 numpy pandas matplotlib scipy sympy openpyxl

---

## Schnellstart

1. Klicke auf **„Öffne Excel / CSV“** und wähle deine Messdatei aus.
2. Wähle im rechten Bedienfeld unter **Data** die gewünschte Y-Messreihe aus.
3. Passe Achsenbeschriftungen, Skalierung (linear/logarithmisch) und Kurvenanpassungen (z. B. Polynom- oder Exponential-Fit) an.
4. Exportiere das fertige Diagramm über **„Save Plot“** als hochauflösende PDF- oder PNG-Grafik für dein Protokoll.

---

## Dateneinlese und Datenformat (Excel / CSV)

### Daten importieren über Dateien
Damit Protokollix Dateien fehlerfrei einliest, muss die Datei wie folgt aufgebaut sein:

* **Spalte 1:** X-Werte (Messzeit, Spannung, etc.)
* **Folgende Spalten:** Y-Werte (Messreihen)
* Optional: Zeile 1 als Spaltentitel (Header)

| X (Zeit in s) | Y1 (Strom in A) | Y2 (Spannung in V) |
| :--- | :--- | :--- |
| 1.0 | 0.25 | 1.20 |
| 2.0 | 0.51 | 2.38 |
| 3.0 | 0.74 | 3.61 |

Derzeit können entweder Excel oder CSV Dateien importiert werden - andere Dateitypen werden nicht unterstützt. Das Programm gibt eine Warnung aus, falls die eingelesenen Daten nicht passen, und zeigt zusätzlich beim Importieren nochmal das erwünschte Format an. 

> [!TIP]
> Dezimaltrennzeichen: Sowohl Punkte (`1.25`) als auch Kommas (`1,25`) werden beim Einlesen automatisch erkannt und konvertiert.

### Daten importieren durch die eingebaute Tabellenfunktion


---

## Funktionen im Überblick

* **Interaktive Messwerttabelle:** Manuelles Hinzufügen, Bearbeiten oder Entfernen von Datenreihen und Einzelpunkten per Rechtsklick.
* **Fit-Routinen:** Lineare Regression, Polynom-Fits, Exponential- und Sättigungsfunktionen (über SciPy).
* **Peak-Erkennung:** Lokale Extrema (Minima/Maxima) automatisch markieren und exportieren.
* **Symbolische Größtfehlerberechnung:** Partielle Ableitungen und Fehlerfortpflanzung auf Knopfdruck.

---

## Größtfehler-Rechner (Syntax)

Der integrierte Rechner nutzt symbolische Computeralgebra (SymPy). Beim Eingeben der Berechnungsformel gelten folgende mathematische Standards:

* Multiplikation: `*` (z. B. `m * g * h`)
* Potenzen: `**` (z. B. `r**2` für $r^2$)
* Funktionen: `sin(...)`, `cos(...)`, `sqrt(...)`, `exp(...)`, `log(...)`

<details>
<summary><b>Beispiel anzeigen: Kinetische Energie</b></summary>

* **Formel:** `0.5 * m * v**2`
* **Variablen:** `m, v`
* **Unsicherheiten:** `dm, dv`

Das Programm bildet automatisch die partiellen Ableitungen:
$$\Delta E_{\text{kin}} = \left| \frac{\partial E}{\partial m} \right| \Delta m + \left| \frac{\partial E}{\partial v} \right| \Delta v$$
</details>

---

## Kontakt & Feedback

Gefällt dir das Tool oder hast du einen Fehler gefunden?
* Erstelle gerne ein **Issue** hier auf GitHub.
* Oder schreibe eine E-Mail an: `jakob.breinl@edu.uni-graz.at`