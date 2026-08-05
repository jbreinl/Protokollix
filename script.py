# Fehler die es zu beheben gibt:
#Was, wenn ich fehlerbalken für x und y haben will? Weil beide messgrößen behaftet sind? Funktioniert nicht. 
# Es nimmt x werte und fehler für die y achse an. 
#Ersetzt das ganze nun meine "y/x" Transformations-Box?


import sys
import os
import pandas as pd
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
# 1. Zwingt Matplotlib dazu, PySide6 statt PyQt6 zu verwenden!
os.environ["QT_API"] = "pyside6"
from scipy.optimize import curve_fit

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.ticker as ticker

# 2. PySide6 Imports
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QTableWidget, QTableWidgetItem, QWidget, QDialog, QFormLayout, QDialogButtonBox, QSlider, QCheckBox, QStyledItemDelegate, QTabWidget, QComboBox, QColorDialog,  QDoubleSpinBox, QMessageBox, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel  # H = Horizontal,  V = Vertikal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#Vorläufige Hauptfunktion

class MeinPlotterApp(QMainWindow): # Vererbung, also das übergeben von QMainWindow gibt der Klasse alle Funktionen, die QMainWindow auch hat. 
    def __init__(self):
        super().__init__()

    # Fenstertitel und Anfangsgröße festlegen
        self.setWindowTitle("Phyplot - © 2026 Jakob Breinl")
        self.setGeometry(100, 100, 1200, 800)

        # Speicher für die geladenen Daten (anfangs leer)
        self.x_data = None
        self.y_data = None
        self.x_err = None  # Neu!
        self.y_err = None
        self.current_x = None
        self.current_y = None
        self.plot_color = QColor("#1f77b4")
        self.w = 5
        self.h = 4

        # Das Haupt-Widget und das Layout erstellen
        zentral_widget = QWidget()
        self.setCentralWidget(zentral_widget)
        self.haupt_layout = QHBoxLayout()
        zentral_widget.setLayout(self.haupt_layout)

        #Aufräumen
        self.setup_bedienfeld()
        self.setup_plot()
        self.connect_signals()

        # Einmalig am Anfang ausführen, damit der Start-Titel gesetzt wird
        self.plot_aktualisieren()

    def setup_bedienfeld(self):
    #Tab Bedienungsfeld

        self.tabs = QTabWidget()

        tab_label_widget = QWidget()
        layout_tab_label= QVBoxLayout()
        # Erstellt ein neues Layout


    #Seitenverhältniss

        layout_tab_label.addWidget(QLabel("Seitenverhätlnis z.B. 5:4"))
        figsize_layout = QHBoxLayout()

        #Horizontale Größe
        self.figsize_x_input = QDoubleSpinBox()
        self.figsize_x_input.setValue(5)
        self.figsize_x_input.setRange(1.0, 30.00) # Maximale Bildgröße
        self.figsize_x_input.setSingleStep(0.10)
        figsize_layout.addWidget(self.figsize_x_input)


        #Vertikale Größe
        self.figsize_y_input = QDoubleSpinBox()
        self.figsize_y_input.setValue(4)
        self.figsize_y_input.setRange(1.0, 30.00) # Maximale Bildgröße
        self.figsize_y_input.setSingleStep(0.10)
        figsize_layout.addWidget(self.figsize_y_input)

        layout_tab_label.addLayout(figsize_layout)


        #Schriftgröße
        layout_tab_label.addWidget(QLabel("Schriftgröße"))

        self.fontsize_slider = QSlider(Qt.Orientation.Horizontal)

        self.fontsize_slider.setRange(6,25) # Range
        self.fontsize_slider.setValue(12) # Startwert

        self.fontsize_slider.setSingleStep(1) #1er Schritte als Skalierung
        layout_tab_label.addWidget(self.fontsize_slider)


        #Titel Eingabe
        layout_tab_label.addWidget(QLabel("Plot-Titel:"))

        self.titel_input = QLineEdit() #Self ist hier super zentral, weil ich auf den text ja später noch zugreifen will! 
        self.titel_input.setPlaceholderText("z.B. Pendelversuch")
        layout_tab_label.addWidget(self.titel_input)


        # 2. X-Achse-eingabe
        layout_tab_label.addWidget(QLabel("X-Achse (LaTeX Support):"))

        self.x_label_input = QLineEdit()
        self.x_label_input.setPlaceholderText("z.B. Zeit t / s")
        layout_tab_label.addWidget(self.x_label_input)


        # 3. Y-Achse-Eingabe
        layout_tab_label.addWidget(QLabel("Y-Achse (LaTeX Support):"))
        self.y_label_input = QLineEdit()
        self.y_label_input.setPlaceholderText("z.B. Auslenkung x / m")
        layout_tab_label.addWidget(self.y_label_input)

        #--------------------------------------------------------------------------------------
        #Achenlimits

        # X achsen Limit
        layout_tab_label.addWidget(QLabel("X-Achsen-Limits"))
        x_limits_layout = QHBoxLayout()

        # X minimum
        self.x_min_input = QDoubleSpinBox()
        self.x_min_input.setValue(-10.0)
        self.x_min_input.setRange((-(10**5)), (10**5)) # Erlaubt Werte von -100000 bis +100000
        x_limits_layout.addWidget(self.x_min_input)

        # SpinBox für X-Max
        self.x_max_input = QDoubleSpinBox()
        self.x_max_input.setRange((-(10**5)), (10**5))
        self.x_max_input.setValue(10.0)            
        x_limits_layout.addWidget(self.x_max_input)

        layout_tab_label.addLayout(x_limits_layout)# 4. Das Unter-Layout (addLayout!) ins Haupt-Bedienfeld einfügen


        # Y Achsen Limits
        layout_tab_label.addWidget(QLabel("Y-Achsen-Limits"))
        y_limits_layout = QHBoxLayout()

        #SpinBox für Y-min
        self.y_min_input = QDoubleSpinBox()
        self.y_min_input.setValue(0)
        self.y_min_input.setRange((-(10**9)), (10**9)) # Erlaubt Werte von 1 Milliarde
        y_limits_layout.addWidget(self.y_min_input)


        #SpinBox für Y-Max
        self.y_max_input = QDoubleSpinBox()
        self.y_max_input.setRange((-(10**9)), (10**9))
        self.y_max_input.setValue(10.0)            
        y_limits_layout.addWidget(self.y_max_input)

        layout_tab_label.addLayout(y_limits_layout)# 4. Das Unter-Layout (addLayout!) ins Haupt-Bedienfeld einfügen
        #--------------------------------------------------------------------------------------

        # Button zum automatischen Anpassen der Axen anlegen

        self.achsenlimit_button = QPushButton("Achsenlimits automatisch anpassen")
        #Schriftgröße bearbeiten
        font = self.achsenlimit_button.font()
        font.setPointSize(11)
        self.achsenlimit_button.setFont(font)

        layout_tab_label.addWidget(self.achsenlimit_button)

        #Legende
        layout_tab_label.addWidget(QLabel("Datenlabel"))
        self.legende_input = QLineEdit()
        self.legende_input.setPlaceholderText("z.B. erste Messreihe")
        layout_tab_label.addWidget(self.legende_input)  
    
       


        # Ein Platzhalter-Federzug nach unten, der alles nach oben drückt
        layout_tab_label.addStretch()
        tab_label_widget.setLayout(layout_tab_label)
        #--------------------------------------------------------------------------------
    # Data
        tab_trafo_widget = QWidget()
        trafo_tab_layout = QVBoxLayout()

        # Hilfetext definieren
        # Hilfetext für Datentransformationen (HTML-formatiert)
        trafo_hilfe = (
            "Diese Eingabefelder ermöglichen das nachträgliche Bearbeiten "
            "der Daten (z. B. Umrechnen von Einheiten oder physikalische Transformationen).<br><br>"
            "<b>Mögliche Funktionen & Syntax:</b>"
            "<ul style='margin-top: 4px; margin-bottom: 4px; padding-left: 15px;'>"
                "<li><b>Grundrechenarten:</b> <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>^</code> (z. B. <code>x^2</code>, <code>y/1000</code>)</li>"
                "<li><b>Multiplikation ohne *:</b> <code>2x</code>, <code>3y</code> werden automatisch erkannt</li>"
                "<li><b>Trigonometrie:</b> <code>sin(x)</code>, <code>cos(x)</code>, <code>tan(x)</code></li>"
                "<li><b>Logarithmen & Wurzeln:</b> <code>log(y)</code> (nat. Log.), <code>exp(x)</code>, <code>sqrt(x)</code></li>"
                "<li><b>Konstanten:</b> <code>pi</code> (z. B. <code>x * 2 * pi</code>)</li>"
            "</ul>"
            "<b>Spezielle Manipulationen:</b>"
            "<ul style='margin-top: 4px; margin-bottom: 4px; padding-left: 15px;'>"
                "<li><b>Achsentausch:</b> Im X-Feld einfach <code>y</code> eingeben, das gleidhe fürs Y-Feld</li>"
                "<li><b>Ableitung (dy/dx):</b> <code>dy/dx</code> oder <code>diff(y)/diff(x)</code></li>"
                "<li><b>Schritt-Differenz:</b> <code>dy</code> oder <code>diff(y)</code> (nimmt Δx = 1 an)</li>"
            "</ul>"
        )
        
        #Eingabe für die X-Koordinate
        x_label_layout = QHBoxLayout()
        x_label_layout.addWidget(QLabel("X-Daten manipulieren"))
        x_label_layout.addWidget(self.erstelle_hilfe_button(trafo_hilfe))
        x_label_layout.addStretch()
        trafo_tab_layout.addLayout(x_label_layout)

        
        self.x_trafo_input = QLineEdit()
        self.x_trafo_input.setPlaceholderText("z.B. x*2*np.pi oder x/100")
        self.x_trafo_input.setToolTip(trafo_hilfe)
        trafo_tab_layout.addWidget(self.x_trafo_input)

        # 2. Eingabe für Y-Koordinates
        y_label_layout = QHBoxLayout()
        y_label_layout.addWidget(QLabel("Y-Daten transformieren:"))
        y_label_layout.addWidget(self.erstelle_hilfe_button(trafo_hilfe))
        y_label_layout.addStretch()
        trafo_tab_layout.addLayout(y_label_layout)

        self.y_trafo_input = QLineEdit()
        self.y_trafo_input.setPlaceholderText("z.B. dy/dx oder np.log(y)")
        self.y_trafo_input.setToolTip(trafo_hilfe)
        trafo_tab_layout.addWidget(self.y_trafo_input)


# Polyfit
        self.polyfit_heading_label = QLabel("Ausgleichskurve / Fit")
        trafo_tab_layout.addWidget(self.polyfit_heading_label)
        
        self.polyfit_combo = QComboBox()
        # Keine Extra-Delegates nötig! Direkt Unicode verwenden:
        self.polyfit_combo.addItem("None", None)
        self.polyfit_combo.addItem("linear: y = kx + d", "poly_1")
        self.polyfit_combo.addItem("quadratisch: y = ax² + bx + c", "poly_2")
        self.polyfit_combo.addItem("kubisch (3. Grad)", "poly_3")
        self.polyfit_combo.addItem("Exponential: y = A · eᵇˣ", "exp")
        self.polyfit_combo.addItem("Andrade / Invers-Expo: y = A · eᵇᐟˣ", "andrade")
        self.polyfit_combo.addItem("Sättigung: y = A · (1 - e⁻ᵇˣ)", "saettigung")
        self.polyfit_combo.setCurrentIndex(0)
        trafo_tab_layout.addWidget(self.polyfit_combo)

        # Polyfit Label
        self.polyfit_input_label = QLineEdit()
        self.polyfit_input_label.setPlaceholderText("Label des Fits: z.B. linearer Fit")
        self.polyfit_input_label.setEnabled(False)
        trafo_tab_layout.addWidget(self.polyfit_input_label)


    # Button für den Größtfehler-Rechner anlegen
        self.btn_groesstfehler = QPushButton("Größtfehlerrechner & Datenauswertung")
        
        # Den Button mit der eben getippten Methode verbinden
        self.btn_groesstfehler.clicked.connect(self.oeffne_groesstfehler_dialog)
        
        # Ins Layout deines Data-Tabs einfügen
        # (Ersetze 'data_layout' durch den Namen deines Layouts im Data-Tab)
        trafo_tab_layout.addWidget(self.btn_groesstfehler)

          
        trafo_tab_layout.addStretch()
        tab_trafo_widget.setLayout(trafo_tab_layout)


         #--------------------------------------------------------------------------------
    #Style

        tab_style_widget = QWidget()
        style_tab_layout = QVBoxLayout()


        # Auswahlbox für Linestyle
        style_tab_layout.addWidget(QLabel("Linestyle"))

        self.linestyle_combo = QComboBox()
        #Optionen hinzufügen
        self.linestyle_combo.addItem("None", "")
        self.linestyle_combo.addItem("-.", "-.")
        self.linestyle_combo.addItem("-", "-")
        self.linestyle_combo.addItem("--", "--")
        self.linestyle_combo.addItem(":", ":")
        self.linestyle_combo.setCurrentIndex(0)
        style_tab_layout.addWidget(self.linestyle_combo) 

        #Auswahlbox für den Markerstyle
        style_tab_layout.addWidget(QLabel("Markerstyle"))
        self.markerstyle_combo = QComboBox()
        markerstyles = [
        ("None", ""), ("point", "."), ("pixel", ","),  ("circle", "o"), ("triangle down", "v"), ("triangle up", "^"), ("triangle left", "<"),
        ("triangle right", ">"), ("tri down", "1"), ("tri up", "2"), ("tri left", "3"), ("tri right", "4"), ("octagon", "8"), ("square", "s"),
        ("pentagon", "p"), ("plus (filled)", "P"),  ("star", "*"),  ("hexagon1", "h"), ("hexagon2", "H"), ("plus", "+"), ("x", "x"), ("x (filled)", "X"), ("diamond", "D"),
        ("thin diamond", "d")]
        for name, code in markerstyles:
            self.markerstyle_combo.addItem(name, code)
        
        self.markerstyle_combo.setCurrentIndex(1)
        style_tab_layout.addWidget(self.markerstyle_combo)



        self.grid_checkbox = QCheckBox("Grid True/False")
        self.grid_checkbox.setChecked(True)
        style_tab_layout.addWidget(self.grid_checkbox)


        #Box für die Farbe(n)
        style_tab_layout.addWidget(QLabel("Linien und Markerfarbe:"))
        self.color_button = QPushButton("Farbe wählen")
        self.update_color_button_style()
        style_tab_layout.addWidget(self.color_button)


        style_tab_layout.addStretch()
        tab_style_widget.setLayout(style_tab_layout)

    #Import/Export

        #Excel öffnen Button

        tab_import_export_widget = QWidget()
        tab_import_export_layout = QVBoxLayout()

        #Button zum Datei öffnen einfügen

        self.datei_button = QPushButton("Excel öffnen")
        tab_import_export_layout.addWidget(self.datei_button)

        tab_import_export_widget.setLayout(tab_import_export_layout)

        # Speicher-Button anlegen
        self.save_button = QPushButton("Plot speichern unter...")

        # (Optional) Schrift etwas hervorheben
        font = self.save_button.font()
        font.setBold(True)
        self.save_button.setFont(font)

        # Ins Tab-Layout einfügen
        tab_import_export_layout.addStretch()
        tab_import_export_layout.addWidget(self.save_button)    


#Verknüpfen

        #Tabs zum QTABWIDGET hinzufügen und ins Hauptlayout schieben
        self.tabs.addTab(tab_label_widget, "Allgemeines")
        self.tabs.addTab(tab_trafo_widget, "Data")
        self.tabs.addTab(tab_style_widget, "Style")
        self.tabs.addTab(tab_import_export_widget, "Import/Export")

        #Das wichtigste:
        # Verknüpfen der Tabs mit dem Hauptlayout
        self.haupt_layout.addWidget(self.tabs, 1)

    def setup_plot(self):
        # Matplotlib Figure und Canvas erstellen


        plot_container = QWidget()
        plot_layout = QVBoxLayout()
        plot_container.setLayout(plot_layout)


        self.figure = Figure(figsize=(8, 6), dpi=100)# wieder zurücjändern zu 5,4
        self.canvas = FigureCanvas(self.figure)


        #Löschen?
        # 2. HIER DIREKT DIE CANVAS-GRÖSSE FIXIEREN (5 Zoll * 100 DPI = 500px, 4 Zoll * 100 DPI = 400px)
        # Oder dynamisch über die Spinboxen:
        w_start = int(self.figsize_x_input.value() * self.figure.dpi)
        h_start = int(self.figsize_y_input.value() * self.figure.dpi)
             

        #Löschen?
    

        # Ein Achsensystem (Axes) zur Figure hinzufügen
        self.ax = self.figure.add_subplot(1, 1, 1) #111 = Anzahl der Spalten, der Zeilen, Nummer des Plots im Raster
        self.initial_title = "noch keine Daten geladen"
        self.ax.set_title(self.initial_title)

        # Den Canvas in das Haupt-Layout einfügen, ohne das ist es nur eine weiße Oberfläche!

        plot_layout.addStretch()
        plot_layout.addWidget(self.canvas, alignment = Qt.AlignmentFlag.AlignCenter)
        plot_layout.addStretch()

        self.haupt_layout.addWidget(plot_container, 3) #3 Neu hinzufügens
 
    def connect_signals(self):
    #Signale Verbinden
        for signal in (
        self.titel_input.textChanged,
        self.x_label_input.textChanged,
        self.y_label_input.textChanged,
        self.x_min_input.valueChanged,
        self.x_max_input.valueChanged,
        self.y_min_input.valueChanged,
        self.y_max_input.valueChanged,
        self.x_trafo_input.textChanged,
        self.y_trafo_input.textChanged,
        self.legende_input.textChanged,
        self.linestyle_combo.currentTextChanged,
        self.markerstyle_combo.currentTextChanged,
        self.figsize_x_input.valueChanged, # Neu
        self.figsize_y_input.valueChanged, # Neu
        self.fontsize_slider.valueChanged,
        self.polyfit_combo.currentTextChanged,
        self.grid_checkbox.toggled,
        self.polyfit_input_label.textChanged
        ):
            signal.connect(self.plot_aktualisieren)

        # Button verknüpfungen
        self.datei_button.clicked.connect(self.load_file)
        self.achsenlimit_button.clicked.connect(self.auto_limits)
        self.color_button.clicked.connect(self.choose_color)
        self.save_button.clicked.connect(self.save_plot)

    def plot_aktualisieren(self):

    
        #Plotgröße updaten zu beginn
        w = self.figsize_x_input.value() # Bildgröße
        h = self.figsize_y_input.value()


        # 2. WICHTIG: Achse vollständig leeren vor dem Neuzeichnen!
        self.ax.clear()

        self.ax.set_box_aspect(h / w)



        #Restliche Werte holen
        titel_text = self.titel_input.text()
        x_text = self.x_label_input.text()
        y_text = self.y_label_input.text()
        label = self.legende_input.text()

        x_min = self.x_min_input.value()
        x_max = self.x_max_input.value()
        y_min = self.y_min_input.value()
        y_max = self.y_max_input.value()
        current_linestyle = self.linestyle_combo.currentData()
        current_markerstyle = self.markerstyle_combo.currentData()
        color = self.plot_color.name()
        fontsize = self.fontsize_slider.value()
        grid_aktiv = self.grid_checkbox.isChecked()  # Gibt True oder False zurück

        #Beschriftungen
        self.ax.set_title(titel_text if titel_text else self.initial_title, fontsize = fontsize)
        self.ax.set_xlabel(x_text if x_text else "X-Achse", fontsize = fontsize * 0.80)
        self.ax.set_ylabel(y_text if y_text else "Y-Achse", fontsize = fontsize * 0.80)

        # In plot_aktualisieren():
        # Berechne die maximale Anzahl an Gitterlinien basierend auf der Schriftgröße
        # Kleinere Schrift = mehr Gitterlinien (z.B. 10), Größere Schrift = weniger (z.B. 4)
        grid_dichte = int(np.clip(20 - (fontsize * 0.8), 4, 12))

        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=grid_dichte))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=grid_dichte))

        self.ax.grid(grid_aktiv)

        #Ticksgröße
        self.ax.tick_params(axis='both', labelsize=fontsize * 0.70)
    

        #Achsenlimits
        if x_max >= x_min: 
            self.ax.set_xlim(x_min, x_max)
        if y_max != y_min:
            self.ax.set_ylim(y_min, y_max)

        # Daten plotten

        if self.x_data is not None and self.y_data is not None:

            x_geplottet = self.x_data.copy()
            y_geplottet = self.y_data.copy()
            
            x_formel = self.x_trafo_input.text().strip().replace("^", "**") # strip nimmt Leerzeichen weg
            if x_formel:
                try: 
                    res = self.transformiere_daten(x_formel, self.x_data, self.y_data)
                    if res is not None:
                        x_geplottet = res
                    
                
                except Exception:
                    pass

            y_formel = self.y_trafo_input.text().strip().replace("^", "**")
            if y_formel:
                try:
                    res = self.transformiere_daten(y_formel, self.x_data, self.y_data)
                    if res is not None:
                        y_geplottet = res
                    
                    
                except Exception:
                    pass

            #Abspeichern der aktuellen Plot daten für die Achsenlimits
            self.current_x = x_geplottet
            self.current_y = y_geplottet

            # Prüfen, ob Y-Errorbars da sind
            if self.y_err is not None:
                self.ax.errorbar(
                    x_geplottet, 
                    y_geplottet, 
                    yerr=self.y_err,
                    xerr=self.x_err,
                    marker=current_markerstyle, 
                    markersize=6, 
                    color=color, 
                    linestyle=current_linestyle, 
                    capsize=3, 
                    label=label
                )
            else:
                self.ax.plot(
                    x_geplottet, 
                    y_geplottet, 
                    marker=current_markerstyle, 
                    markersize=8, 
                    color=color, 
                    linestyle=current_linestyle, 
                    label=label
                )


            # Fit integration -----------------------------------------------------------------------------------------
            fit_typ = self.polyfit_combo.currentData()
            polyfit_label = self.polyfit_input_label.text()

            if fit_typ is not None:
                try:
                    self.polyfit_input_label.setEnabled(True) #Eingabefeld aktivieren fürs Label
                    # Ausreichend Punkte für eine glatte Kurve generieren
                    x_fit_smooth = np.linspace(min(x_geplottet), max(x_geplottet), 200)

                    #Polynom Fits-------------------------------------
                    if str(fit_typ).startswith("poly_"):
                        grad = int(fit_typ.split("_")[1])
                        popt, pcov = np.polyfit(x_geplottet, y_geplottet, grad, cov = True)
                        y_fit_smooth = np.polyval(popt, x_fit_smooth)

                        formel_text = self.erstelle_fit_formel(popt, pcov)
                        self.polyfit_heading_label.setText(f"<b>Fit</b>: {formel_text}")
                    # Nicht lineare Fits (SciPy Curve Fits)

                    else:
                    # Modell-Funktion wählen
                        if fit_typ == "exp":
                            func = self.model_exp
                            p0 = [1.0, 0.1] # Startwerte für Iteration
                        elif fit_typ == "andrade":
                            func = self.model_andrade
                            p0 = [1.0, 1.0]
                        elif fit_typ == "saettigung":
                            func = self.model_saettigung
                            p0 = [1.0, 0.1]

                        # 1. Curve Fit durchführen
                        popt, pcov = curve_fit(func, x_geplottet, y_geplottet, p0 = p0, maxfev= 5000)
                        A, B = popt

                        #Fehler aus der Kovarianzmatrix holen
                        perr = np.sqrt(np.diag(pcov))
                        err_A, err_B = perr[0], perr[1]

                        #3. Y Werte für die Ausgleichsgerade berechnen
                        y_fit_smooth = func(x_fit_smooth, A, B) # was macht das?

                        str_A = self.format_html_zahl(A)
                        str_B = self.format_html_zahl(B)

                        # 4. Formel und Parameter mitsamt Unsicherheiten (±) im Header ausgeben
                        if fit_typ == "exp":
                            formel_html = f"y = {str_A} · e<sup>{str_B}x</sup>"
                        elif fit_typ == "andrade":
                            formel_html = f"y = {str_A} · e<sup>{str_B}/x</sup>"
                        elif fit_typ == "saettigung":
                            formel_html = f"y = {str_A} · (1 - e<sup>-{str_B}x</sup>)"

                        str_A_err = self.format_html_zahl(A, err_A)
                        str_B_err = self.format_html_zahl(B, err_B)
                        param_html = f"<br><small>A = {str_A_err}, B = {str_B_err}</small>"
                        self.polyfit_heading_label.setText(f"<b>Fit:</b> {formel_html}{param_html}")
                    # Fit-Linie zeichnen
                    self.ax.plot(x_fit_smooth, y_fit_smooth, color="red", linestyle="--", label = polyfit_label)

                except Exception as e:
                    self.polyfit_heading_label.setText("Fit fehlgeschlagen (Konvergenzfehler)")
            else:
                self.polyfit_heading_label.setText("Ausgleichskurve / Fit")
                self.polyfit_input_label.setEnabled(False)
                self.polyfit_input_label.blockSignals(True)
                self.polyfit_input_label.clear()
                self.polyfit_input_label.blockSignals(False)
                
            # Nur eine Legende zeichnen, wenn Daten geladen sind und mindestens ein Label existiert
            handles, labels = self.ax.get_legend_handles_labels()
            if handles:
                self.ax.legend(fontsize=fontsize * 0.75)

        self.canvas.draw_idle()

    def choose_color(self):
        # Öffnet den Betriebssystem-Farbdialog mit der aktuellen Farbe als Startwert
        color = QColorDialog.getColor(self.plot_color, self, "Farbe für Plot auswählen")

        if color.isValid():
            self.plot_color = color #wenn wahr, übernehme die Farbe
            self.update_color_button_style()
            self.plot_aktualisieren() # Plot neu Zeichnen

    def update_color_button_style(self):
        # Baut einen CSS-String, um den Button einzufärben und die Schrift lesbar zu halten
        hex_code = self.plot_color.name()
        self.color_button.setStyleSheet(
            f"background-color: {hex_code}; color: white; font-weight: bold; border-radius: 4px; padding: 6px;"
        )

    def auto_limits(self):

        # Falls schon transformierte Daten da sind, nimm sie, sonst die Rohdaten:
        x_vals = self.current_x if self.current_x is not None else self.x_data
        y_vals = self.current_y if self.current_y is not None else self.y_data

        if x_vals is not None and y_vals is not None:
            randx = np.ptp(x_vals) * 0.1 #ptp berechnet die Spanne, also den Absolutbetrag
            randy = np.ptp(y_vals) * 0.1
            
            if randx == 0: randx = 1.0
            if randy == 0: randy = 1.0

            self.x_min_input.setValue(float(min(x_vals) - randx))
            self.x_max_input.setValue(float(max(x_vals) + randx))
            self.y_min_input.setValue(float(min(y_vals) - randy))
            self.y_max_input.setValue(float(max(y_vals) + randy))

    def transformiere_daten(self, formel_text, x_arr, y_arr):
        if not formel_text.strip():
            return None
        

        #Spezialfall: Differenzenquotient
        if "diff(y)/diff(x)" in formel_text or "dy/dx" in formel_text:
            return np.gradient(y_arr, x_arr)
        
        if formel_text.strip() in ["diff(y)", "dy", "grad(y)"]:
            # Falls x gleichabständige Zeiten t sind:
            return np.gradient(y_arr)

        #Mathe Symbole definieren
        x, y, pi = sp.symbols("x y pi")

        #Was erlaubt sein soll:
        transformations = standard_transformations + (implicit_multiplication_application,) # Liste + einzelne Funktion addieren, sonst hätten wir falsche Dimensionen!
        expr = parse_expr(formel_text, transformations=transformations)

        mathe_funktion = sp.lambdify((x,y,pi), expr, modules = ["numpy"]) #args, expr, modules

        ergebnis = mathe_funktion(x_arr, y_arr, np.pi)

        # WICHTIGER TRICK: Falls eine Konstante eingegeben wurde (z.B. nur "5"), 
        # liefert NumPy eine einzelne Zahl zurück. Wir machen daraus wieder ein Array mit passender Länge:
        if isinstance(ergebnis, (int, float, np.number)):
            ergebnis = np.full_like(x_arr, ergebnis)

        return ergebnis

    def load_file(self):
        dateiname, _ = QFileDialog.getOpenFileName(
        self, "Excel-Datei auswählen", "", "Excel-Dateien (*.xlsx *.xls)") # *xlsx etc. ist ein Filter, nur diese Dateien können ausgewählt werden! 
        if dateiname: # if dateiname is not none
            print(dateiname)

            try: 
                datafile = pd.read_excel(dateiname)
                datafile_numpy = datafile.to_numpy(dtype=float)
                self.x_data = datafile_numpy[:,0]
                self.y_data = datafile_numpy[:,1]
                #Wenn das gut geht, Plot aktualisieren:

                #Einmalig beim Laden die Limits anpassen
                # Limits berechnen
                randx = np.ptp(self.x_data) * 0.1
                randy = np.ptp(self.y_data) * 0.1
                
                if randx == 0: randx = 1.0
                if randy == 0: randy = 1.0

                # Signale kurz blockieren, damit nicht 4x hintereinander plot_aktualisieren aufgerufen wird
                self.x_min_input.blockSignals(True)
                self.x_max_input.blockSignals(True)
                self.y_min_input.blockSignals(True)
                self.y_max_input.blockSignals(True)

                self.x_min_input.setValue(float(min(self.x_data) - randx))
                self.x_max_input.setValue(float(max(self.x_data) + randx))
                self.y_min_input.setValue(float(min(self.y_data) - randy))
                self.y_max_input.setValue(float(max(self.y_data) + randy))

                # Signale wieder aktivieren
                self.x_min_input.blockSignals(False)
                self.x_max_input.blockSignals(False)
                self.y_min_input.blockSignals(False)
                self.y_max_input.blockSignals(False)

                # Jetzt EINMAL sauber den Plot neu zeichnen
                self.plot_aktualisieren()

            except ValueError:
                # Dieser Block wird nur ausgeführt, wenn der Text nicht zu Zahlen (float) umgewandelt werden konnte
                QMessageBox.critical(self,  "Datenfehler",  "Die Excel-Datei enthält ungültige Zeichen (z. B. Text).\nBitte stelle sicher, dass in den ersten beiden Spalten nur Zahlen stehen!"
                )
                # Speicher wieder leeren, damit kein halber Müll geplottet wird
                self.x_data = None
                self.y_data = None
                
            except Exception as e:
                # Fängt alle anderen Fehler ab (z. B. Excel-Datei hat nur 1 Spalte oder ist kaputt)
                QMessageBox.critical(
                    self,   "Allgemeiner Fehler",   f"Details zum Fehler:\n{type(e).__name__}: {str(e)}"
                )

    def save_plot(self):
            # Öffnet den System-Speicherdialog mit Dateityp-Filtern
            dateiname, gewaehlter_filter = QFileDialog.getSaveFileName(
                self,
                "Plot speichern",
                "mein_plot.png",  # Standard-Dateiname
                "PNG Bild (*.png);;PDF Dokument (*.pdf);;SVG Vektorgrafik (*.svg);;JPEG Bild (*.jpg)"
            )

            # Wenn der Nutzer nicht auf "Abbrechen" geklickt hat:
            if dateiname:
                try:
                    # Speichert die Figure in hoher Auflösung (300 DPI für gestochen scharfen Druck)
                    # bbox_inches='tight' schneidet unnötige weiße Ränder außen sauber ab
                    self.figure.savefig(dateiname, dpi=300, bbox_inches='tight')

                    # Erfolgsmeldung anzeigen
                    QMessageBox.information(
                        self, 
                        "Erfolg", 
                        f"Der Plot wurde erfolgreich gespeichert unter:\n{dateiname}"
                    )

                except Exception as e:
                    # Fehlermeldung falls beim Schreiben etwas schiefgeht
                    QMessageBox.critical(
                        self, 
                        "Fehler beim Speichern", 
                        f"Die Datei konnte nicht gespeichert werden:\n{str(e)}"
                    )

    def erstelle_fit_formel(self, coeffs, pcov):
        grad = len(coeffs) - 1
        label = r"y = "
        # Standardfehler aus der Kovarianzmatrix berechnen
        # Falls pcov nicht berechnet werden konnte (z.B. zu wenige Punkte), Fallback auf Nullen
        if pcov is not None and isinstance(pcov, np.ndarray):
            errors = np.sqrt(np.diag(pcov))
        else:
            errors = [0.0] * len(coeffs)

        for i, c in enumerate(coeffs):
            power = grad - i
            err = errors[i]

            if abs(c) < 1e-10:
                continue

            if i > 0:
                if c >= 0:
                    label += " + "
                else:
                    label += " - "
                    c = abs(c)


            #Formel für den Text mit Unsicherheit aufbauen
            term_str = f"({c:.3g} ± {err:.3g})"

            if power == 0:
                label += f"{term_str}"

            elif power == 1:
                label += f"{term_str}x"

            else:
                label += f"{term_str}x<sup>{power}</sup>"

        return label

    def erstelle_hilfe_button(self, hilfe_text):
            btn = QPushButton("?")
            btn.setFixedSize(18, 18)  # Kompakt und unaufdringlich
            btn.setToolTip(hilfe_text)
            btn.setCursor(Qt.CursorShape.WhatsThisCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    color: #333333;
                    border-radius: 9px;
                    font-weight: bold;
                    font-size: 11px;
                    border: 1px solid #b0b0b0;
                }
                QPushButton:hover {
                    background-color: #1f77b4;
                    color: white;
                }
            """)
            return btn
    
    # Mathematical fit models
    @staticmethod
    def model_exp(x, A, B):
        return A * np.exp(B * x)

    @staticmethod
    def model_andrade(x, A, B):
        return A * np.exp(B / x)

    @staticmethod
    def model_saettigung(x, A, B):
        return A * (1 - np.exp(-B * x))

    def format_html_zahl(self, val, err=None):
            """Formatiert eine Zahl (und optional ihren Fehler) sauber für HTML mit x10^n."""
            def single_fmt(x):
                if x == 0:
                    return "0"
                abs_x = abs(x)
                # Wenn sehr klein oder sehr groß -> wissenschaftliche Schreibweise mit 10^n
                if abs_x < 0.0001 or abs_x >= 100000:
                    exponent = int(np.floor(np.log10(abs_x)))
                    mantisse = x / (10**exponent)
                    return f"{mantisse:.2f} · 10<sup>{exponent}</sup>"
                else:
                    return f"{x:.3g}"

            txt = single_fmt(val)
            if err is not None:
                err_txt = single_fmt(err)
                txt += f" ± {err_txt}"
            return txt

    def berechne_groesstfehler(self, formel_text, werte_dict, unsicherheiten_dict):
        formel_sauber = formel_text.replace("^", "**") #Latex hochschreibweise integrierens
        expr = sp.parse_expr(formel_sauber, transformations=standard_transformations + (implicit_multiplication_application,))

        #Variablen im Ausdruck erkennen (ohne pi etc.)
        variablen_symbole = [s for s in expr.free_symbols if s.name != "pi"]

        f_num = sp.lambdify(variablen_symbole, expr, modules = ["numpy"])
        
        #Argumente in passende Reihenfolg für lambidy zusammenstellen und einem dictionary hinzufügen

        args_werte = [werte_dict[s.name] for s in variablen_symbole]
        funktions_wert = f_num(*args_werte) #ruft f_num von oben auf und wertet die Funktion aus

        #Größtfehler berechnen: Formel siehe Skript

        gesamt_fehler = 0.0
        for sym in variablen_symbole:
            var_name = sym.name

            #Partielle Ableitung bilden: df / d(var
            partielle_ableitung = sp.diff(expr, sym) #Bildet die symbolische partielle ableitung der Formel "expr" nach der aktuellen Variable "sym"
            df_num = sp.lambdify(variablen_symbole, partielle_ableitung, modules = ["numpy"]) #Nimmt den symboplischen Ausdruck und übersetzt ihn in eine Numpy Funktion

            #Betrag der Ableitung an der stelle auswerten
            abl_wert = np.abs(df_num(*args_werte)) #Jetzt werden die Messwerte eingesetzt, * entpackt eine Liste
            u_var = unsicherheiten_dict[var_name]
            #Aufsummieren

            gesamt_fehler+= abl_wert * u_var

        # FIX: Wenn der Funktionswert ein Array ist (z.B. x_data), aber der Fehler eine Zahl (z.B. 0.2),
        # bringe den Fehler auf dieselbe Array-Form!
        if isinstance(funktions_wert, np.ndarray) and isinstance(gesamt_fehler, (int, float, np.number)):
            gesamt_fehler = np.full_like(funktions_wert, gesamt_fehler)

        elif isinstance(funktions_wert, (int, float, np.number)):
            if self.x_data is not None:
                funktions_wert = np.full_like(self.x_data, funktions_wert)
                gesamt_fehler = np.full_like(self.x_data, gesamt_fehler)

        return funktions_wert, gesamt_fehler

    def oeffne_groesstfehler_dialog(self):
            # 1. Dialog erstellen und unsere Rechenmethode direkt als Argument mitgeben
            dialog = GroesstfehlerDialog(
                parent=self, 
                x_data=self.x_data, 
                y_data=self.y_data, 
                rechen_funktion=self.berechne_groesstfehler
            )

            # 2. Öffnen und auf den Klick auf OK warten
            if dialog.exec() == QDialog.DialogCode.Accepted:
                formel, werte, unsicherheiten = dialog.get_daten()
                if not formel:
                    return

                # Größtfehler berechnen
                f_neu, f_err = self.berechne_groesstfehler(formel, werte, unsicherheiten)

                # Prüfen, welcher Radio-Button im Dialog gewählt wurde
                if dialog.radio_y.isChecked():
                    self.y_data = f_neu
                    self.y_err = f_err
                    self.plot_aktualisieren()

                elif dialog.radio_x.isChecked():
                    self.x_data = f_neu
                    self.x_err = f_err
                    self.plot_aktualisieren()

                elif dialog.radio_nur_ausgabe.isChecked():
                    # Daten im Plot bleiben unverändert, die Berechnung war nur für die Tabelle gedacht
                    print("Berechnung erfolgreich durchgeführt (ohne Plot-Änderung).")

            else:
                print("Größtfehler-Berechnung abgebrochen.")

class GroesstfehlerDialog(QDialog):
    #grundgerüst wird aufgebaut
    def __init__(self, parent=None, x_data=None, y_data=None, rechen_funktion = None):
        super().__init__(parent)
        self.setWindowTitle("Größtfehler-Rechner & Datenauswertung")
        self.resize(650, 600)

        self.x_data = x_data
        self.y_data = y_data
        self.rechen_funktion = rechen_funktion

        # Hauptlayout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 1. Zielauswahl (Wohin sollen die berechneten Daten?)
        self.layout.addWidget(QLabel("<b>Ziel der Berechnung:</b>"))
        ziel_layout = QHBoxLayout()
        self.radio_y = QRadioButton("Y-Daten & Y-Errorbar (vertikal)")
        self.radio_x = QRadioButton("X-Daten & X-Errorbar (horizontal)")
        self.radio_nur_ausgabe = QRadioButton("Nur Berechnen (Tabelle / Einzelwert)")
        
        self.radio_y.setChecked(True) # Standardmäßig Y wählen
        
        ziel_layout.addWidget(self.radio_y)
        ziel_layout.addWidget(self.radio_x)
        ziel_layout.addWidget(self.radio_nur_ausgabe)
        self.layout.addLayout(ziel_layout)

        # 2. Formeleingabe
        self.layout.addWidget(QLabel("<b>Mathematische Formel:</b>"))
        self.formel_input = QLineEdit()
        self.formel_input.setPlaceholderText("z. B. 4 * pi^2 * (m * V0) / (A^2 * p * tau^2)")
        self.layout.addWidget(self.formel_input)

        # 3. Dynamischer Bereich für Variablen-Eingaben
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.layout.addWidget(self.form_widget)

        self.inputs_werte = {}
        self.inputs_unsicherheiten = {}

        # 4. Live-Ergebistabelle
        self.layout.addWidget(QLabel("<b>Ergebnis- & Datentabelle (Live-Vorschau):</b>"))
        self.tabelle = QTableWidget()
        self.layout.addWidget(self.tabelle)

        # 5. OK / Abbrechen Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        # Signale verbinden
        self.formel_input.textChanged.connect(self.aktualisiere_variablen_felder) # Das hier ist essentiell
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
    
    def aktualisiere_variablen_felder(self):
        #Altes Formular leeren (alle Zeilen löschen)
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)
        
        self.inputs_werte.clear()
        self.inputs_unsicherheiten.clear()

        text = self.formel_input.text().strip()
        if not text:
            return
        try: 
            # SymPy Ausdruck parsen & Variablen ermitteln #nochmal das ganze? Haben wir das nicht oben in unserer ersten Klasse schon in berechne_größtfehler?
            formel_sauber = text.replace("^", "**")
            expr = sp.parse_expr(formel_sauber, transformations=standard_transformations + (implicit_multiplication_application,))
            variablen = sorted([s.name for s in expr.free_symbols if s.name != "pi"])

            # Für jede Variable Eingabefelder im Formlayout anlegen
            for var in variablen:
                #Feld für den Wert (Zahl oder "x"/"y")
                val_input = QLineEdit()
                if var.lower() == "x" or var.lower() == "y":
                    val_input.setText(var)
                val_input.setPlaceholderText(f"Wert für {var} (z.B. 1.5 oder x)")

                #Feld für die Unsicherheit
                err_input = QLineEdit()
                err_input.setPlaceholderText(f"Delta {var} (z.B. 0.01)")

                val_input.textChanged.connect(self.aktualisiere_tabelle_live)
                err_input.textChanged.connect(self.aktualisiere_tabelle_live)

                #Speicher Dictionarys befüllen

                self.inputs_werte[var] = val_input
                self.inputs_unsicherheiten[var] = err_input
                #Ins QFormLayout einfügen 
                self.form_layout.addRow(QLabel(f"<b>{var}:</b>"), val_input)
                self.form_layout.addRow(QLabel(f"Δ{var}:"), err_input)

            self.aktualisiere_tabelle_live()

        except Exception:
            #falls die Formel noch getippt wird oder Ähnliches
            pass

    def get_daten(self):
        """Liest alle Eingabefelder aus und liefert die Dictionaries und die Formel zurück."""
        werte = {}
        unsicherheiten = {}

        for var, input_widget in self.inputs_werte.items():
            txt = input_widget.text().strip()

            # Wenn im Feld "x" (oder leer gelassen) steht und x_data vorhanden ist -> Messdaten nehmen
            if (txt.lower() == var.lower() or txt == "") and var.lower() == "x" and self.x_data is not None:
                werte[var] = self.x_data
            # Analog für "y"
            elif (txt.lower() == var.lower() or txt == "") and var.lower() == "y" and self.y_data is not None:
                werte[var] = self.y_data
            else: 
                try:
                    werte[var] = float(txt)
                except ValueError:
                    # Fallback: Falls der Nutzer z. B. nur "x" eingetippt hat
                    if var.lower() == "x" and self.x_data is not None:
                        werte[var] = self.x_data
                    elif var.lower() == "y" and self.y_data is not None:
                        werte[var] = self.y_data
                    else:
                        werte[var] = 0.0

        for var, input_widget in self.inputs_unsicherheiten.items():
            txt = input_widget.text().strip()
            try: 
                unsicherheiten[var] = float(txt)
            except ValueError:
                unsicherheiten[var] = 0.0

        return self.formel_input.text().strip(), werte, unsicherheiten

    def aktualisiere_tabelle_live(self):
            formel, werte, unsicherheiten = self.get_daten()
            if not formel:
                return

            try:
                if self.rechen_funktion is None:
                    return
                
                f_val, f_err = self.rechen_funktion(formel, werte, unsicherheiten)

                # Sicherstellen, dass f_val und f_err Arrays sind
                if isinstance(f_val, (int, float, np.number)):
                    n_rows = len(self.x_data) if self.x_data is not None else 1
                    f_val = np.full(n_rows, f_val)
                    f_err = np.full(n_rows, f_err)

                n_zeilen = len(f_val)
                self.tabelle.setRowCount(n_zeilen)
                self.tabelle.setColumnCount(5)
                self.tabelle.setHorizontalHeaderLabels(["Index", "X-Data", "Y-Data", "Ergebnis f", "Fehler Δf"])

                for i in range(n_zeilen):
                    x_str = f"{self.x_data[i]:.4g}" if self.x_data is not None and i < len(self.x_data) else "-"
                    y_str = f"{self.y_data[i]:.4g}" if self.y_data is not None and i < len(self.y_data) else "-"
                    res_str = f"{f_val[i]:.4g}"
                    err_str = f"± {f_err[i]:.4g}"

                    self.tabelle.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                    self.tabelle.setItem(i, 1, QTableWidgetItem(x_str))
                    self.tabelle.setItem(i, 2, QTableWidgetItem(y_str))
                    self.tabelle.setItem(i, 3, QTableWidgetItem(res_str))
                    self.tabelle.setItem(i, 4, QTableWidgetItem(err_str))

            except Exception:
                # Ignorieren, falls Formel oder Felder noch unvollständig ausgefüllt sind
                pass

# --- Startpunkt der Anwendung ---
if __name__ == "__main__": # Alles unter der if Abfrage wird nur dann ausgefsührt, wenn ich die Datei direkt starte
    app = QApplication(sys.argv)
    fenster = MeinPlotterApp() # Hier wird unser Bauplan angewendet.
    fenster.show()
    sys.exit(app.exec()) # App exec ist eine Endlosschleife, wenn ich das Programm schließe gibt es 0 zurück, wenn es abstürzt 1 