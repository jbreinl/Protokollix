<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

<p align="center">
  <img src="FullIcon.png" alt="Protokollix Logo" width="520">
</p>

🌐 **Language:** English | [🇩🇪 Deutsche Version](de)

---

**Protokollix** is a lightweight desktop tool for fast data evaluation, interactive plotting, and automated maximum error propagation—optimized for undergraduate physics laboratory courses and scientific reports, designed specifically to save time during data analysis.

---

## Table of Contents
- [Installation & Download](#installation--download)
  - [Option 1: Standalone Application](#option-1-standalone-application-recommended--no-python-required)
  - [Option 2: Run from Source Code](#option-2-run-from-source-code-python-required)
- [Quick Start](#quick-start)
- [Language Selection](#language-selection)
- [Data Import & File Formats (Excel / CSV)](#data-import--file-formats-excel--csv)
  - [Importing Data from Files](#importing-data-from-files)
  - [Importing Data via the Built-in Table](#importing-data-via-the-built-in-table)
  - [Exporting Plots & Data](#exporting-plots--data)
- [Overview of Graphical Customizations](#overview-of-graphical-customizations)
- [Overview of Mathematical Operations](#overview-of-mathematical-operations)
  - [Curve Fitting / Regression](#curve-fitting--regression)
  - [Maximum Error Calculator](#maximum-error-calculator)
    - [Target Selection for Data](#target-selection-for-data)
    - [Formula Input & Syntax](#formula-input--syntax)
    - [Uncertainties & Instrument Digits](#uncertainties--instrument-digits)
    - [Live Data & Preview Table](#live-data--preview-table)
    - [Applying & Resetting Changes](#applying--resetting-changes)
  - [Mean Calculator](#mean-calculator)
    - [Functionality & Statistical Formulas](#functionality--statistical-formulas)
    - [Data Input: File Import or Manual Table](#data-input-file-import-or-manual-table)
  - [Peak Detection (Local Maxima / Minima)](#peak-detection-local-maxima--minima)
    - [Plot Visualization](#plot-visualization)
    - [Exporting Extrema](#exporting-extrema)

---

## Installation & Download

### Option 1: Standalone Application (Recommended – no Python required)
Pre-built standalone executables for Windows and macOS are available under **[Releases](https://github.com/jbreinl/Protokollix/releases)** on the right:

1. Download the archive matching your operating system (`Protokollix-Windows.zip` or `Protokollix-macOS-arm64.zip`).
2. Extract the archive.
3. Launch the application by double-clicking the executable (no Python environment required).

<div id="important-notice-for-macos-users-gatekeeper-warning" style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>macOS Security Notice:</strong><br>
Because Protokollix is a free, open-source project without a paid Apple Developer certificate, macOS Gatekeeper flags the downloaded bundle on initial launch (<em>"Apple cannot check it for malicious software"</em> or <em>"App is damaged"</em>).<br><br>
<strong>How to open the app for the first time:</strong><br><br>
<strong>Option A (Via System Settings):</strong>
<ol>
  <li>Attempt to open <strong>Protokollix</strong> via double-click once (the security warning appears) &rarr; click <strong>Done</strong> (or <strong>Cancel</strong>).</li>
  <li>Open your Mac's <strong>System Settings</strong> &rarr; <strong>Privacy & Security</strong>.</li>
  <li>Scroll down to the <strong>Security</strong> section.</li>
  <li>Click <strong>"Open Anyway"</strong> next to the Protokollix prompt and confirm.</li>
</ol>
<strong>Option B (Fast Terminal Fix / Remove Quarantine):</strong><br>
If macOS prevents execution by stating the app is damaged, open your <strong>Terminal</strong> and run:
<pre style="background: #e1e4e8; padding: 8px; border-radius: 4px; margin-top: 6px;">xattr -cr /path/to/Protokollix.app</pre>
<em>(Tip: Type <code>xattr -cr </code> with a trailing space, drag & drop the extracted <code>Protokollix.app</code> from Finder directly into the Terminal window, and hit Enter).</em><br><br>
<strong>Notice:</strong> This bypass is only required <strong>once</strong> right after downloading. Afterwards, Protokollix will launch normally via double-click.
</div>

<div id="note-for-windows-users-smartscreen" style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Windows SmartScreen Notice:</strong><br>
On initial launch, Microsoft Defender SmartScreen might display: <em>"Windows protected your PC"</em>.<br>
Simply click <strong>"More info"</strong> and then select <strong>"Run anyway"</strong>.
</div>

---

### Option 2: Run from Source (Python required)

If you have Python installed or want to modify the source code:

1. Clone the repository:
   ```bash
   git clone [https://github.com/jbreinl/Protokollix.git](https://github.com/jbreinl/Protokollix.git)
   cd Protokollix
   ```
2. Install the required dependencies:
   ```bash
   pip install PySide6 numpy pandas matplotlib scipy sympy openpyxl
   ```
3. Run the application:
   ```bash
   python protokollix.py
   ```

---

## Quick Start

1. Click **"Open Excel / CSV"** and choose your measurement file.
2. Select your desired active Y dataset in the left control panel under the **General** tab.
3. Configure axis labels, axis scaling (linear/logarithmic), styles, and curve fits.
4. Perform mathematical transformations or error propagations in the **Error Calculator** and calculate statistical means using the **Mean Calculator**.
5. Export the finished publication-quality figure via **"Save Plot as..."** as a high-resolution PDF or PNG file for your lab report.

---

## Language Selection
Protokollix fully supports both German and English. The language can be changed dynamically at any time via the top menu under `Edit -> Sprache/Language`. The user interface updates immediately; dialog windows (such as the Mean Calculator and the Error Calculator) adopt the newly selected language the next time they are opened.

---

## Data Import & File Formats (Excel / CSV)

### Importing Data from Files 

Protokollix supports spreadsheet files (`.xlsx`, `.xls`) as well as comma/semicolon-separated values (`.csv`). The file dialog is triggered via the **Data** tab.

To ensure proper parsing, format your table as follows:

* **Column 1:** X values (e.g., time, voltage, frequency)
* **Subsequent Columns:** Y values (any number of parallel measurement series)
* **Optional:** Row 1 as a descriptive header (column titles and units are recognized automatically)

| X (Time in s) | Y1 (Current in A) | Y2 (Voltage in V) |
| :--- | :--- | :--- |
| 1.0 | 0.25 | 1.20 |
| 2.0 | 0.51 | 2.38 |
| 3.0 | 0.74 | 3.61 |

The program validates the structure during import and alerts you if columns or formats do not conform.

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Decimal Separators:</strong> Both decimal dots (<code>1.25</code>) and European decimal commas (<code>1,25</code>) are parsed and converted into valid floating-point numbers automatically.
</div>

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Background Initialization:</strong> When importing data for the very first time in a session, there might be a brief delay (1–10 seconds depending on system performance). This occurs because SciPy's peak-detection engine (<code>find_peaks</code>) initializes in the background. The mouse cursor changes to a waiting cursor to signal this background task.
</div>

---

### Importing Data via the Built-in Table

For small measurement series or quick corrections, you can enter data manually in the built-in table view located inside the **Data** tab:

<p align="center">
  <img src="Datentabelle.png" alt="Built-in data table" width="700"><br>
  <em>Figure 1: Built-in spreadsheet table for manual data entry and editing.</em>
</p>

Data can be typed directly or pasted from the system clipboard. Incomplete data pairs (e.g., missing an X or Y coordinate) are automatically ignored during plotting, preventing runtime crashes. 

Once manual values have been entered, select the newly added series using the central dataset selector dropdown in the **General** tab:

<p align="center">
  <img src="Aktiverdatensatz.png" alt="Active dataset selector" width="700"><br>
  <em>Figure 2: The active dataset must be chosen via the dropdown menu.</em>
</p>

The placeholder option `No data available` disappears once real data is imported. The table view can also be used to slightly modify existing points. To delete entire rows completely from an imported dataset, edit the original source file and reload it.

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Best Practice:</strong> While convenient for small checks, it is advisable to log raw lab data inside a dedicated spreadsheet program (such as Excel) and import the finished file into Protokollix.
</div>

---

### Exporting Plots & Data

Plots can be saved at any time using the **"Save Plot as..."** button. Supported output formats include `.png`, `.jpg`, `.svg`, and `.pdf`. A dialog will prompt for the target destination. Export resolution can be set between 100 and 1200 DPI via the export slider. 

Processed and recalculated numerical data can also be exported separately—for details, see the [Maximum Error Calculator](#maximum-error-calculator).

---

## Overview of Graphical Customizations

Protokollix provides extensive graphical customizations on top of `Matplotlib`, without requiring any manual Python scripting.
Most text input fields support native **LaTeX notation**. The program operates under a strict *"What you see is what you get"* approach: all adjustments update in real time.

Configurable plot settings include:
* Aspect ratio, font sizes, and individual dataset legend labels
* X and Y axis limits, custom tick formatting, and scale models (linear, semilog-X, semilog-Y, log-log)
* Line styles, data point marker types, and marker sizes
* Grid lines (True/False), line and scatter colors, and automatic/manual legend positions

Input fields feature real-time LaTeX syntax checking and highlight in red when an incomplete expression (such as an unclosed `$` sign) is detected, preventing canvas crashes while typing.

<p align="center">
  <img src="schwingung.png" alt="Example plot of a damped oscillation" width="700"><br>
  <em>Figure 3: High-resolution plot of a damped oscillation rendered in Protokollix.</em>
</p>

---

## Overview of Mathematical Operations

One of the application's strongest capabilities is applying mathematical transformations and computing experimental error propagations directly on measurement series:

* **Regression Fits:** Fit standard analytical models through data points.
* **Data Manipulation & Error Propagation:** General arithmetic manipulation along with an automated maximum error calculator based on symbolic derivation. Propagated uncertainties are rendered automatically as error bars.
* **Mean Calculator:** Calculates the sample mean and standard error of the mean across arbitrary datasets, including batch-processing of multiple series.
* **Local Extrema (Peaks / Troughs):** Finds and marks local maxima and minima, with direct export to Excel.

---

### Curve Fitting / Regression
Fitting regression models through experimental data is located under the **Calculator** tab:

<p align="center">
  <img src="Fits.png" alt="Fit selector dropdown" width="700"><br>
  <em>Figure 4: Regression models selectable via the dropdown menu.</em>
</p>

The following models are available:
* Linear: $y = kx + d$
* Quadratic: $y = ax^2 + bx + c$
* Cubic: 3rd-degree polynomial
* Exponential: $y = A \cdot e^{Bx}$
* Andrade / Inverse-Exponential: $y = A \cdot e^{B/x}$
* Saturation: $y = A \cdot (1 - e^{-Bx})$

Once a model is selected, its custom legend label can be configured. The evaluated parameters—**including their standard errors** computed from the covariance matrix—are displayed above the plot:

<p align="center">
  <img src="Fittest.png" alt="Fit with parameters and uncertainties" width="700"><br>
  <em>Figure 5: Example of an exponential fit displaying calculated parameters and standard errors.</em>
</p>

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Note:</strong> Plotting multiple distinct regression curves simultaneously within the same axis is currently not supported, as this is rarely required in standard lab reports.
</div>

---

### Maximum Error Calculator

Clicking the `Data Manipulation and Error Calculation` button opens a dedicated calculation workspace:

<p align="center">
  <img src="Rechner.png" alt="Error calculator window" width="700"><br>
  <em>Figure 6: The Maximum Error Calculator interface.</em>
</p>

---

#### Target Selection for Data

Three radio options at the top define how transformed data is routed:
* **Y-Data & Y-Errorbar (vertical):** Calculations and propagated uncertainties are applied to the active Y dataset. Error bars are drawn vertically. Transformed series can be exported using the `Save Data` button.
* **X-Data & X-Errorbar (horizontal):** Calculations and propagated uncertainties apply to the X dataset. Error bars are drawn horizontally.
* **Calculation Only (Table / Single Value):** For calculations that do not require plotting. Using the dedicated `Load single data column` button, an isolated data column can be evaluated and exported independently.

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Variable Mapping:</strong> Inside the <code>Calculation Only</code> mode, loaded values are referenced using variable <code>y</code>.<br><br>
In physics, axes are often named after specific physical quantities (such as $t$ for time or $s$ for displacement). Inside the calculator, axes are <strong>always referenced as <code>x</code> and <code>y</code></strong>, as the parser cannot guess the physical nature of your measurement.
</div>

---

#### Formula Input & Syntax

Below the target options are two formula fields:

* **Mathematical Formula (rendered):** Read-only preview field providing formatted mathematical rendering for legibility.
* **Mathematical Formula:** The actual input field where algebraic expressions are entered.

<p align="center">
  <img src="Rendering.png" alt="Live formula preview" width="700"><br>
  <em>Figure 7: Formula preview (rendered) and text input fields.</em>
</p>

The integrated engine uses SymPy for symbolic algebra. The following standards apply:

* Arithmetic: `+`, `-`, `*`, `/`
* Powers: `**` or `^` (e.g., `r**2` or `r^2` for $r^2$). Exponential functions are written as `exp(...)`.
* Functions: `sin(...)`, `cos(...)`, `sqrt(...)`, `exp(...)`. <br>
`log(...)` evaluates the **common logarithm** ($\log_{10}$), whereas `ln(...)` evaluates the **natural logarithm** ($\ln$). While this diverges from standard Python conventions, it mirrors scientific calculators and physics course standards.
* Numerical Derivatives: `diff(y)` evaluates the numerical derivative $\frac{dy}{dx}$ using finite gradient approximations (`np.gradient`).

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Syntax Convention:</strong> The constant $\pi$ must be entered in lowercase as <code>pi</code> (not <code>Pi</code>).
</div>

<details>
<summary><b>Show Example: Plotting the phase space of a damped harmonic oscillator</b></summary>

To plot phase space $(\varphi, \dot{\varphi})$ or $(x, \dot{x})$, plot angular velocity against angular displacement.

**Initial Scenario:**
Your spreadsheet contains time $t$ (Column 1) and angular displacement $\varphi$ (Column 2).

**Step-by-Step in Protokollix:**

1. **Calculate Angular Velocity:**
   * Select **X-Data & X-Errorbar (horizontal)** under *Target of Calculation*.
2. **Assign the Derivative:**
   * In the formula field, enter `diff(y)` (evaluates $\dot{\varphi} = \frac{d\varphi}{dt}$). This replaces the time axis data with angular velocity $\omega$. Click **OK**.

<p align="center">
  <img src="diff.png" alt="Derivative via diff(y)" width="700"><br>
  <em>Figure 8: Applying diff(y) to numerically differentiate displacement data.</em>
</p>

3. **Result:**
   * Click **Adjust Axis Limits** in the **General** tab. The plot now displays the characteristic inward-spiraling phase-space trajectory approaching the origin $(0, 0)$.

<p align="center">
  <img src="Phasenraum.png" alt="Phase space plot" width="700"><br>
  <em>Figure 9: The resulting phase-space trajectory of a damped oscillation.</em>
</p>
</details>

---

### Uncertainties & Instrument Digits

Protokollix implements rigorous worst-case error propagation (Größtfehler) via total differentials:

$$\Delta f = \sum_i \left| \frac{\partial f}{\partial v_i} \right| \cdot \Delta v_i$$

For every custom variable entered in the formula (as well as for `x` and `y`), three input fields are generated:
* Value of the variable
* Absolute uncertainty ($\Delta$) of the variable
* Instrument digit uncertainty ($\pm X$ digits, integer)

In the following example, constants `a` and `b` are multiplied with `y`: $a = 1.5, \Delta a = 0.01$, Digits(a) = 1, $b = 2, \Delta b = 0.05$:

<p align="center">
  <img src="Unsicherheiten.png" alt="Uncertainty parameter inputs" width="700"><br>
  <em>Figure 10: Parameter definitions including absolute uncertainties and instrument digits.</em>
</p>

The digit error is determined automatically from the smallest decimal place of the input (e.g., $0.01$ for an input of `1.25`) multiplied by the number of digits.

Uncertainties can also be imported from a single-column Excel file:

<p align="center">
  <img src="ImportUnsicherheiten.png" alt="Importing uncertainties" width="700"><br>
  <em>Figure 11: Y uncertainties loaded from an external Excel file.</em>
</p>

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Workflow Tip:</strong> You can work incrementally: calculate uncertainties for an isolated dataset first, export them, reload the original measurement coordinates, and import the previously computed uncertainties.
</div>

---

#### Live Data & Preview Table
The preview table at the bottom updates with every keystroke:
* `Index`: Row numbering.
* `X-Data` / `Y-Data`: Current coordinate values.
* `Ergebnis f`: Result of the evaluated mathematical function.
* `Fehler Δf`: Propagated total uncertainty $\Delta f$.

---

#### Applying & Resetting Changes
Clicking **OK** commits the transformed values to the main plot. **Calculated uncertainties automatically become error bars.** 

To undo modifications, use the **Reset X-Data** or **Reset Y-Data** buttons in the **Data** tab to restore the original imported state.

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Two-Axis Propagation:</strong> If you want to transform both axes or assign error bars to both X and Y, run the calculator twice: once selecting X data, click <strong>OK</strong>, then reopen, select Y data, and confirm with <strong>OK</strong> again.
</div>

---

### Mean Calculator

Repeated measurements of identical quantities require calculating the arithmetic mean and sample standard deviation. Clicking **Mean Calculator** opens this analysis dialog:

<p align="center">
  <img src="Mittelwertrechner.png" alt="Mean calculator interface" width="600"><br>
  <em>Figure 12: The Mean Calculator dialog window.</em>
</p>

---

#### Functionality & Statistical Formulas

The calculator computes standard statistical indicators:

* **Arithmetic Mean ($\bar{x}$):**
  $$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$
* **Sample Standard Deviation ($s_x$):**
  $$s_x = \sqrt{\frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})^2}$$
* **Standard Error of the Mean ($s_{\bar{x}}$):**
  $$s_{\bar{x}} = \frac{s_x}{\sqrt{n}}$$

---

#### Data Input: File Import or Manual Table

1. **Excel/CSV Import:** Load files containing measurement series organized into columns. Multiple columns are processed in parallel as separate series.
2. **Manual Input:** Enter numbers directly into the interactive spreadsheet; calculations update in real time.

Using **Save as Excel**, all computed statistics across all columns can be exported in a clean tabular summary.

<details>
<summary><b>Show Example: Evaluating multiple imported measurement series</b></summary>

<p align="center">
  <img src="Mittelwertrechner_items.png" alt="Parallel mean evaluation" width="700"><br>
  <em>Figure 13: Parallel evaluation of multiple measurement series in the Mean Calculator.</em>
</p>
</details>

---

### Peak Detection (Local Maxima / Minima)

For resonance curves, damped oscillations, and spectroscopy, Protokollix integrates peak detection powered by `scipy.signal.find_peaks`. Controls are located under the **Calculator** tab in the *Maxima / Minima* section.

#### Plot Visualization
Use the dropdown menu to highlight extrema on the active Y series:
* **Hide local Max/Min:** Standard view (no markers).
* **Show Local Maxima:** Marks all detected peaks with red `+` symbols on the curve.
* **Show Local Minima:** Marks all detected troughs on the curve.

<p align="center">
  <img src="Maxima.png" alt="Peak detection controls" width="700"><br>
  <em>Figure 14: Marking and exporting local extrema.</em>
</p>

<div style="background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 14px 18px; margin: 16px 0; border-radius: 4px; color: #24292e;">
<strong>Requirements:</strong> Peak detection evaluates the currently active Y dataset. The dropdown and export buttons remain disabled when no data is loaded or when no peaks are detected.
</div>

#### Exporting Extrema
Click **"Save Maxima / Minima to Excel"** to export all identified extrema into a standalone Excel (`.xlsx`) or CSV (`.csv`) file with four columns:
* `Minima (x)` & `Minima (y)`
* `Maxima (x)` & `Maxima (y)`

Differing row counts between peaks and troughs are balanced with empty cells automatically.
