# Fehler die es zu beheben gibt:
#Was, wenn ich fehlerbalken für x und y haben will? Weil beide messgrößen behaftet sind? Funktioniert nicht. 
# Es nimmt x werte und fehler für die y achse an. 
#Ersetzt das ganze nun meine "y/x" Transformations-Box?

import sys
import os
import pandas as pd
import numpy as np
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
# 1. Zwingt Matplotlib dazu, PySide6 statt PyQt6 zu verwenden!
os.environ["QT_API"] = "pyside6"


import matplotlib
matplotlib.use("QtAgg")
import matplotlib.ticker as ticker

# 2. PySide6 Imports
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QTableWidget, QTableWidgetItem, QWidget, QDialog, QFormLayout, QDialogButtonBox, QSlider, QCheckBox, QStyledItemDelegate, QTabWidget, QComboBox, QColorDialog,  QDoubleSpinBox, QMessageBox, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel  # H = Horizontal,  V = Vertikal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure





#Wörterbuch anlegen

TRANSLATIONS = {
    "de": {
        "title": "Protokollix - © 2026",
        "tab_general": "Allgemeines",
        "tab_math": "Rechner",
        "tab_style": "Style",
        "tab_import": "Daten",
        "btn_excel": "Öffne Excel / CSV",
        "btn_save": "Plot speichern unter...",
        "btn_groesstfehler": "Datenmanipulation | Fehlerrechnung",
        "btn_mittelwert": "Mittelwertrechner",
        "lbl_active_ds": "Aktiver Datensatz (Y):",
        "lbl_title_input": "Plot-Titel (LaTeX-Support):",
        "lbl_seitenverhältnis": "Seitenverhältnis:",
        "lbl_fontsize": "Schriftgröße:",
        "lbl_x_axis": "X-Achse (LaTeX Support):",
        "lbl_y_axis": "Y-Achse (LaTeX Support):",
        "lbl_x_axis_limits": "X-Achsenlimits",
        "lbl_fit": "Ausgleichskurve / Fit:",
        "lbl_y_axis_limits": "Y-Achsenlimits",
        "btn_autolimits": "Achsenlimits automatisch anpassen",
        "data_label": "Datenlabel (LaTeX Support):",
        "y_data_combo": "Keine Daten geladen",
        "lbl_mathematicaloperation": "Mathematische Operationen und Tools:",
        "lbl_achsenmanipulation": "Achsen Maßstab:",
        # --- Größtfehler-Dialog (DE) ---
        "gf_title": "Datenauswertung & Größtfehlerrechner",
        "gf_target": "Ziel der Berechnung:",
        "gf_radio_y": "Y-Daten & Y-Errorbar (vertikal)",
        "gf_radio_x": "X-Daten & X-Errorbar (horizontal)",
        "gf_radio_none": "Nur Berechnen (Tabelle / Einzelwert)",
        "gf_rendered_formula": "Mathematische Formel (gerendert):",
        "gf_rendered_ph": "Die gerenderte Formel erscheint hier...",
        "gf_formula_label": "Mathematische Formel:",
        "gf_formula_ph": "z. B. 4 * pi^2 * (m * V0) / (A^2 * p * tau^2)",
        "gf_btn_excel": "Importiere Y-Unsicherheiten als Excel",
        "gf_preview_table": "Ergebnis- & Datentabelle (Live-Vorschau):",
        "gf_val_ph": "Wert für {var} (z.B. 1.5 oder x)",
        "gf_err_ph": "Delta {var} (z.B. 0.01)",
        "btn_loadsinglecolumn": "Lade einzelne Datenspalte (Nur bei (Tabelle / Einzelwert) verfügbar)",
        "menubar_app": "Protokollix",
        "menubar_edit": "Bearbeiten",
        "menu_about": "Über Protokollix",
        "about_text": (
            "<h2>Protokollix</h2>"
            "<b>© 2026 Jakob Breinl</b><br><br>"
            "Ein Werkzeug zur schnellen Datenauswertung, Plot-Erstellung und Größtfehlerberechnung "
            "für physikalische Praktika und wissenschaftliche Berichte, entwickelt aus Langeweile in den Sommerferien :D .<br><br>"
            "<i>Entwickelt mit Python unter Zuhilfenahme der Bibliotheken PySide6, Pandas, Numpy, Matplotlib &amp; SymPy.</i> <br><br>"
            "Verbesserungssvorschläge, Programmfehler etc. bitte per Mail an <i> jakob.breinl@edu.uni-graz.at </i>"),
        "Mittelwert_title": "Mittelwert-Rechner",
        "Mittelwert_header": "Mittelwert & Standardabweichung berechnen",
        "Mittelwert_open": "Excel für Mittelwerte laden",
        "Mittelwert_save": "Mittelwerte als Excel speichern",
        "lbl_color": "Linien und Markerfarbe:",
        "choose_color": "Farbe wählen",
        "initial_title": "keine Daten geladen",
        "initial_title": "noch keine Daten geladen",
        "default_x_axis": "X-Achse:",
        "default_y_axis": "Y-Achse:",
        "btn_xreset": "X-Daten zurücksetzen",
        "btn_yreset": "Y-Daten zurücksetzen",
        "mean_preview_table": "Daten/Ergebnistabelle",
        "lbl_limitkommastellen": "Anzahl der Nachkommastellen der Limits:",
        "btn_save_data": "Daten speichern",
        "lbl_legendposition": "Legenden Position:",
        "lbl_dpi": "DPI beim Export:",
        "lbl_datentabelle": "Datentabelle",
        "btn_deletealldata": "Alle Daten löschen"

    },
    "en": {
        "title": "Protokollix - © 2026",
        "tab_general": "General",
        "tab_math": "Calculator",
        "tab_style": "Style",
        "tab_import": "Data",
        "btn_excel": "Open Excel / CSV",
        "btn_save": "Save Plot as...",
        "btn_groesstfehler": "Data Manipulation | Error Calculation",
        "btn_mittelwert": "Mean Calculator",
        "lbl_active_ds": "Active Dataset (Y):",
        "lbl_title_input": "Plot Title (LaTeX Support):",
        "lbl_seitenverhältnis": "Aspect Ratio:",
        "lbl_fontsize": "Fontsize:",
        "lbl_x_axis": "X-Axis Label (LaTeX Support):",
        "lbl_y_axis": "Y-Axis Label (LaTeX Support):",
        "lbl_x_axis_limits": "Set X-Limits",
        "lbl_fit": "Regression Curve / Fit:",
        "lbl_y_axis_limits": "Set Y-Limits",
        "btn_autolimits": "Adjust Axis Limits",
        "data_label": "Set Datalabel (LaTeX Support):",
        "y_data_combo": "No data available",
        "lbl_mathematicaloperation": "Data Analysis",
        "lbl_achsenmanipulation": "Axis Scaling:",
        # --- Größtfehler-Dialog (EN) ---
        "gf_title": "Data Evaluation & Error Calculator",
        "gf_target": "Target of Calculation:",
        "gf_radio_y": "Y-Data & Y-Errorbar (vertical)",
        "gf_radio_x": "X-Data & X-Errorbar (horizontal)",
        "gf_radio_none": "Calculation Only (Table / Single Value)",
        "gf_rendered_formula": "Mathematical Formula (rendered):",
        "gf_rendered_ph": "The rendered formula will appear here...",
        "gf_formula_label": "Mathematical Formula:",
        "gf_formula_ph": "e.g. 4 * pi^2 * (m * V0) / (A^2 * p * tau^2)",
        "gf_btn_excel": "Import Y-Errors from Excel",
        "gf_preview_table": "Result & Data Table (Live Preview):",
        "gf_val_ph": "Value for {var} (e.g. 1.5 or x)",
        "gf_err_ph": "Delta {var} (e.g. 0.01)",
        "btn_loadsinglecolumn": "Load single data column",
        "menubar_app": "Protokollix",
        "menubar_edit": "Edit",
        "menu_about": "About Protokollix",
        "about_text": (
            "<h2>Protokollix</h2>"
            "<b>© 2026 Jakob Breinl</b><br><br>"
            "A tool for fast data evaluation, plotting, and maximum error calculation "
            "for physics lab courses and scientific reports, developed out of boredom during summer break. .<br><br>"
            "<i>Developed with Python using the PySide6, Pandas, NumPy, Matplotlib &amp; SymPy libraries.</i> <br><br>"
            "Suggestions for improvement, bug reports, etc. please via email to <i>jakob.breinl@edu.uni-graz.at</i>"
        ),
        "Mittelwert_title": "mean calculator",
        "Mittelwert_header": "Calculate Mean & Mean Error",
        "Mittelwert_open": "Open Excel",
        "Mittelwert_save": "Save as Excel",
        "lbl_color": "Colour:",
        "choose_color": "Choose Colour",
        "initial_title": "No data available",
        "default_x_axis": "X-Axis",
        "default_y_axis": "Y-Axis",
        "btn_xreset": "Reset X-Data",
        "btn_yreset": "Reset Y-Data",
        "mean_preview_table": "Data Table & Results:",
        "lbl_limitkommastellen": "Number of Decimal Points for the Limits:",
        "btn_save_data": "Save Data",
        "lbl_legendposition": "Legend Position:",
        "lbl_dpi": "DPI for Export:",
        "lbl_datentabelle": "Data Table",
        "btn_deletealldata": "Delete Data"
        
    }
}
#Vorläufige Hauptfunktion

class MeinPlotterApp(QMainWindow): # Vererbung, also das übergeben von QMainWindow gibt der Klasse alle Funktionen, die QMainWindow auch hat. 
    def __init__(self):
        super().__init__()

        self.aktuelle_sprache = "de" #Sprache festlegen
    # Fenstertitel und Anfangsgröße festlegen
        self.setWindowTitle("Protokollix - © 2026 Jakob Breinl")
        self.setGeometry(100, 100, 1200, 800)

        # Speicher für die geladenen Daten (anfangs leer)
        self.x_data = None
        #Rohdaten fürs Zurücksetzen anlegen:

        self.y_dict_raw = {}
        self.x_data_raw = None
        self.y_dict= {} # Dicitionary für beliebig viele y Spalten
        self.y_styles = {}  # Speichert Stile pro Y-Spalte: {"Warmwasser": {"color": "#1f77b4", "linestyle": "-", ...}}
        self.x_err = None  # Neu!
        self.y_err = None # das bleibt gleich?
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


    # Globale Auswahlschachtel für die aktive Y-Spalte
        
        layout_y_auswahl = QHBoxLayout()
        self.label_aktiverDatensatz = QLabel()
        layout_y_auswahl.addWidget(self.label_aktiverDatensatz)
        
        self.aktive_y_combo = QComboBox()
        self.aktive_y_combo.addItem("No Data available")
        layout_y_auswahl.addWidget(self.aktive_y_combo)
        self.menu_hilfebutton = MeinPlotterApp.erstelle_hilfe_button(self.get_hilfetext())
        layout_y_auswahl.addWidget(self.menu_hilfebutton)
        
        # Ganz oben ins Haupt-Bedienfeld einfügen
        layout_tab_label.addLayout(layout_y_auswahl) # Oder ganz oben im Data/Style-Tab


    #Seitenverhältniss

        self.label_Seitenverhältnis = QLabel()
        layout_tab_label.addWidget(self.label_Seitenverhältnis)
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
        self.schriftgroesse_label = QLabel()
        layout_tab_label.addWidget(self.schriftgroesse_label)

        self.fontsize_slider = QSlider(Qt.Orientation.Horizontal)

        self.fontsize_slider.setRange(6,25) # Range
        self.fontsize_slider.setValue(12) # Startwert

        self.fontsize_slider.setSingleStep(1) #1er Schritte als Skalierung
        layout_tab_label.addWidget(self.fontsize_slider)


        #Titel Eingabe
        self.plot_title_label = QLabel()
        layout_tab_label.addWidget(self.plot_title_label)

        self.titel_input = QLineEdit() #Self ist hier super zentral, weil ich auf den text ja später noch zugreifen will! 
        self.titel_input.setPlaceholderText("z.B. Pendelversuch")
        layout_tab_label.addWidget(self.titel_input)


        # 2. X-Achse-eingabe
        self.x_achsen_label = QLabel()
        layout_tab_label.addWidget(self.x_achsen_label)
        self.x_label_input = QLineEdit()
        self.x_label_input.setPlaceholderText("z.B. Zeit t / s")
        layout_tab_label.addWidget(self.x_label_input)


        # 3. Y-Achse-Eingabe
        self.y_achsen_label = QLabel()
        layout_tab_label.addWidget(self.y_achsen_label)
        self.y_label_input = QLineEdit()
        self.y_label_input.setPlaceholderText("z.B. Auslenkung x / m")
        layout_tab_label.addWidget(self.y_label_input)

        #--------------------------------------------------------------------------------------
        #Achenlimits

        # X achsen Limit
        self.x_limit_label = QLabel()
        layout_tab_label.addWidget(self.x_limit_label)
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
        self.y_limit_label = QLabel()
        layout_tab_label.addWidget(self.y_limit_label)
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


        #Regler für die Nachkommestellen der Achsenlimits
        self.lbl_limitskommastellen = QLabel()
        layout_tab_label.addWidget(self.lbl_limitskommastellen)
        self.limitskommastellen_slider = QSlider(Qt.Orientation.Horizontal)

        self.limitskommastellen_slider.setRange(0,10) # Range
        self.limitskommastellen_slider.setValue(2) # Startwert

        self.limitskommastellen_slider.setSingleStep(1) #1er Schritte als Skalierung
        layout_tab_label.addWidget(self.limitskommastellen_slider)

        self.update_limitkommastellen()
        #--------------------------------------------------------------------------------------

        # Button zum automatischen Anpassen der Axen anlegen
        self.achsenlimits_anpassen = QLabel()
        self.achsenlimit_button = QPushButton(self.achsenlimits_anpassen)
        #Schriftgröße bearbeiten
        font = self.achsenlimit_button.font()
        font.setPointSize(11)
        self.achsenlimit_button.setFont(font)

        layout_tab_label.addWidget(self.achsenlimit_button)

        #Legende
        self.datenlabel_label = QLabel()
        layout_tab_label.addWidget(self.datenlabel_label)
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


# Polyfit
        self.polyfit_heading_label = QLabel()
        trafo_tab_layout.addWidget(self.polyfit_heading_label)
        
        self.polyfit_combo = QComboBox()
        # Keine Extra-Delegates nötig! Direkt Unicode verwenden:
        self.polyfit_combo.addItem("None", None)
        self.polyfit_combo.addItem("linear: y = kx + d", "poly_1")
        self.polyfit_combo.addItem("quadratic: y = ax² + bx + c", "poly_2")
        self.polyfit_combo.addItem("cubic", "poly_3")
        self.polyfit_combo.addItem("exponential: y = A · eᵇˣ", "exp")
        self.polyfit_combo.addItem("Andrade / Invers-Expo: y = A · eᵇᐟˣ", "andrade")
        self.polyfit_combo.addItem("saturation: y = A · (1 - e⁻ᵇˣ)", "saettigung")
        self.polyfit_combo.setCurrentIndex(0)
        trafo_tab_layout.addWidget(self.polyfit_combo)

        # Polyfit Label
        self.polyfit_input_label = QLineEdit()
        self.polyfit_input_label.setPlaceholderText("Label des Fits: z.B. linearer Fit (LaTeX Support)")
        self.polyfit_input_label.setEnabled(False)
        trafo_tab_layout.addWidget(self.polyfit_input_label)

    #Überschrift

        self.datentab_label = QLabel("Mathematische Operationen und Tools:")
        trafo_tab_layout.addWidget(self.datentab_label)
    # Button für den Größtfehler-Rechner anlegen
        self.btn_groesstfehler = QPushButton("Datenmanipulation | Fehlerrechnung")
        self.btn_groesstfehler.setStyleSheet("font-weight: bold;")
        
        # Den Button mit der eben getippten Methode verbinden
        self.btn_groesstfehler.clicked.connect(self.oeffne_groesstfehler_dialog)
        
        # Ins Layout deines Data-Tabs einfügen
        # (Ersetze 'data_layout' durch den Namen deines Layouts im Data-Tab)
        trafo_tab_layout.addWidget(self.btn_groesstfehler)

        self.btn_oeffne_mittelwert = QPushButton("Mittelwertrechner")
        self.btn_oeffne_mittelwert.setStyleSheet("font-weight: bold;")
        self.btn_oeffne_mittelwert.clicked.connect(self.oeffne_mittelwert_dialog)
        trafo_tab_layout.addWidget(self.btn_oeffne_mittelwert)

    #Checkbox für Semilogy Axis

        self.logaxis_label = QLabel("Achsenmanipulationen:")
        trafo_tab_layout.addWidget(self.logaxis_label)
        
        self.logaxis_combo = QComboBox()
        # Keine Extra-Delegates nötig! Direkt Unicode verwenden:
        self.logaxis_combo.addItem("default (linear)", "linear")
        self.logaxis_combo.addItem("semilogY", "semilogy")
        self.logaxis_combo.addItem("semilogX", "semilogx")
        self.logaxis_combo.addItem("loglog", "loglog")
        self.polyfit_combo.setCurrentIndex(0)
        trafo_tab_layout.addWidget(self.logaxis_combo)
        
    #Checkbox für "zeige Maxima" #showmaxima_checkbox

        self.maxmin_label = QLabel("Maxima / Minima:")
        trafo_tab_layout.addWidget(self.maxmin_label)

        self.showmaxmin_combo = QComboBox()
        self.showmaxmin_combo.addItem("Verstecke lokale Minima/Maxima", "dontshow")
        self.showmaxmin_combo.addItem("Zeige lokale Maxima", "locmax")
        self.showmaxmin_combo.addItem("Zeige lokale Minima", "locmin")
        self.showmaxmin_combo.setCurrentIndex(0)
        trafo_tab_layout.addWidget(self.showmaxmin_combo)

        self.save_maxmin = QPushButton("Speichere Maxima / Minima als Excel")
        self.save_maxmin.setEnabled(False)
        trafo_tab_layout.addWidget(self.save_maxmin)

          
        trafo_tab_layout.addStretch()
        tab_trafo_widget.setLayout(trafo_tab_layout)


         #--------------------------------------------------------------------------------
    #Style

        tab_style_widget = QWidget()
        style_tab_layout = QVBoxLayout()


        # Auswahlbox für Linestyle
        style_tab_layout.addWidget(QLabel("Linestyle:"))

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
        style_tab_layout.addWidget(QLabel("Markerstyle:"))
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

        #Spinbox für die Markergröße

        style_tab_layout.addWidget(QLabel("Markersize:"))
        self.markersize_spinbox = QDoubleSpinBox()
        self.markersize_spinbox.setValue(10)
        self.markersize_spinbox.setRange(1, 20) #
        style_tab_layout.addWidget(self.markersize_spinbox)



        self.grid_checkbox = QCheckBox("Grid: True/False")
        self.grid_checkbox.setChecked(True)
        style_tab_layout.addWidget(self.grid_checkbox)


        #Box für die Farbe(n)
        self.color_lbl = QLabel()
        style_tab_layout.addWidget(self.color_lbl)
        self.color_button = QPushButton("Farbe wählen")
        self.update_color_button_style()
        style_tab_layout.addWidget(self.color_button)

        tab_style_widget.setLayout(style_tab_layout)

        #Slider für die Legenden Position

        self.lbl_legendposition = QLabel()
        style_tab_layout.addWidget(self.lbl_legendposition)

        self.slider_legendposition = QSlider(Qt.Orientation.Horizontal)
        self.slider_legendposition.setRange(0,10)
        self.slider_legendposition.setSingleStep(1)
        self.slider_legendposition.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_legendposition.setTickInterval(1)
        self.slider_legendposition.setEnabled(False)
        style_tab_layout.addWidget(self.slider_legendposition)

        style_tab_layout.addStretch()


    #Import/Export / Daten

        #Excel öffnen Button

        tab_import_export_widget = QWidget()
        tab_import_export_layout = QVBoxLayout()

        #Tabelle zum Laden der Daten einfügen
        self.lbl_datentabelle = QLabel()
        tab_import_export_layout.addWidget(self.lbl_datentabelle)
        self.datentabelle = QTableWidget()
        tab_import_export_layout.addWidget(self.datentabelle)
        self.update_datentabelle()

        #Button zum Datei öffnen einfügen

        self.datei_button = QPushButton("Excel öffnen")
        tab_import_export_layout.addWidget(self.datei_button)

        tab_import_export_widget.setLayout(tab_import_export_layout)
        font_importbutton = self.datei_button.font()
        font_importbutton.setBold(True)
        self.datei_button.setFont(font_importbutton)


        #Export Einstellungen:
        self.lbl_dpi = QLabel()
        tab_import_export_layout.addWidget(self.lbl_dpi)

        self.slider_dpi = QSlider(Qt.Orientation.Horizontal)
        self.slider_dpi.setRange(0,4)
        self.slider_dpi.setSingleStep(1)
        self.slider_dpi.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_dpi.setTickInterval(1)
        self.slider_dpi.setValue(2)
        self.slider_dpi.setEnabled(True)
        tab_import_export_layout.addWidget(self.slider_dpi)

        layout_dpi_labels = QHBoxLayout()
        layout_dpi_labels.setContentsMargins(0, 0, 0, 0)
        for val in ["100", "150", "300", "600", "1200"]:
            lbl = QLabel(val)
            lbl.setStyleSheet("font-size: 9px; color: #666666;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_dpi_labels.addWidget(lbl)

        tab_import_export_layout.addLayout(layout_dpi_labels)


            #Button zum Zurücksetzen der Daten


        layout_reset_data = QHBoxLayout()
        #Y Zurücksetz Button
        self.btn_reset_xdata = QPushButton()
        layout_reset_data.addWidget(self.btn_reset_xdata)
        self.btn_reset_xdata.clicked.connect(self.reset_xdaten)
        #X Zurücksetz Button
        self.btn_reset_ydata = QPushButton()
        layout_reset_data.addWidget(self.btn_reset_ydata)
        self.btn_reset_ydata.clicked.connect(self.reset_ydaten)


        tab_import_export_layout.addLayout(layout_reset_data)

        self.btn_deletealldata = QPushButton()
        tab_import_export_layout.addWidget(self.btn_deletealldata)


        # Speicher-Button anlegen
        self.save_button = QPushButton("Plot speichern unter...")
        font = self.save_button.font()
        font.setBold(True)
        self.save_button.setFont(font)
        tab_import_export_layout.addWidget(self.save_button) 

        tab_import_export_layout.addStretch() 

#Menüleiste oben hinzufügen
        menubar = self.menuBar()
        
        #Programm Menu
        self.name_menu = menubar.addMenu("Protokollix")
        self.action_about = self.name_menu.addAction("About Protokollix")
        self.action_about.setMenuRole(QAction.MenuRole.NoRole)
        self.action_about.triggered.connect(self.zeige_about_dialog)

        #Sprachmenu
        self.bearbeiten_menu = menubar.addMenu("Bearbeiten")
        sprachen_menu = self.bearbeiten_menu.addMenu("Sprache/Language")
        akt_deutsch = sprachen_menu.addAction("Deutsch")
        akt_englisch = sprachen_menu.addAction("English")

        akt_deutsch.triggered.connect(lambda: self.sprache_wechseln("de"))
        akt_englisch.triggered.connect(lambda: self.sprache_wechseln("en"))

#Verknüpfen

        #Tabs zum QTABWIDGET hinzufügen und ins Hauptlayout schieben
        self.tabs.addTab(tab_label_widget, "Allgemeines")
        self.tabs.addTab(tab_trafo_widget, "Data")
        self.tabs.addTab(tab_style_widget, "Style")
        self.tabs.addTab(tab_import_export_widget, "Import/Export")

        #Das wichtigste:
        # Verknüpfen der Tabs mit dem Hauptlayout
        self.haupt_layout.addWidget(self.tabs, 1)
        self.retranslate_ui()

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
        self.legende_input.textChanged,
        self.linestyle_combo.currentTextChanged,
        self.markerstyle_combo.currentTextChanged,
        self.figsize_x_input.valueChanged, # Neu
        self.figsize_y_input.valueChanged, # Neu
        self.fontsize_slider.valueChanged,
        self.polyfit_combo.currentTextChanged,
        self.grid_checkbox.toggled,
        self.polyfit_input_label.textChanged,
        self.logaxis_combo.currentTextChanged,
        self.markersize_spinbox.valueChanged,
        self.showmaxmin_combo.currentTextChanged,
        self.slider_legendposition.valueChanged
        ):
            signal.connect(self.plot_aktualisieren)

        # Button verknüpfungen
        self.datei_button.clicked.connect(self.load_file)
        self.achsenlimit_button.clicked.connect(self.auto_limits)
        self.color_button.clicked.connect(self.choose_color)
        self.save_button.clicked.connect(self.save_plot)
        self.aktive_y_combo.currentTextChanged.connect(self.spalte_gewechselt)
        self.limitskommastellen_slider.valueChanged.connect(self.update_limitkommastellen)
        self.save_maxmin.clicked.connect(self.save_maxmin_excel)
        self.datentabelle.cellChanged.connect(self.tabelle_zelle_geaendert)
        self.btn_deletealldata.clicked.connect(self.reset_everything)

    def plot_aktualisieren(self):

        #Plotgröße updaten zu beginn
        w = self.figsize_x_input.value() # Bildgröße
        h = self.figsize_y_input.value()


        # 2. WICHTIG: Achse vollständig leeren vor dem Neuzeichnen!
        self.ax.clear()

        self.ax.set_box_aspect(h / w)
        self.speichere_stil_der_aktiven_spalte()



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
        current_markersize = self.markersize_spinbox.value()
        color = self.plot_color.name()
        fontsize = self.fontsize_slider.value()
        grid_aktiv = self.grid_checkbox.isChecked()  # Gibt True oder False zurück
        legend_pos = self.slider_legendposition.value()

        #Beschriftungen
        # Übersetzungspaket für leere Achsenbeschriftungen holen
        t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])
        default_title = t.get("initial_title", "noch keine Daten geladen")
        default_x = t.get("default_x_axis", "X-Achse:")
        default_y = t.get("default_y_axis", "Y-Achse:")

        # Beschriftungen setzen
        self.ax.set_title(titel_text if titel_text else default_title, fontsize=fontsize)
        self.ax.set_xlabel(x_text if x_text else default_x, fontsize=fontsize * 0.80)
        self.ax.set_ylabel(y_text if y_text else default_y, fontsize=fontsize * 0.80)

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
        # 1. ERST die Achsenskalierung setzen (Linear vs. Log)
        axistype = self.logaxis_combo.currentData()

        if axistype == "semilogy":
            self.ax.set_xscale("linear")
            self.ax.set_yscale("log")
            self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=grid_dichte))
            self.ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0))
        elif axistype == "semilogx":
            self.ax.set_xscale("log")
            self.ax.set_yscale("linear")
            self.ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0))
            self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=grid_dichte))
        elif axistype == "loglog":
            self.ax.set_xscale("log")
            self.ax.set_yscale("log")
            self.ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0))
            self.ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0))
        else:
            self.ax.set_xscale("linear")
            self.ax.set_yscale("linear")
            self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=grid_dichte))
            self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=grid_dichte))

        self.ax.grid(grid_aktiv, which="both" if "log" in str(axistype) else "major")

        # 2. DANACH die Achsenlimits anwenden (mit Absturz-Schutz für Logarithmen!)
        if x_max > x_min:
            if "logx" in str(axistype) or axistype == "loglog":
                if x_min > 0:
                    self.ax.set_xlim(x_min, x_max)
            else:
                self.ax.set_xlim(x_min, x_max)

        if y_max > y_min:
            if "semilogy" in str(axistype) or axistype == "loglog":
                # Verhindert den Absturz bei log: y_min MUSS strikt > 0 sein!
                if y_min > 0:
                    self.ax.set_ylim(y_min, y_max)
                else:
                    # Automatisches Fallback für Log-Skala, falls in der Spinbox 0 steht
                    if self.y_dict:
                        aktive_spalte = self.aktive_y_combo.currentText()
                        vals = self.y_dict.get(aktive_spalte, [])
                        pos_vals = [v for v in vals if v > 0]
                        if pos_vals:
                            self.ax.set_ylim(min(pos_vals) * 0.8, max(vals) * 1.2)
            else:
                self.ax.set_ylim(y_min, y_max)

        # Daten plotten

        if self.x_data is not None and self.y_dict:
            x_geplottet = self.x_data.copy()
            self.current_x = x_geplottet


            # Schleife über ALLE geladenen Y-Spalten (z.B. Warmwasser, Kaltwasser)
            for spalten_name, y_raw in self.y_dict.items():
                y_geplottet = y_raw.copy()
                
                # Stile für DIESE Spalte holen (falls vorhanden, sonst Fallback)
                stil = self.y_styles.get(spalten_name, {
                    "color": self.plot_color.name(),
                    "linestyle": current_linestyle,
                    "markerstyle": current_markerstyle,
                    "markersize": current_markersize
                })

                # Wenn die aktuell gezeichnete Spalte die in der ComboBox gewählte ist AND ein Label getippt wurde -> nimm das Label!
                kurven_label = stil.get("label", spalten_name)

                # Plotten mit DEN INDIVIDUELLEN STILEN dieser Kurve!

                spalten_y_err = stil.get("y_err", None) # Daten holen

                if spalten_y_err is not None and np.any(spalten_y_err != 0) or self.x_err is not None and np.any( self.x_err != 0):
                    self.ax.errorbar(
                        x_geplottet, y_geplottet, yerr=spalten_y_err, xerr=self.x_err,
                        marker=stil["markerstyle"], markersize= stil["markersize"], color=stil["color"],
                        linestyle=stil["linestyle"], capsize=3, label=kurven_label
                    )
                else:
                    self.ax.plot(
                        x_geplottet, y_geplottet,
                        marker=stil["markerstyle"], markersize= stil["markersize"], color=stil["color"],
                        linestyle=stil["linestyle"], label=kurven_label
                        )



            # Fit-Block vorübergehend absichern (nimmt vorerst die letzte Spalte für den Fit)
            aktive_spalte = self.aktive_y_combo.currentText()
            if aktive_spalte in self.y_dict:
                y_daten = self.y_dict[aktive_spalte]

            fit_typ = self.polyfit_combo.currentData()
            polyfit_label = self.polyfit_input_label.text()

            if fit_typ is not None and 'y_geplottet' in locals():
                try:
                    self.polyfit_input_label.setEnabled(True)
                    # Ausreichend Punkte für eine glatte Kurve generieren
                    x_fit_smooth = np.linspace(min(x_geplottet), max(x_geplottet), 200)

                    #Polynom Fits-------------------------------------
                    if str(fit_typ).startswith("poly_"):
                        grad = int(fit_typ.split("_")[1])
                        popt, pcov = np.polyfit(x_geplottet, y_daten, grad, cov = True)
                        y_fit_smooth = np.polyval(popt, x_fit_smooth)

                        formel_text = self.erstelle_fit_formel(popt, pcov)
                        self.polyfit_heading_label.setText(f"<b>Fit</b>: {formel_text}")
                    # Nicht lineare Fits (SciPy Curve Fits)

                    else:
                        from scipy.optimize import curve_fit
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
                        popt, pcov = curve_fit(func, x_geplottet, y_daten, p0 = p0, maxfev= 5000)
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
                self.polyfit_heading_label.setText("Ausgleichskurve / Fit:")
                self.polyfit_input_label.setEnabled(False)
                self.polyfit_input_label.blockSignals(True)
                self.polyfit_input_label.clear()
                self.polyfit_input_label.blockSignals(False)
                
            # Nur eine Legende zeichnen, wenn Daten geladen sind und mindestens ein Label existiert
            handles, labels = self.ax.get_legend_handles_labels()
            if handles:
                self.ax.legend(fontsize=fontsize * 0.75, loc = legend_pos)
                #Legenden Position freischalten
                self.slider_legendposition.setEnabled(True)
            else: 
                self.slider_legendposition.setEnabled(False)

            self.lbl_legendposition.setText(self.update_legend_position())


        # Maxima / Minima holen & Box sperren/freischalten
        maxmin_xval, maxmin_yval = self.calculate_locmaxmin()
        self.showmaxmin_combo.setEnabled(maxmin_xval.size > 0)
        self.save_maxmin.setEnabled(maxmin_xval.size > 0)

        # Nur zeichnen, wenn nicht ausgeblendet
        if self.showmaxmin_combo.currentData() in ("locmax", "locmin"):
            self.ax.plot(maxmin_xval, maxmin_yval, c="red", markersize=10, marker="+", linestyle="")




        self.canvas.draw_idle()

    def choose_color(self):
        color = QColorDialog.getColor(self.plot_color, self, "Farbe für Plot auswählen")

        if color.isValid():
            self.plot_color = color
            self.update_color_button_style()
            self.plot_aktualisieren()  # Reicht völlig aus, speichert jetzt automatisch!

    def update_color_button_style(self):
        # Baut einen CSS-String, um den Button einzufärben und die Schrift lesbar zu halten
        hex_code = self.plot_color.name()
        self.color_button.setStyleSheet(
            f"background-color: {hex_code}; color: white; font-weight: bold; border-radius: 4px; padding: 6px;"
        )

    def auto_limits(self):
        # Holt die Daten der AKTUELL gewählten Y-Spalte aus der ComboBox
        aktive_spalte = self.aktive_y_combo.currentText()
        
        x_vals = self.current_x if self.current_x is not None else self.x_data
        
        if aktive_spalte in self.y_dict and x_vals is not None:
            y_vals = self.y_dict[aktive_spalte]

            randx = np.ptp(x_vals) * 0.1
            randy = np.ptp(y_vals) * 0.1

            if randx == 0: randx = 1.0
            if randy == 0: randy = 1.0

            self.x_min_input.setValue(float(min(x_vals) - randx))
            self.x_max_input.setValue(float(max(x_vals) + randx))
            self.y_min_input.setValue(float(min(y_vals) - randy))
            self.y_max_input.setValue(float(max(y_vals) + randy))

    def load_file(self):

        msgBox = QMessageBox(self)
        
        
        # 1. Info-Box mit Beispiel-Tabelle anzeigen
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Hinweis zum Excel-Format")
        msgBox.setText("<b>Optimale Struktur für den Datei-Import</b>" if self.aktuelle_sprache == "de" else "<b>Optimized layout for data import</b>")
        
        # HTML-Tabelle mit Anschauungsbeispiel bauen
        html_text_deutsch = (
            "Damit die Daten fehlerfrei eingelesen werden, beachte bitte folgendes (beispielhaftes) Format:<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            "  <tr style='background-color: #e0e0e0; font-weight: bold;'>"
            "    <td>Zeit t / s</td><td>T1 / °C</td><td>T2 / °C</td><td>P / W</td>"
            "  </tr>"
            "  <tr><td>0.0</td><td>10.2</td><td>20.5</td><td>5.1</td></tr>"
            "  <tr><td>1.0</td><td>12.4</td><td>22.1</td><td>5.8</td></tr>"
            "  <tr><td>2.0</td><td>76.0</td><td>24.8</td><td>6.4</td></tr>"
            "</table><br>"
            "<b>Wichtige Regeln:</b>"
            "<ul style='margin-top: 4px; padding-left: 20px;'>"
            "  <li>Erste Spalte = <b>X-Daten</b>, alle weiteren Spalten = <b>Y-Daten</b>.</li>"
            "  <li> Somit ist es möglich, <b> mehrere Y-Datenreihen </b> gleichzeitig zu laden und zu bearbeiten.</li>"
            "  <li>Optional eine Kopfzeile mit Text (Einheiten/Namen), diese werden automatisch erkannt.</li>"
            "  <li>Keine leeren Zellen mitten in den Datenreihen.</li>"
            "  <li>Abgesehen von den Spalten und ihren Namen muss die Datei leer sein</li>"
            "</ul>"
        )

        html_text_english = (
            "To ensure your data is read without errors, please follow this (exemplary) format:<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            "  <tr style='background-color: #e0e0e0; font-weight: bold;'>"
            "    <td>Time t / s</td><td>T1 / °C</td><td>T2 / °C</td><td>P / W</td>"
            "  </tr>"
            "  <tr><td>0.0</td><td>10.2</td><td>20.5</td><td>5.1</td></tr>"
            "  <tr><td>1.0</td><td>12.4</td><td>22.1</td><td>5.8</td></tr>"
            "  <tr><td>2.0</td><td>76.0</td><td>24.8</td><td>6.4</td></tr>"
            "</table><br>"
            "<b>Important Rules:</b>"
            "<ul style='margin-top: 4px; padding-left: 20px;'>"
            "  <li>First column = <b>X data</b>, all subsequent columns = <b>Y data</b>.</li>"
            "  <li>This allows <b>multiple Y datasets</b> to be loaded and processed simultaneously.</li>"
            "  <li>Optional header row with text (units/names); these will be recognized automatically.</li>"
            "  <li>No empty cells within the data series.</li>"
            "  <li>Apart from the columns and their headers, the sheet must be empty.</li>"
            "</ul>"
        )
        
        msgBox.setInformativeText(html_text_deutsch if self.aktuelle_sprache == "de" else html_text_english )
        msgBox.exec()

        dateiname, _ = QFileDialog.getOpenFileName(
        self, 
        "Messdaten auswählen" if self.aktuelle_sprache == "de" else "Select Data File", "",  "Messdaten (*.xlsx *.xls *.csv);;Excel-Dateien (*.xlsx *.xls);;CSV-Dateien (*.csv)")
        if dateiname: # if dateiname is not none
            print(dateiname)

            try: 

                #Mauszeiger auf "Beschäftigt" stellen
                QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                if dateiname.lower().endswith(".csv"):
                    # sep=None zusammen mit engine='python' erkennt automatisch Komma, Semikolon oder Tabulator!
                    # decimal=',' sorgt dafür, dass auch deutsche Kommazahlen (12,4) sauber als Float gelesen werden
                    raw_df = pd.read_csv(dateiname, header=None, sep=None, engine="python", decimal=",")
                else:
                    raw_df = pd.read_excel(dateiname, header=None)

                raw_df = raw_df.dropna(how = "all").reset_index(drop = True)
                raw_df = raw_df.dropna(how='all', axis=1)

                if raw_df.empty:
                    QMessageBox.warning(self, "Datei leer", "diese Datei enthält keine Daten!")
                    return 
                if raw_df.shape[1] < 2:
                    msg = (
                        "Die Datei muss mindestens 2 Spalten enthalten:\n\n"
                        "• Spalte 1: X-Daten\n"
                        "• Spalte 2 (und weitere): Y-Daten"
                        if self.aktuelle_sprache == "de"
                        else
                        "The file must contain at least 2 columns:\n\n"
                        "• Column 1: X data\n"
                        "• Column 2 (and subsequent): Y data"
                    )
                    QMessageBox.warning(
                        self,
                        "Zu wenige Spalten" if self.aktuelle_sprache == "de" else "Not Enough Columns",
                        msg
                    )
                    return
                
                #Erste Zeile reine Zahlen?
                erste_zeile = raw_df.iloc[0]
                numerisch = True
                for val in erste_zeile:
                    try: 
                        float(val)
                    except (ValueError, TypeError):
                        numerisch = False
                        break
                #Spaltenname und Daten trennen
                if numerisch: #
                    x_label_text = ""
                    y_spalten_namen = [f"Datensatz {i+1}" for i in range(raw_df.shape[1] - 1)]
                    datafile = raw_df.copy()
                else: #erste Zeile ist ein Text
                    x_label_text = str(raw_df.iloc[0,0])
                    y_spalten_namen = [str(val) for val in raw_df.iloc[0, 1:]]
                    datafile = raw_df.iloc[1:].reset_index(drop=True)
                # Prüfen, ob nach dem Header irgendwo leere Felder (NaN) in den Daten sind
                if datafile.isnull().values.any():
                    QMessageBox.warning(
                        self, 
                        "Fehlende Datenwerte", 
                        "In deiner Excel-Datei fehlen einzelne Zahlenwerte (leere Zellen).\n\n"
                        "Bitte überprüfe deine Datei und stelle sicher, dass alle Messreihen vollständig ausgefüllt sind."
                    )
                    return

                self.x_data = datafile.iloc[:, 0].to_numpy(dtype = float)
                
                # Alle restlichen Spalten werden als Y Spalten gespeichert
                # Standard-Farbpalette von Matplotlib für unterschiedliche Farben
                default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

                self.y_dict = {}
                self.y_styles = {}
                self.aktive_y_combo.blockSignals(True)
                self.aktive_y_combo.clear()
                k = 0

                for idx, spalten_name in enumerate(y_spalten_namen):
                    spalten_name = str(spalten_name)
                    self.y_dict[spalten_name] = datafile.iloc[:, idx + 1].to_numpy(dtype=float)
                    # Stile für diese spezifische Spalte anlegen
                    farbe = default_colors[idx % len(default_colors)]
                    self.y_styles[spalten_name] = {
                        "color": farbe,
                        "linestyle": "",
                        "markerstyle": ".",
                        "label": spalten_name,
                        "y_err": None, # Neu: Fehler pro Y Spalte
                        "markersize": 10
                    }
                    self.aktive_y_combo.addItem(spalten_name)

                #Datenkopie erstellen, die unberührt ist fürs Zurücksetzen:

                self.x_data_raw = self.x_data.copy()
                self.y_dict_raw = {k: v.copy() for k, v in self.y_dict.items()}

                self.aktive_y_combo.blockSignals(False)
                if x_label_text:
                    self.x_label_input.blockSignals(True)
                    self.x_label_input.setText(x_label_text)
                    self.x_label_input.blockSignals(False)
                #Wenn das gut geht, Plot aktualisieren:

                #Einmalig beim Laden die Limits anpassen
                # Limits berechnen
                randx = np.ptp(self.x_data) * 0.1
                erste_y_werte = list(self.y_dict.values())[0] if self.y_dict else [1.0]
                randy = np.ptp(erste_y_werte) * 0.1
                
                if randx == 0: randx = 1.0
                if randy == 0: randy = 1.0

                # Signale kurz blockieren, damit nicht 4x hintereinander plot_aktualisieren aufgerufen wird
                self.x_min_input.blockSignals(True)
                self.x_max_input.blockSignals(True)
                self.y_min_input.blockSignals(True)
                self.y_max_input.blockSignals(True)

                self.x_min_input.setValue(float(min(self.x_data) - randx))
                self.x_max_input.setValue(float(max(self.x_data) + randx))
                self.y_min_input.setValue(float(min(erste_y_werte) - randy))
                self.y_max_input.setValue(float(max(erste_y_werte) + randy))

                # Signale wieder aktivieren
                self.x_min_input.blockSignals(False)
                self.x_max_input.blockSignals(False)
                self.y_min_input.blockSignals(False)
                self.y_max_input.blockSignals(False)

                # NEU: Das Legenden-Textfeld mit dem Namen der 1. Spalte befüllen!
                if self.aktive_y_combo.count() > 0:
                    erste_spalte = self.aktive_y_combo.itemText(0)
                    self.legende_input.blockSignals(True)
                    self.legende_input.setText(erste_spalte)
                    self.legende_input.blockSignals(False)
                # Jetzt EINMAL sauber den Plot neu zeichnen und die Datentabelle updaten
                self.update_datentabelle()
                self.plot_aktualisieren()
                


            except ValueError:
                # Dieser Block wird nur ausgeführt, wenn der Text nicht zu Zahlen (float) umgewandelt werden konnte
                QMessageBox.critical(self,  "Datenfehler",  "Die Excel-Datei enthält ungültige Zeichen (z. B. Text).\nBitte stelle sicher, dass in den ersten beiden Spalten nur Zahlen stehen!"
                )
                # Speicher wieder leeren, damit kein halber Müll geplottet wird
                self.x_data = None
                self.y_data = {}
                
            except Exception as e:
                # Fängt alle anderen Fehler ab (z. B. Excel-Datei hat nur 1 Spalte oder ist kaputt)
                QMessageBox.critical(
                    self,   "Allgemeiner Fehler",   f"Details zum Fehler:\n{type(e).__name__}: {str(e)}"
                )

            finally:
                QApplication.restoreOverrideCursor()

    def save_plot(self):
            # Öffnet den System-Speicherdialog mit Dateityp-Filtern
            current_dpi = self.get_current_dpi()
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
                    self.figure.savefig(dateiname, dpi=current_dpi, bbox_inches='tight')

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

    @staticmethod
    def erstelle_hilfe_button(hilfe_text):
            btn = QPushButton("?")
            btn.setFixedSize(18, 18)  # Kompakt und unaufdringlich
            btn.setToolTip(hilfe_text)
            btn.setCursor(Qt.CursorShape.WhatsThisCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1686ff;
                    color: #FFFFFF;
                    border-radius: 9px;
                    font-weight: bold;
                    font-size: 11px;
                    border: none;
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

    def berechne_groesstfehler(self, formel_text, werte_dict, unsicherheiten_dict, digit_unsicherheiten_dict, raw_texte_dict = None):
        formel_sauber = formel_text.replace("^", "**") #Latex hochschreibweise integrierens

        #Neu: Ableitungen berechnen

        if "diff(" in formel_sauber and self.x_data is not None and "y" in werte_dict:
            y_arr = werte_dict["y"]
            x_arr = werte_dict["x"] if "x" in werte_dict else self.x_data

            dy_dx = np.gradient(y_arr, x_arr)
            formel_sauber = re.sub(r"diff\s*\(\s*y\s*(,\s*x\s*)?\)", "_dydx", formel_sauber)
            werte_dict["_dydx"] = dy_dx
            unsicherheiten_dict["_dydx"] = 0.0  # Ableitung selbst hat vorerst 0 Fehler



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
            val_var = werte_dict[var_name]

            #Digit schrittweise ermitteln
            digits_count = digit_unsicherheiten_dict.get(var_name, 0.0) #Standard-Rückfallwert 0.0
            # Digit-Schrittweite ermitteln
            if digits_count != 0.0:
                s_eingabe = raw_texte_dict.get(var_name, "").strip().replace(",", ".")
# Wenn der Nutzer z. B. "40.0" oder "1.25" getippt hat:
                if s_eingabe and s_eingabe.lower() not in ["x", "y"]:
                    if "." in s_eingabe:
                      stellen = len(s_eingabe.split(".")[1])
                      digit_step = 10.0 ** (-stellen)
                    else:
                      digit_step = 1.0
                else:
                  # Für x/y: Schrittweite aus der eingegebenen Unsicherheit Δx bzw. Δy ableiten
                    s_u = f"{u_var:.8f}".rstrip("0")
                    if "." in s_u and len(s_u.split(".")[1]) > 0:
                        stellen = len(s_u.split(".")[1])
                        digit_step = 10.0 ** (-stellen)
                    else:
                        digit_step = 0.01

                digit_err = digit_step * digits_count
            else:
               digit_err = 0.0

            #Digits Unsicherheit dazurechnen zum Fehler
            u_gesamt = u_var + digit_err

            #Aufsummieren
            gesamt_fehler+= abl_wert * u_gesamt

        # FIX: Wenn der Funktionswert ein Array ist (z.B. x_data), aber der Fehler eine Zahl (z.B. 0.2),
        # bringe den Fehler auf dieselbe Array-Form!
        if isinstance(funktions_wert, np.ndarray) and isinstance(gesamt_fehler, (int, float, np.number)):
            gesamt_fehler = np.full_like(funktions_wert, gesamt_fehler)

        elif isinstance(funktions_wert, (int, float, np.number)):
            if self.x_data is not None:
                funktions_wert = np.full_like(self.x_data, funktions_wert)
                gesamt_fehler = np.full_like(self.x_data, gesamt_fehler)

        return funktions_wert, gesamt_fehler

    def oeffne_mittelwert_dialog(self):
        dialog = MittelwertDialog(parent = self, sprache = self.aktuelle_sprache)
        dialog.exec()

    def oeffne_groesstfehler_dialog(self):
            # 1. Dialog erstellen und unsere Rechenmethode direkt als Argument mitgeben
            aktive_spalte = self.aktive_y_combo.currentText() # aktive Spalte abfragen
            aktive_y_daten = self.y_dict.get(aktive_spalte, None)
            
            dialog = GroesstfehlerDialog(
                parent=self, 
                x_data=self.x_data, 
                y_data= aktive_y_daten, 
                rechen_funktion=self.berechne_groesstfehler,
                sprache=self.aktuelle_sprache
            )

            # 2. Öffnen und auf den Klick auf OK warten
            if dialog.exec() == QDialog.DialogCode.Accepted:
                formel, werte, unsicherheiten, digit_unsicherheiten, raw_texte = dialog.get_daten()
                if not formel:
                    return

                # Größtfehler berechnen
                f_neu, f_err = self.berechne_groesstfehler(formel, werte, unsicherheiten, digit_unsicherheiten, raw_texte)

                # Prüfen, welcher Radio-Button im Dialog gewählt wurde
                if dialog.radio_y.isChecked():
                    if aktive_spalte in self.y_dict:
                        self.y_dict[aktive_spalte] = f_neu
                    if aktive_spalte in self.y_styles:
                        self.y_styles[aktive_spalte]["y_err"] = f_err
                    self.plot_aktualisieren()

                elif dialog.radio_x.isChecked():
                    self.x_data = f_neu
                    self.x_err = f_err
                    self.plot_aktualisieren()

                elif dialog.radio_nur_ausgabe.isChecked():
                    # Daten im Plot bleiben unverändert, die Berechnung war nur für die Tabelle gedacht
                    print("Berechnung erfolgreich durchgeführt (ohne Plot-Änderung).")
                self.update_datentabelle()

            else:
                print("Größtfehler-Berechnung abgebrochen.")

    def speichere_stil_der_aktiven_spalte(self):
        aktive_spalte = self.aktive_y_combo.currentText()
        if aktive_spalte in self.y_styles:
            self.y_styles[aktive_spalte]["color"] = self.plot_color.name()
            self.y_styles[aktive_spalte]["linestyle"] = self.linestyle_combo.currentData()
            self.y_styles[aktive_spalte]["markerstyle"] = self.markerstyle_combo.currentData()
            self.y_styles[aktive_spalte]["label"] = self.legende_input.text()
            self.y_styles[aktive_spalte]["markersize"] = self.markersize_spinbox.value()

    def lade_stil_in_gui(self):
        aktive_spalte = self.aktive_y_combo.currentText()
        if aktive_spalte in self.y_styles:
            stil = self.y_styles[aktive_spalte]
            
            # Signale blockieren, damit das Ändern der Felder nicht vorzeitig abspeichert!
            self.linestyle_combo.blockSignals(True)
            self.markerstyle_combo.blockSignals(True)
            self.legende_input.blockSignals(True)
            self.markersize_spinbox.blockSignals(True)

            # 1. Farbe
            self.plot_color = QColor(stil["color"])
            self.update_color_button_style()

            # 2. Textfelder
            self.legende_input.setText(stil.get("label", ""))

            # 3. ComboBoxen
            idx_line = self.linestyle_combo.findData(stil.get("linestyle", "-"))
            if idx_line != -1: self.linestyle_combo.setCurrentIndex(idx_line)

            idx_marker = self.markerstyle_combo.findData(stil.get("markerstyle", "o"))
            if idx_marker != -1: self.markerstyle_combo.setCurrentIndex(idx_marker)

            # 4. Markersize in SpinBox laden
            self.markersize_spinbox.setValue(float(stil.get("markersize", 10)))

            # Signale wieder freigeben
            self.linestyle_combo.blockSignals(False)
            self.markerstyle_combo.blockSignals(False)
            self.legende_input.blockSignals(False)
            self.markersize_spinbox.blockSignals(False)

    def spalte_gewechselt(self):
        # Erst Einstellungen der alten Spalte sichern, dann die der neuen laden
        self.lade_stil_in_gui()

        self.plot_aktualisieren()

    def reset_xdaten(self):
        if self.x_data_raw is not None:
            self.x_data = self.x_data_raw.copy()
            self.x_err = None
            self.plot_aktualisieren()
            self.update_datentabelle()
            QMessageBox.information(self, "Reset", "Alle X-Daten wurden auf den ursprünglichen Zustand der Excel-Datei zurückgesetzt." if self.aktuelle_sprache == "de" else "All X-Data had been reset")

    def reset_ydaten(self):
        aktive_spalte = self.aktive_y_combo.currentText()
        if self.y_dict_raw and aktive_spalte in self.y_dict_raw:
            # Nur die aktive Spalte aus dem Backup wiederherstellen
            self.y_dict[aktive_spalte] = self.y_dict_raw[aktive_spalte].copy()
            
            # Nur den Fehlerbalken der aktiven Spalte entfernen
            if aktive_spalte in self.y_styles:
                self.y_styles[aktive_spalte]["y_err"] = None
                
            self.plot_aktualisieren()
            self.update_datentabelle()
            
            msg = (
                f"Die Daten für '{aktive_spalte}' wurden zurückgesetzt." 
                if self.aktuelle_sprache == "de" 
                else f"Data for '{aktive_spalte}' has been reset."
            )
            QMessageBox.information(self, "Reset", msg)

    def retranslate_ui(self):
        # 1. Übersetzungspaket holen
        t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])

        # 2. Fenstertitel
        self.setWindowTitle(t["title"])

        # 3. Tab-Titel anpassen
        self.tabs.setTabText(0, t["tab_general"])
        self.tabs.setTabText(1, t["tab_math"])
        self.tabs.setTabText(2, t["tab_style"])
        self.tabs.setTabText(3, t["tab_import"])

        #Überschriften anpassen in den Tabs
        self.label_Seitenverhältnis.setText(t["lbl_seitenverhältnis"])
        self.plot_title_label.setText(t["lbl_title_input"])
        self.x_achsen_label.setText(t["lbl_x_axis"])
        self.y_achsen_label.setText(t["lbl_y_axis"])
        self.x_limit_label.setText(t["lbl_x_axis_limits"])
        self.y_limit_label.setText(t["lbl_y_axis_limits"])
        self.datenlabel_label.setText(t["data_label"])
        self.schriftgroesse_label.setText(t["lbl_fontsize"])
        self.polyfit_heading_label.setText(t["lbl_fit"])
        self.datentab_label.setText(t["lbl_mathematicaloperation"])
        self.logaxis_label.setText(t["lbl_achsenmanipulation"])

        #Comboboxen

        if self.x_data is None:
            self.aktive_y_combo.setItemText(0, t["y_data_combo"])


        # 4. Buttons anpassen
        self.datei_button.setText(t["btn_excel"])
        self.save_button.setText(t["btn_save"])
        self.btn_groesstfehler.setText(t["btn_groesstfehler"])
        self.btn_oeffne_mittelwert.setText(t["btn_mittelwert"])
        self.achsenlimit_button.setText(t["btn_autolimits"])
        self.color_button.setText(t["choose_color"])
        self.btn_reset_xdata.setText(t["btn_xreset"])
        self.btn_reset_ydata.setText(t["btn_yreset"])
        self.menu_hilfebutton.setToolTip(self.get_hilfetext())
        self.btn_deletealldata.setText(t["btn_deletealldata"])

        # 5. Labels & Placeholdernamen anpassen
        self.label_aktiverDatensatz.setText(f"<b>{t['lbl_active_ds']}</b>")
        self.titel_input.setPlaceholderText("z.B. Pendelversuch" if self.aktuelle_sprache == "de" else "e.g. Pendulum Experiment")
        self.x_label_input.setPlaceholderText("z.B. Zeit t / s" if self.aktuelle_sprache == "de" else "e.g. time t / s")
        self.y_label_input.setPlaceholderText("z.B. Auslenkung x / m" if self.aktuelle_sprache == "de" else "e.g. Displacement x / m")
        self.legende_input.setPlaceholderText("z.B. Messreihe 1" if self.aktuelle_sprache == "de" else "e.g. pendulum data")
        self.color_lbl.setText(t["lbl_color"])
        self.polyfit_input_label.setPlaceholderText("Label des Fits: z.B. linearer Fit (LaTeX Support)" if self.aktuelle_sprache == "de" else "Fit Label: e.g. linear fit (LaTeX Support)")
        self.showmaxmin_combo.setItemText(0, "Verstecke lokale Minima/Maxima" if self.aktuelle_sprache == "de" else "Hide local Max/Min")
        self.showmaxmin_combo.setItemText(1, "Zeige lokale Maxima" if self.aktuelle_sprache == "de" else "Show Local Maxima")
        self.showmaxmin_combo.setItemText(2, "Zeige lokale Minima" if self.aktuelle_sprache == "de" else "Show Local Minima")
        self.lbl_limitskommastellen.setText(t["lbl_limitkommastellen"])
        self.lbl_legendposition.setText(t["lbl_legendposition"])
        self.lbl_dpi.setText(t["lbl_dpi"])
        self.lbl_datentabelle.setText(t["lbl_datentabelle"])
        
        


        #Menubar
        if hasattr(self, "name_menu"):
            self.name_menu.setTitle(t["menubar_app"])
        if hasattr(self, "bearbeiten_menu"):
            self.bearbeiten_menu.setTitle(t["menubar_edit"])
        if hasattr(self, "action_about"):
            self.action_about.setText(t["menu_about"])

        # Plot anpassen

        if hasattr(self, "ax"):
            self.plot_aktualisieren()

    def sprache_wechseln(self, sprache_code):
        self.aktuelle_sprache = sprache_code
        # Das Daten-Kürzel ("de" oder "en") aus der ComboBox auslesen
        print(f"Sprache gewechselt zu: {sprache_code}")
        # Sämtliche Texte auf dem Schirm aktualisieren!
        self.retranslate_ui()
    
    def zeige_about_dialog(self):
        try: 
            t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])
            QMessageBox.about(self, t["menubar_app"], t["about_text"])
            print("About Dialog erfolgreich angezeigt")
        except Exception as e:
            print(f"About Tab wurde unerwartet abgebrochen: {e}")

    def calculate_locmaxmin(self):
        # 1. Sicherung gegen None-Absturz beim Start
        if self.x_data is None or not self.y_dict:
            return np.array([]), np.array([])
        from scipy.signal import find_peaks

        aktive_spalte = self.aktive_y_combo.currentText()

        if aktive_spalte in self.y_dict:
            x_daten = self.x_data
            y_daten = self.y_dict[aktive_spalte]  # Daten holen
            
            # Wenn Minima gewählt sind -> Minima berechnen
            if self.showmaxmin_combo.currentData() == "locmin":
                if len(x_daten) == len(y_daten):
                    y_daten_reverse = -y_daten
                    peaks_idx, _ = find_peaks(y_daten_reverse)
                    x_val_peaks = x_daten[peaks_idx]
                    y_val_peaks = y_daten[peaks_idx] 
                    return (x_val_peaks, y_val_peaks)
            
            # Ansonsten (bei "locmax" oder zur Peak-Prüfung bei "dontshow") -> Maxima berechnen
            else:
                if len(x_daten) == len(y_daten):
                    peaks_idx, _ = find_peaks(y_daten)
                    x_val_peaks = x_daten[peaks_idx]
                    y_val_peaks = y_daten[peaks_idx]
                    return (x_val_peaks, y_val_peaks)

        return np.array([]), np.array([])
                        
    def update_limitkommastellen(self):
        decimals = self.limitskommastellen_slider.value()
        self.y_max_input.setDecimals(decimals)
        self.y_min_input.setDecimals(decimals)
        self.x_max_input.setDecimals(decimals)
        self.x_min_input.setDecimals(decimals)

    def save_maxmin_excel(self):
        if self.x_data is None or not self.y_dict:
            return

        aktive_spalte = self.aktive_y_combo.currentText()
        if aktive_spalte not in self.y_dict:
            return
        from scipy.signal import find_peaks

        x_daten = self.x_data
        y_daten = self.y_dict[aktive_spalte]

        # 1. Maxima & Minima getrennt berechnen
        max_idx, _ = find_peaks(y_daten)
        min_idx, _ = find_peaks(-y_daten)

        # 2. DataFrame mit pd.Series aufbauen (gleicht unterschiedliche Längen automatisch mit NaN aus)
        daten = {
            "Minima (x)": pd.Series(x_daten[min_idx]),
            "Minima (y)": pd.Series(y_daten[min_idx]),
            "Maxima (x)": pd.Series(x_daten[max_idx]),
            "Maxima (y)": pd.Series(y_daten[max_idx])
        }
        df = pd.DataFrame(daten)

        # 3. Datei-Speicherdialog öffnen
        dateiname, _ = QFileDialog.getSaveFileName(
            self,
            "Maxima & Minima speichern",
            f"extrema_{aktive_spalte}.xlsx",
            "Excel-Arbeitsmappe (*.xlsx);;CSV-Datei (*.csv)"
        )

        if dateiname:
            try:
                if dateiname.endswith(".csv"):
                    df.to_csv(dateiname, index=False, sep=";", float_format="%.4f")
                else:
                    df.to_excel(dateiname, index=False, float_format="%.4f")

                QMessageBox.information(
                    self, 
                    "Erfolg", 
                    f"Die Extrema wurden erfolgreich gespeichert unter:\n{dateiname}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Fehler beim Speichern", 
                    f"Die Datei konnte nicht gespeichert werden:\n\n{str(e)}"
                )

    def get_hilfetext(self):
        if self.aktuelle_sprache == "de":
            return (
            "<b>Zentraler Datensatz-Selektor</b><br>"
            "Mit diesem Dropdown-Menü wählst du aus, welcher Y-Datensatz "
            "aktuell bearbeitet werden soll.<br><br>"
            "Alle Einstellungen in den folgenden Tabs beziehen sich "
            "<b>spezifisch auf die hier gewählte Datenreihe:</b>"
            "<ul style='margin-top: 6px; margin-bottom: 6px; padding-left: 18px;'>"
                "<li><b>Allgemeines:</b> Individuelles Datenlabel für die Legende</li>"
                "<li><b>Data:</b> Y-Transformationen & Größtfehler-Berechnung</li>"
                "<li><b>Style:</b> Farbe, Linienstil und Marker-Typ</li>"
            "</ul>"
            "<i>Tipp: Bei einem Wechsel im Dropdown werden alle Einstellungen der einzelnen Spalten automatisch gespeichert.</i>")
        else:
            return (
                "<b>Central Dataset Selector</b><br>"
                "Use this dropdown menu to select which Y dataset "
                "is currently being edited.<br><br>"
                "All settings in the following tabs apply "
                "<b>specifically to the selected dataset:</b>"
                "<ul style='margin-top: 6px; margin-bottom: 6px; padding-left: 18px;'>"
                    "<li><b>General:</b> Custom data label for the legend</li>"
                    "<li><b>Data:</b> Y transformations & maximum error calculation</li>"
                    "<li><b>Style:</b> Color, line style, and marker type</li>"
                "</ul>"
                "<i>Tip: When switching datasets in the dropdown, all individual settings are saved automatically.</i>")

    def update_legend_position(self):
        current_position = self.slider_legendposition.value()
        #Derzeitige Sprache holen
        t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])
        first_part = t["lbl_legendposition"]
        list_positions = ["best", "upper right", "upper left", 
                          "lower left", "lower right", "right", 
                          "center left", "center right", 
                          "lower center", "upper center", "center"]
        current_string = list_positions[current_position]
        return(first_part + " " + current_string)
        
    def get_current_dpi(self):
        values = (100, 150, 300, 600, 1200)
        return values[self.slider_dpi.value()]

    def update_datentabelle(self):
        print("Test")
        if self.x_data is not None and self.y_dict:
            try: 
                #Daten holen
                x_daten = self.x_data
                first_ycolumn = list(self.y_dict.values())[0]
                n_rows = len(first_ycolumn)
                n_columns = len(self.y_dict) + 1 # +1 für die X Daten - also X Spalte und alle Y Spalten
                    
                self.datentabelle.blockSignals(True) # Kurz blockieren
                self.datentabelle.setRowCount(n_rows)
                self.datentabelle.setColumnCount(n_columns)
                

                #Spaltenüberschriften setzen
                header_labels = ["X"] + list(self.y_dict.keys())
                self.datentabelle.setHorizontalHeaderLabels(header_labels)

                for i in range(n_rows):
                    x_str = f"{self.x_data[i]:.4g}"
                    self.datentabelle.setItem(i, 0, QTableWidgetItem(x_str))
            
                for col_idx, (spalten_name, y_data) in enumerate(self.y_dict.items()):
                    for row_idx in range(n_rows):
                        y_str = f"{y_data[row_idx]:.4g}"
                        self.datentabelle.setItem(row_idx, col_idx + 1, QTableWidgetItem(y_str))

                self.datentabelle.blockSignals(False)
                

            except Exception as e:
                print(f"Tabellenberechnung abgebrochen. Error: {e}")

        else:
                n_rows = 50
                n_columns = 10
                self.datentabelle.setRowCount(n_rows)
                self.datentabelle.setColumnCount(n_columns)
                
        #Anzahl der Spalten berechnen
    
    def tabelle_zelle_geaendert(self, row, col):
        item = self.datentabelle.item(row, col)
        if item is None:
            return

        text = item.text().strip().replace(",", ".")

        self.datentabelle.blockSignals(True)
        try:
            # 1. Prüfen: Zahl eingegeben oder Zelle gelöscht?
            ist_leer = (text == "")
            neuer_wert = np.nan if ist_leer else float(text)
            
            n_rows = self.datentabelle.rowCount()

            # 2. Sicherstellen, dass self.x_data existiert
            if self.x_data is None:
                self.x_data = np.full(n_rows, np.nan, dtype=float)
                self.datentabelle.setHorizontalHeaderItem(0, QTableWidgetItem("X"))

            # 3. Zeilen erweitern falls nötig
            if row >= len(self.x_data):
                zusatz = np.full(row - len(self.x_data) + 1, np.nan, dtype=float)
                self.x_data = np.concatenate([self.x_data, zusatz])
                for k in self.y_dict:
                    self.y_dict[k] = np.concatenate([self.y_dict[k], zusatz.copy()])

            # 4. Wert eintragen
            if col == 0:
                if not self.x_data.flags.writeable:
                    self.x_data = self.x_data.copy()
                self.x_data[row] = neuer_wert
            else:
                spalten_namen = list(self.y_dict.keys())
                
                # Existiert diese Y-Spalte schon? Falls nein: sauber neu anlegen!
                if col - 1 >= len(spalten_namen):
                    gewaehlte_spalte = f"Datensatz {col}"
                    self.y_dict[gewaehlte_spalte] = np.full(len(self.x_data), np.nan, dtype=float)
                    
                    self.y_styles[gewaehlte_spalte] = {
                        "color": self.plot_color.name() if len(self.y_dict) == 1 else "#ff7f0e",
                        "linestyle": "",  # "" bedeutet kein Strich
                        "markerstyle": "o",
                        "markersize": 7,
                        "label": gewaehlte_spalte,
                        "y_err": None
                    }
                    
                    # ComboBox aktualisieren
                    self.aktive_y_combo.blockSignals(True)
                    # Falls vorher "No Data" drin stand, erst leeren
                    if self.aktive_y_combo.count() == 1 and "No Data" in self.aktive_y_combo.itemText(0):
                        self.aktive_y_combo.clear()
                    self.aktive_y_combo.addItem(gewaehlte_spalte)
                    self.aktive_y_combo.blockSignals(False)

                    # Legende und Header setzen
                    if len(self.y_dict) == 1:
                        self.legende_input.blockSignals(True)
                        self.legende_input.setText(gewaehlte_spalte)
                        self.legende_input.blockSignals(False)

                    self.datentabelle.setHorizontalHeaderItem(col, QTableWidgetItem(gewaehlte_spalte))
                else:
                    gewaehlte_spalte = spalten_namen[col - 1]

                # Wert ins Array schreiben
                if not self.y_dict[gewaehlte_spalte].flags.writeable:
                    self.y_dict[gewaehlte_spalte] = self.y_dict[gewaehlte_spalte].copy()
                self.y_dict[gewaehlte_spalte][row] = neuer_wert

                # --- Prüfen, ob die Spalte jetzt komplett leer gelöscht wurde ---
                if np.isnan(self.y_dict[gewaehlte_spalte]).all():
                    del self.y_dict[gewaehlte_spalte]
                    if gewaehlte_spalte in self.y_styles:
                        del self.y_styles[gewaehlte_spalte]

                    idx = self.aktive_y_combo.findText(gewaehlte_spalte)
                    if idx != -1:
                        self.aktive_y_combo.blockSignals(True)
                        self.aktive_y_combo.removeItem(idx)
                        self.aktive_y_combo.blockSignals(False)

                    self.datentabelle.setHorizontalHeaderItem(col, QTableWidgetItem(f"Y{col}"))

                    # War das die letzte Y-Spalte?
                    if not self.y_dict:
                        self.x_data = None
                        self.current_x = None
                        
                        t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])
                        self.aktive_y_combo.blockSignals(True)
                        self.aktive_y_combo.clear()
                        self.aktive_y_combo.addItem(t.get("y_data_combo", "No Data available"))
                        self.aktive_y_combo.blockSignals(False)
                        
                        self.legende_input.blockSignals(True)
                        self.legende_input.clear()
                        self.legende_input.blockSignals(False)
                    else:
                        self.lade_stil_in_gui()

            # Hintergrund weiß setzen
            item.setBackground(QColor("#ffffff"))
            self.datentabelle.blockSignals(False)

            # Plot neu zeichnen
            self.plot_aktualisieren()

        except ValueError:
            item.setBackground(QColor("#ffcccc"))
            self.datentabelle.blockSignals(False)
            
        except Exception as e:
            self.datentabelle.blockSignals(False)
            print(f"Fehler bei Zelländerung: {type(e).__name__}: {e}")

    def reset_everything(self):
        # 1. Datenstrukturen komplett leeren
        self.x_data = None
        self.x_data_raw = None
        self.x_err = None
        self.y_err = None
        self.current_x = None
        self.current_y = None
        self.y_dict = {}
        self.y_dict_raw = {}
        self.y_styles = {}

        # 2. Dropdown für die Datenreihen zurücksetzen
        t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])
        self.aktive_y_combo.blockSignals(True)
        self.aktive_y_combo.clear()
        self.aktive_y_combo.addItem(t.get("y_data_combo", "No Data available"))
        self.aktive_y_combo.blockSignals(False)

        # 3. Textfelder leeren
        self.legende_input.blockSignals(True)
        self.legende_input.clear()
        self.legende_input.blockSignals(False)

        self.polyfit_input_label.blockSignals(True)
        self.polyfit_input_label.clear()
        self.polyfit_input_label.setEnabled(False)
        self.polyfit_input_label.blockSignals(False)

        # 4. Fit- und Extrema-Auswahl zurücksetzen
        self.polyfit_combo.blockSignals(True)
        self.polyfit_combo.setCurrentIndex(0)
        self.polyfit_combo.blockSignals(False)

        self.showmaxmin_combo.blockSignals(True)
        self.showmaxmin_combo.setCurrentIndex(0)
        self.showmaxmin_combo.setEnabled(False)
        self.showmaxmin_combo.blockSignals(False)
        self.save_maxmin.setEnabled(False)

        # 5. Datentabelle leeren und auf 50x10 Standardraster zurücksetzen
        self.datentabelle.blockSignals(True)
        self.datentabelle.clear()
        self.datentabelle.setRowCount(50)
        self.datentabelle.setColumnCount(10)
        
        # Header auf Standard beschriften (X, Y1, Y2, ...)
        standard_header = ["X"] + [f"Y{i}" for i in range(1, 10)]
        self.datentabelle.setHorizontalHeaderLabels(standard_header)
        self.datentabelle.blockSignals(False)

        # 6. Plot zurücksetzen (leert die Achse und setzt den Anfangstitel)
        self.plot_aktualisieren()

        QMessageBox.information(
                    self, 
                    "Reset", 
                    ("Alle Daten wurden gelöscht und alle Einstellungen zurückgesetzt!" if self.aktuelle_sprache == "de" else "Succesfully reset all data and!" ))




class GroesstfehlerDialog(QDialog):
    #grundgerüst wird aufgebaut
    def __init__(self, parent=None, x_data=None, y_data=None, rechen_funktion = None, sprache= "de"):
        super().__init__(parent)
        self.setWindowTitle("Datenauswertungmanipulation und Größtfehlerrechner")
        self.resize(650, 600)

        self.imported_err = None
        self.x_data = x_data
        self.y_data = y_data
        self.y_data_orig = y_data.copy() if isinstance(y_data, np.ndarray) else y_data  # ORIGINAL SICHERN!
        self.rechen_funktion = rechen_funktion
        self.aktuelle_sprache = sprache

        # Hauptlayout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        
        layout_lbl_ziel = QHBoxLayout()
        self.lbl_ziel = QLabel()
        layout_lbl_ziel.addWidget(self.lbl_ziel)
        layout_lbl_ziel.addWidget(MeinPlotterApp.erstelle_hilfe_button(self.get_hilfetext()))
        self.layout.addLayout(layout_lbl_ziel)

        # 1. Zielauswahl (Wohin sollen die berechneten Daten?)
        
        ziel_layout = QHBoxLayout()
        self.radio_y = QRadioButton("Y-Daten & Y-Errorbar (vertikal)")
        self.radio_x = QRadioButton("X-Daten & X-Errorbar (horizontal)")
        self.radio_nur_ausgabe = QRadioButton("Nur Berechnen (Tabelle / Einzelwert)")
        
        self.radio_y.setChecked(True) # Standardmäßig Y wählen
        
        ziel_layout.addWidget(self.radio_y)
        ziel_layout.addWidget(self.radio_x)
        ziel_layout.addWidget(self.radio_nur_ausgabe)
        self.layout.addLayout(ziel_layout)

        # 3. Latex-gerenderte Formel
        self.lbl_latex_header = QLabel()
        self.layout.addWidget(self.lbl_latex_header)
        self.latex_formel = QLabel()
        self.latex_formel.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
            }
        """)
        self.latex_formel.setText("<i>Die gerenderte Formel erscheint hier...</i>")
        self.latex_formel.setTextFormat(Qt.TextFormat.RichText)
        self.layout.addWidget(self.latex_formel)

        # 4. Formeleingabe
        layout_formel_input = QHBoxLayout()
        self.lbl_formel_title = QLabel()
        layout_formel_input.addWidget(self.lbl_formel_title)
        layout_formel_input.addStretch()
        self.layout.addLayout(layout_formel_input)

        self.formel_input = QLineEdit()
        self.formel_input.setPlaceholderText("z. B. 4 * pi^2 * (m * V0) / (A^2 * p * tau^2)")
        self.layout.addWidget(self.formel_input)

        # Excel Unsicherheiten Button
        self.open_excel_layout = QHBoxLayout()
        self.btn_import_excel = QPushButton()
        self.open_excel_layout.addWidget(self.btn_import_excel)
        self.layout.addLayout(self.open_excel_layout)

        #Lade Datenspalte Button
        self.open_data_layout = QHBoxLayout()
        self.btn_import_data = QPushButton("Daten laden")
        self.open_data_layout.addWidget(self.btn_import_data)

        self.btn_save_data = QPushButton("Daten speichern")
        self.open_data_layout.addWidget(self.btn_save_data)

        self.layout.addLayout(self.open_data_layout)


        # 5. Dynamischer Bereich für Variablen-Eingaben
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.layout.addWidget(self.form_widget)

        self.inputs_werte = {}
        self.inputs_unsicherheiten = {}
        self.inputs_digitserr = {}

        # NEU: Dauerhafter Speicher für getippte Werte
        self.gespeicherte_werte = {}
        self.gespeicherte_unsicherheiten = {}
        self.gespeicherte_digits = {}

        # 4. Live-Ergebistabelle
        self.lbl_tabelle_title = QLabel()
        self.layout.addWidget(self.lbl_tabelle_title)
        self.tabelle = QTableWidget()
        self.layout.addWidget(self.tabelle)

        # 5. OK / Abbrechen Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        # Signale verbinden
        self.formel_input.textChanged.connect(self.aktualisiere_variablen_felder) # Das hier ist essentiell
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.btn_import_excel.clicked.connect(self.importiere_unsicherheiten_excel)
        self.radio_y.toggled.connect(self.aktualisiere_button_status)
        self.radio_x.toggled.connect(self.aktualisiere_button_status)
        self.radio_nur_ausgabe.toggled.connect(self.aktualisiere_button_status)
        self.btn_import_data.clicked.connect(self.importiere_singledatacolumns)
        self.btn_save_data.clicked.connect(self.save_data)

        # Prüfen, ob überhaupt Plot-Daten vorliegen:
        keine_daten = (self.x_data is None) and (self.y_data is None)
        if keine_daten:
            self.radio_nur_ausgabe.setChecked(True)
            self.radio_y.setEnabled(False)
            self.radio_x.setEnabled(False)

        # Einmaligen Start-Zustand setzen (da Y standardmäßig aktiv ist, wird er initial ausgegraut)
        self.aktualisiere_button_status()

        # EINMAL retranslate_ui aufrufen
        self.retranslate_ui()
    
    def aktualisiere_variablen_felder(self):

        #Sind Werte vorhanden? Wenn ja, speichern!
        for var, widget in self.inputs_werte.items():
            self.gespeicherte_werte[var] = widget.text()
        for var, widget in self.inputs_unsicherheiten.items():
            self.gespeicherte_unsicherheiten[var] = widget.text()
        for var, widget in self.inputs_digitserr.items():
            self.gespeicherte_digits[var] = widget.text()

        text = self.formel_input.text().strip()
        if not text:
            return
        try: 
            #Latex Formel richtig darstellen:
            self.latex_formel.setText(self.latex_to_html(text)) #strip() schlimm?

            # SymPy Ausdruck parsen & Variablen ermitteln #nochmal das ganze? Haben wir das nicht oben in unserer ersten Klasse schon in berechne_größtfehler?
            # SymPy Ausdruck parsen & Variablen ermitteln
            formel_sauber = text.replace("^", "**")

            # Wenn diff(y) vorkommt, erzwingen wir 'y' (und 'x') in der Variablenliste!
            formel_fuer_parsing = re.sub(r"diff\s*\(\s*y\s*(,\s*x\s*)?\)", "_dydx + y + x", formel_sauber)

            expr = sp.parse_expr(formel_fuer_parsing, transformations=standard_transformations + (implicit_multiplication_application,))
            variablen = sorted([s.name for s in expr.free_symbols if s.name not in ["pi", "_dydx"]])

                    #Altes Formular leeren (alle Zeilen löschen)
            while self.form_layout.rowCount() > 0:
                self.form_layout.removeRow(0)
        
            self.inputs_werte.clear()
            self.inputs_unsicherheiten.clear()
            self.inputs_digitserr.clear()

            # Für jede Variable Eingabefelder im Formlayout anlegen

            t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])

            # Welches Ziel ist ausgewählt? ('x' oder 'y')
            ziel_var = "x" if self.radio_x.isChecked() else "y"

            for var in variablen:
            #Standardwerte 0 setzen, solange nix eingegeben wurde
                if var in self.gespeicherte_werte and self.gespeicherte_werte[var] != "":
                    val_text = self.gespeicherte_werte[var]
                else: 
                    val_text = var if var.lower() in ["x", "y"] else ""

                val_input = QLineEdit(val_text)
                val_input.setPlaceholderText(t["gf_val_ph"].format(var=var))

            #Unsicherheiten mit vorher eingegeben Werten befüllen
                err_text = self.gespeicherte_unsicherheiten.get(var, "0")
                digit_text = self.gespeicherte_digits.get(var, "0")
                err_input = QLineEdit(err_text)
                digiterr_input = QLineEdit(digit_text)
                
                # Prüfen, ob für diese konkrete Variable ein Import vorliegt:
                ziel_var = "x" if self.radio_x.isChecked() else "y"
                hat_import = (var.lower() == ziel_var and self.imported_err is not None)

                if hat_import:
                    hinweis = "Excel-Import" if self.aktuelle_sprache == "de" else "Excel Import"
                    err_input.setText(hinweis)
                    err_input.setEnabled(False)
                    err_input.setStyleSheet("background-color: #e0e0e0; color: #555555; font-style: italic;")

                    digiterr_input.setText(hinweis)
                    digiterr_input.setEnabled(False)
                    digiterr_input.setStyleSheet("background-color: #e0e0e0; color: #555555; font-style: italic;")
                else:
                    err_input.setPlaceholderText(t["gf_err_ph"].format(var=var))
                    digiterr_input.setPlaceholderText("z.B. 4" if self.aktuelle_sprache == "de" else "e.g. 4")
                val_input.textChanged.connect(self.aktualisiere_tabelle_live)
                err_input.textChanged.connect(self.aktualisiere_tabelle_live)
                digiterr_input.textChanged.connect(self.aktualisiere_tabelle_live)




                self.inputs_werte[var] = val_input
                self.inputs_unsicherheiten[var] = err_input
                self.inputs_digitserr[var] = digiterr_input
                
                #Neu
                self.valueAnderror = QHBoxLayout()
                self.valueAnderror.addWidget(QLabel(f"<b>{var}:</b>"))
                self.valueAnderror.addWidget(val_input)

                self.valueAnderror.addWidget(QLabel(f"Δ{var}:"))
                self.valueAnderror.addWidget( err_input)

                self.valueAnderror.addWidget(QLabel("±X digits:"))
                self.valueAnderror.addWidget(digiterr_input)

                self.form_layout.addRow(self.valueAnderror)

                #Neu
                #self.form_layout.addRow(QLabel(f"<b>{var}:</b>"), val_input)
                #self.form_layout.addRow(QLabel(f"Δ{var}:"), err_input)
            
            self.aktualisiere_tabelle_live()

        except Exception:
            #falls die Formel noch getippt wird oder Ähnliches
            pass

    def get_daten(self):
        """Liest alle Eingabefelder aus und liefert die Dictionaries und die Formel zurück."""
        werte = {}
        unsicherheiten = {}
        digit_unsicherheiten = {}
        raw_texte = {}

        # 1. WERTE ALESEN (x, y und Konstanten)
        for var, input_widget in self.inputs_werte.items():
            txt = input_widget.text().strip()
            raw_texte[var] = txt
            var_lower = var.lower()

            # Wenn 'x' in der Formel vorkommt und das Feld "x" heißt oder leer ist
            if var_lower == "x":
                if txt == "" or txt.lower() == "x":
                    werte[var] = self.x_data if self.x_data is not None else 0.0
                else:
                    try:
                        werte[var] = GroesstfehlerDialog.parse_zahl_eingabe(txt)
                    except Exception:
                        werte[var] = self.x_data if self.x_data is not None else 0.0

            # Wenn 'y' in der Formel vorkommt und das Feld "y" heißt oder leer ist
            elif var_lower == "y":
                if txt == "" or txt.lower() == "y":
                    werte[var] = self.y_data if self.y_data is not None else 0.0
                else:
                    try:
                        werte[var] = GroesstfehlerDialog.parse_zahl_eingabe(txt)
                    except Exception:
                        werte[var] = self.y_data if self.y_data is not None else 0.0

            # Alle anderen Variablen (Konstanten wie A, R_0 etc.)
            else:
                if not txt:
                    werte[var] = 0.0
                else:
                    try:
                        werte[var] = GroesstfehlerDialog.parse_zahl_eingabe(txt)
                    except Exception:
                        werte[var] = 0.0

        # 2. UNSICHERHEITEN AUSLESEN (Δx, Δy und ΔKonstanten)
        ziel_var = "x" if self.radio_x.isChecked() else "y"

        #Digit Unsicherheiten

        for var, input_widget in self.inputs_digitserr.items():
            txt_digit = input_widget.text().strip()
            if not txt_digit:
                digit_unsicherheiten[var] = 0.0
            else:
                try: 
                    digit_unsicherheiten[var] = float(txt_digit.replace(",", "."))
                except Exception:
                    digit_unsicherheiten[var] = 0.0

        for var, input_widget in self.inputs_unsicherheiten.items():
            var_lower = var.lower()
            
            # 1. Wurde für die Ziel-Variable eine Excel importiert?
            if var_lower == ziel_var and self.imported_err is not None:
                unsicherheiten[var] = self.imported_err
            else:
                txt = input_widget.text().strip()
                if not txt or txt in ["Excel-Import", "Excel Import"]:
                    unsicherheiten[var] = 0.0
                else:
                    try:
                        unsicherheiten[var] = GroesstfehlerDialog.parse_zahl_eingabe(txt)
                    except Exception:
                        unsicherheiten[var] = 0.0

        return self.formel_input.text().strip(), werte, unsicherheiten, digit_unsicherheiten, raw_texte
   
    def aktualisiere_tabelle_live(self):
            formel, werte, unsicherheiten, digit_unsicherheiten, raw_texte = self.get_daten()
            if not formel:
                return

            try:
                if self.rechen_funktion is None:
                    return
                
                f_val, f_err = self.rechen_funktion(formel, werte, unsicherheiten, digit_unsicherheiten, raw_texte)

                # Sicherstellen, dass f_val und f_err Arrays sind
                if isinstance(f_val, (int, float, np.number)):
                    if self.x_data is not None:
                        n_rows = len(self.x_data)
                    elif self.y_data is not None and isinstance(self.y_data, np.ndarray):
                        n_rows = len(self.y_data)
                    else:
                        n_rows = 1
                    f_val = np.full(n_rows, f_val)
                    f_err = np.full(n_rows, f_err)

                n_zeilen = len(f_val)
                self.tabelle.setRowCount(n_zeilen)
                self.tabelle.setColumnCount(5)
                self.tabelle.setHorizontalHeaderLabels(["Index", "X-Data", "Y-Data", "Ergebnis f", "Fehler Δf"])

                # NACHHER:
                for i in range(n_zeilen):
                    if self.x_data is not None and i < len(self.x_data):
                        x_str = f"{self.x_data[i]:.4g}"
                    else:
                        x_str = f"{i + 1}"  # Zeigt als x einfach den Punkt-Index 1, 2, 3... an

                    y_str = f"{self.y_data[i]:.4g}" if self.y_data is not None and i < len(self.y_data) else "-"
                    res_str = f"{f_val[i]:.4g}"
                    err_str = f"± {f_err[i]:.4g}"

                    self.tabelle.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                    self.tabelle.setItem(i, 1, QTableWidgetItem(x_str))
                    self.tabelle.setItem(i, 2, QTableWidgetItem(y_str))
                    self.tabelle.setItem(i, 3, QTableWidgetItem(res_str))
                    self.tabelle.setItem(i, 4, QTableWidgetItem(err_str))

            except Exception as e:
                # Ignorieren, falls Formel oder Felder noch unvollständig ausgefüllt sind
                print(f"Fehler bei Live-Berechnung: {e}")

    def latex_to_html(self, formel):
        if not formel:
            return ""

        # 1. Erst Potenz-Sterne (** zu ^) umwandeln
        text_html = formel.replace("**", "^")

        # 2. Danach einzelne Malzeichen (*) in &middot; umwandeln
        text_html = text_html.replace("*", " &middot; ")

        # 3. exp(...) in e^(...) umwandeln
        text_html = re.sub(r"\bexp\((.*?)\)", r"<i>e</i><sup>\1</sup>", text_html)

        # 4. Verschachtelte sqrt(...) Klammern exakt auflösen:
        while "sqrt(" in text_html:
            start_idx = text_html.find("sqrt(")
            pos = start_idx + 5  # Länge von "sqrt("
            klammer_ebene = 1
            
            # Gehe den String durch, bis die passend schließende Klammer gefunden ist
            while pos < len(text_html) and klammer_ebene > 0:
                if text_html[pos] == "(":
                    klammer_ebene += 1
                elif text_html[pos] == ")":
                    klammer_ebene -= 1
                pos += 1
            
            # Wenn eine passende Schließklammer gefunden wurde
            if klammer_ebene == 0:
                inhalt = text_html[start_idx + 5 : pos - 1]
                ersetzung = f"&radic;<span style='text-decoration: overline;'>{inhalt}</span>"
                text_html = text_html[:start_idx] + ersetzung + text_html[pos:]
            else:
                # Falls die Klammer im Formeltext noch nicht geschlossen wurde
                break

        # NEU: diff(y) in der gerenderten Formel-Vorschau schön darstellen:
        text_html = re.sub(
            r"diff\s*\(\s*y\s*(,\s*x\s*)?\)", 
            r"<sup>dy</sup>/<sub>dx</sub>", 
            text_html
        )

        # 5. Indizes umwandeln (z. B. R_(0) oder R_0)
        text_html = re.sub(r"_\((.*?)\)", r"<sub>\1</sub>", text_html)
        text_html = re.sub(r"_([a-zA-Z0-9]+)", r"<sub>\1</sub>", text_html)

        # 6. Exponenten umwandeln (z. B. x^(2) oder x^2)
        text_html = re.sub(r"\^\((.*?)\)", r"<sup>\1</sup>", text_html)
        text_html = re.sub(r"\^([a-zA-Z0-9\-]+)", r"<sup>\1</sup>", text_html)

        # 7. Bekannte Konstanten umwandeln
        text_html = re.sub(r"\bpi\b", "&pi;", text_html, flags=re.IGNORECASE)

        # 8. HTML-Modus für QLabel garantieren
        return text_html

    def retranslate_ui(self):
        t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])

        self.setWindowTitle(t["gf_title"])
        self.lbl_ziel.setText(f"<b>{t['gf_target']}</b>")
        self.radio_y.setText(t["gf_radio_y"])
        self.radio_x.setText(t["gf_radio_x"])
        self.radio_nur_ausgabe.setText(t["gf_radio_none"])
        
        self.lbl_latex_header.setText(f"<b>{t['gf_rendered_formula']}</b>")
        if not self.formel_input.text().strip():
            self.latex_formel.setText(f"<i>{t['gf_rendered_ph']}</i>")
            
        self.lbl_formel_title.setText(f"<b>{t['gf_formula_label']}</b>")
        self.formel_input.setPlaceholderText(t["gf_formula_ph"])
        self.btn_import_excel.setText(t["gf_btn_excel"])
        self.lbl_tabelle_title.setText(f"<b>{t['gf_preview_table']}</b>")
        self.btn_import_data.setText(t["btn_loadsinglecolumn"]) 
        self.btn_save_data.setText(t["btn_save_data"])

    def get_hilfetext(self):
        if self.aktuelle_sprache == "en":
            return (
                "<b>User Guide: Data Evaluation &amp; Error Calculator</b><br><br>"
                "<b>1. Target Selection:</b> Choose whether results/error bars apply to X-axis, Y-axis, or table only.<br><br>"
                "<b>2. Syntax:</b> Use <code>x</code> and <code>y</code> for datasets. Custom variables create constant input fields. <b> "
                "Important: </b> Even if the X or Y Axis in your Experiment isn't named with <code>X</code> or <code>Y</code> (so e.g. time <code>t</code> or distance <code>s</code>), the calculator will still take <code>X</code> and <code>Y</code> as the inputs for the datasets.<br>"
                "• Functions: <code>sqrt()</code>, <code>exp()</code>, <code>log()</code>, <code>sin()</code>, <code>cos()</code>, <code>tan()</code><br>"
                "• Derivative: <code>diff(y)</code> calculates <sup>dy</sup>/<sub>dx</sub> via <code>np.gradient</code>.<br><br>"
                "<b>Import Uncertainties from Excel:</b> "
                "It is possible to import uncertainties for either X OR Y values. Simply select &lt;X-Data&gt; or &lt;Y-Data&gt; above "
                "depending on which error it is, then import the errors via the button. After that, enter either &lt;x&gt; or &lt;y&gt; "
                "into the formula field to apply the respective errors.<br><br>"
                "<b>Import Both X and Y Uncertainties:</b><br>"
                "1. Import X-errors, select &lt;X-Data / X-Errorbar&gt; above, enter X in the formula field, and press &lt;Ok&gt;.<br>"
                "2. Afterwards, reopen the window, load Y-errors, select &lt;Y-Data / Y-Errorbar&gt; above, enter Y in the formula field, and press &lt;Ok&gt; again.<br><br>"
            )
        else:
            return (
                "<b>Bedienungsanleitung: Datenauswertung &amp; Größtfehlerrechner</b><br><br>"
                "<b>1. Zielauswahl:</b> Wähle aus, ob Werte/Fehlerbalken auf X-, Y-Achse oder nur in die Tabelle geschrieben werden.<br><br>"
                "<b>2. Formelsyntax:</b> <code>x</code> und <code>y</code> für Messreihen; andere Namen erzeugen Eingabefelder für Konstanten.  <b> Wichtig: </b>"
                "Selbst wenn in einer Messung die X-Achse z.B. die Zeit beschreibt, also <code> t </code> abgekürzt wird in einer Formel, so heißen die X-Daten im Programm immer noch <code> X </code>! Selbes gilt für die Y-Achse.<br>"
                "• Funktionen: <code>sqrt()</code>, <code>exp()</code>, <code>log()</code>, <code>sin()</code>, <code>cos()</code>, <code>tan()</code><br>"
                "• Ableitung: <code>diff(y)</code> berechnet <sup>dy</sup>/<sub>dx</sub> per <code>np.gradient</code>.<br><br>"
                "<b>Importiere Unsicherheiten als Excel:</b> "
                "Es ist möglich, Unsicherheiten für entweder X ODER Y Werte zu importieren. Dazu muss oben einfach &lt;X-Daten&gt; oder &lt;Y-Daten&gt; ausgewählt werden, "
                "je nachdem um welche Fehler es sich handelt, im Anschluss werden die Fehler über den Button importiert. Danach muss noch in die Formelleiste "
                "entweder &lt;x&gt; oder &lt;y&gt; eingegeben werden, um die jeweiligen Fehler wirksam zu machen.<br><br>"
                "<b>Sowohl X- als auch Y-Unsicherheiten importieren:</b><br>"
                "1. X-Fehler importieren, oben &lt;X-Daten / X-Errorbar&gt; auswählen, in der Formelleiste X eingeben, &lt;Ok&gt; drücken.<br>"
                "2. Im Anschluss das Fenster neu öffnen, Y-Fehler laden, oben &lt;Y-Daten / Y-Errorbar&gt; auswählen, Y ins Formelfeld eingeben und wieder &lt;Ok&gt; drücken.<br><br>"
            )

    def importiere_unsicherheiten_excel(self):
        is_en = self.aktuelle_sprache == "en"
        ziel = "X" if self.radio_x.isChecked() else "Y"
        
        # 1. Info-Box mit Format-Hinweis anzeigen
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Format-Hinweis" if not is_en else "Format Notice")
        msgBox.setText("<b>Struktur für den Unsicherheiten-Import</b>" if not is_en else "<b>Structure for Uncertainty Import</b>")
        
        html_text = (
            f"Bitte wähle eine Excel-Datei mit <b>genau EINER Spalte</b> aus.<br><br>"
            f"Da oben <b>{ziel}-Daten</b> ausgewählt sind, werden diese Werte als <b>Δ{ziel}</b> geladen:<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            f"  <tr style='background-color: #e0e0e0; font-weight: bold;'><td>Δ{ziel} / Einheit</td></tr>"
            "  <tr><td>0.02</td></tr>"
            "  <tr><td>0.05</td></tr>"
            "  <tr><td>0.01</td></tr>"
            "</table><br>"
            "• Die erste Zeile kann optional eine Kopfzeile/Einheit sein.<br>"
            "• Die Länge der Spalte sollte der Datenlänge entsprechen."
        ) if not is_en else (
            f"Please select an Excel file with <b>exactly ONE column</b>.<br><br>"
            f"Since <b>{ziel}-Data</b> is selected above, these values will be loaded as <b>Δ{ziel}</b>:<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            f"  <tr style='background-color: #e0e0e0; font-weight: bold;'><td>Δ{ziel} / Unit</td></tr>"
            "  <tr><td>0.02</td></tr>"
            "  <tr><td>0.05</td></tr>"
            "  <tr><td>0.01</td></tr>"
            "</table><br>"
            "• The first row may optionally be a header/unit.<br>"
            "• Column length should match the dataset length."
        )
        
        msgBox.setInformativeText(html_text)
        msgBox.exec()

        # 2. Dateiauswahl öffnen
        dateiname, _ = QFileDialog.getOpenFileName(
            self, 
            "Unsicherheiten-Excel auswählen" if not is_en else "Select Uncertainty Excel", 
            "", 
            "Excel-Dateien (*.xlsx *.xls)"
        )
        
        if dateiname:
            try:
                raw_df = pd.read_excel(dateiname, header=None).dropna(how="all")
                raw_df = raw_df.dropna(how="all", axis=1)

                if raw_df.shape[1] != 1:
                    QMessageBox.warning(
                        self, 
                        "Spaltenfehler" if not is_en else "Column Error", 
                        "Die Datei muss exakt EINE Spalte enthalten!" if not is_en else "The file must contain exactly ONE column!"
                    )
                    return

                # Header unterscheiden
                try:
                    float(raw_df.iloc[0, 0])
                    datafile = raw_df
                except (ValueError, TypeError):
                    datafile = raw_df.iloc[1:].reset_index(drop=True)

                self.imported_err = datafile.iloc[:, 0].dropna().to_numpy(dtype=float)

                QMessageBox.information(
                    self, 
                    "Erfolg" if not is_en else "Success", 
                    f"Es wurden {len(self.imported_err)} Werte für Δ{ziel} geladen!" if not is_en else f"Successfully loaded {len(self.imported_err)} values for Δ{ziel}!"
                )
                
                # Eingabefelder direkt aktualisieren
                self.aktualisiere_variablen_felder()

            except Exception as e:
                QMessageBox.critical(self, "Fehler" if not is_en else "Error", f"Details: {str(e)}")


    def aktualisiere_button_status(self):
        nur_berechnen_aktiv = self.radio_nur_ausgabe.isChecked()
        self.btn_import_data.setEnabled(nur_berechnen_aktiv)

        # Wenn man NICHT auf "Nur Berechnen" steht, Single-Column-Daten verwerfen:
        if not nur_berechnen_aktiv:
            # Setzt y_data wieder strikt auf den originalen Datensatz zurück
            self.y_data = self.y_data_orig.copy() if isinstance(self.y_data_orig, np.ndarray) else self.y_data_orig


        if self.radio_x.isChecked():
            neuer_text = "x"
            self.btn_import_excel.setText("Importiere X-Unsicherheiten als Excel" if self.aktuelle_sprache == "de" else "Import X-Errors from Excel" )
        else:
            # Gilt sowohl für radio_y als auch für radio_nur_ausgabe
            neuer_text = "y"
            self.btn_import_excel.setText("Importiere Y-Unsicherheiten als Excel" if self.aktuelle_sprache == "de" else "Import Y-Errors from Excel" )
        self.formel_input.setText(neuer_text)
            # Aktualisiert das Formular und die Vorschau-Tabelle mit den originalen Daten
        self.aktualisiere_variablen_felder()
   
    def importiere_singledatacolumns(self):
        # 1. Info-Box mit Format-Hinweis anzeigen
        is_en = self.aktuelle_sprache == "en"
        
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Format-Hinweis" if not is_en else "Format Notice")
        msgBox.setText("<b>Struktur für den Daten-Import</b>" if not is_en else "<b>Structure for Data Import</b>")
        
        html_text = (
            "Bitte wähle eine Excel-Datei mit <b>genau EINER Spalte</b> aus, die Daten enthält:<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            "  <tr style='background-color: #e0e0e0; font-weight: bold;'><td>Δy / Einheiten</td></tr>"
            "  <tr><td>schwingungsdauer tau</td></tr>"
            "  <tr><td>0.56</td></tr>"
            "  <tr><td>0.57</td></tr>"
            "  <tr><td>0.58</td></tr>"
            "</table><br>"
            "• Die erste Zeile kann optional den Namen/Einheit enthalten.<br>"
            "• Die Spaltenlänge ist variabel"
        ) if not is_en else (
            "Please select an Excel file with <b>exactly ONE column</b> containing the data :<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            "  <tr style='background-color: #e0e0e0; font-weight: bold;'><td> period tau</td></tr>"
            "  <tr><td>0.56</td></tr>"
            "  <tr><td>0.57</td></tr>"
            "  <tr><td>0.58</td></tr>"
            "</table><br>"
            "• The first row may optionally contain headers/units.<br>"
            "• The column length is free to choose."
        )
        
        msgBox.setInformativeText(html_text)
        msgBox.exec()

        # 2. Dateiauswahl öffnen
        dateiname, _ = QFileDialog.getOpenFileName(
            self, 
            "Daten-Excel auswählen" if not is_en else "Select Data Excel", 
            "", 
            "Excel-Dateien (*.xlsx *.xls)"
        )
        
        if dateiname:
            try:
                raw_df = pd.read_excel(dateiname, header=None).dropna(how="all")
                raw_df = raw_df.dropna(how="all", axis=1)

                if raw_df.shape[1] != 1:
                    QMessageBox.warning(
                        self, 
                        "Spaltenfehler" if not is_en else "Column Error", 
                        "Die Datei muss exakt EINE Spalte enthalten!" if not is_en else "The file must contain exactly ONE column!"
                    )
                    return

                # Header unterscheiden (ob Zeile 1 Text ist)
                try:
                    float(raw_df.iloc[0, 0])
                    datafile = raw_df
                except (ValueError, TypeError):
                    datafile = raw_df.iloc[1:].reset_index(drop=True)

                self.y_data = datafile.iloc[:, 0].dropna().to_numpy(dtype=float)

                # Erfolgsmeldung & Eingabefelder sperren/aktualisieren
                QMessageBox.information(
                    self, 
                    "Erfolg" if not is_en else "Success", 
                    f"Es wurden {len(self.y_data)} Datenwerte erfolgreich geladen!" if not is_en else f"Successfully loaded {len(self.y_data)} data values!"
                )
                
                # Eingabefelder neu rendern/sperren
                self.formel_input.setText("y")

            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Details: {str(e)}")

    @staticmethod
    def parse_zahl_eingabe(txt):
        """Wandelt Ausdrücke wie '201.44*10^-6' oder '1.5*10**3' sauber in float um."""
        s = txt.strip().replace(",", ".")
        # Wandelt z. B. '*10^-6' oder '*10**-6' direkt in 'e-6' um:
        s = re.sub(r"\*10\^([+-]?\d+)", r"e\1", s)
        s = re.sub(r"\*10\*\*([+-]?\d+)", r"e\1", s)
        # Potenzzeichen für verbleibende Rechnungen korrigieren
        s = s.replace("^", "**")
        return float(eval(s))

    def save_data(self):
        formel, werte, unsicherheiten, digit_unsicherheiten, raw_texte = self.get_daten()
        if not formel: 
            Warning_text = ("Es sind keine Daten zum Exportieren vorhanden" if self.aktuelle_sprache == "de" else "No data for export available")
            QMessageBox.warning(self, "Keine Daten", Warning_text)
            return 
        try:
            if self.rechen_funktion is None:
                QMessageBox.warning(self, "Keine Daten", "An Error occured")
                return
            f_val, f_err = self.rechen_funktion(formel, werte, unsicherheiten, digit_unsicherheiten, raw_texte)
            if isinstance(f_val, (int, float, np.number)):
                f_val = np.array([f_val])
                f_err = np.array([f_err])

            #Abfragen, um was für daten es sich überhaupt handelt
            if self.radio_y.isChecked():
                y_exportData = f_val
                y_exportError = f_err
                x_exportData = self.x_data
                df = pd.DataFrame({"X-Values": x_exportData,"Y-Values": y_exportData, "Y-Errors": y_exportError})

            if self.radio_x.isChecked():
                x_exportData = f_val
                x_exportError = f_err
                y_exportData = self.y_data
                df = pd.DataFrame({"X-Values": x_exportData,"X-errors": x_exportError, "Y-Data": y_exportData})

            if self.radio_nur_ausgabe.isChecked():
                y_exportData = f_val
                y_exportError = f_err
                df = pd.DataFrame({"Y-Values": y_exportData,"Y-errors": y_exportError})

                    # 3. Datei-Speicherdialog öffnen
            dateiname, _ = QFileDialog.getSaveFileName(
                self,
                "Daten speichern",
                "EditedData.xlsx",
                "Excel-Arbeitsmappe (*.xlsx);;CSV-Datei (*.csv)"
            )

            # 4. Datei auf die Festplatte schreiben
            if dateiname:
                try:
                    if dateiname.endswith(".csv"):
                        df.to_csv(dateiname, index=False, sep=";", float_format="%.4f")
                    else:
                        df.to_excel(dateiname, index=False, float_format="%.4f")

                    QMessageBox.information(
                        self,
                        "Erfolg",
                        f"Die Daten wurden erfolgreich gespeichert unter:\n{dateiname}"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Fehler beim Speichern",
                        f"Die Datei konnte nicht gespeichert werden (ist sie eventuell noch in Excel geöffnet?):\n\n{str(e)}"
                    )

        except Exception as e: 
            print(f"Fehler beim Abspeichern der Daten: {e}")


        
            


class MittelwertDialog(QDialog):
    #Init Funktion
    def __init__(self, parent = None, sprache = "de"):
        super().__init__(parent)
        self.setWindowTitle("Mittelwert-Rechner")
        self.aktuelle_sprache = sprache
        self.resize(675, 550)

        #Hauptlayout

        # 1. Hauptlayout für den Dialog anlegen
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 2. Widgets hinzufügen
        
        
        layout_btn_excel = QHBoxLayout()
        layout_2_buttons = QVBoxLayout()
        self.lbl_mean_calculator = QLabel("<b>Mittelwert & Standardabweichung berechnen</b>")
        layout_btn_excel.addWidget(self.lbl_mean_calculator)


        self.btn_excel_laden = QPushButton("Excel für Mittelwerte laden")
        self.btn_excel_laden.clicked.connect(self.open_excel)
        layout_2_buttons.addWidget(self.btn_excel_laden)
        
        self.btn_excel_save = QPushButton("Mittelwerte als Excel speichern")
        self.btn_excel_save.clicked.connect(self.save_excel)
        layout_2_buttons.addWidget(self.btn_excel_save)

        layout_btn_excel.addWidget(MeinPlotterApp.erstelle_hilfe_button(self.get_hilfetext()))
        layout_btn_excel.addLayout(layout_2_buttons)
        self.layout.addLayout(layout_btn_excel)

        # 3. Live-Mittelwertabelle
        self.lbl_dataAndresult = QLabel()
        self.layout.addWidget(self.lbl_dataAndresult)
        self.tabelle = QTableWidget()
        self.layout.addWidget(self.tabelle)

        # Platzhalter nach unten
        #self.layout.addStretch()

        #OK / Abbrechen Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)
        self.button_box.rejected.connect(self.reject)

        # 1. Erstmalig eine leere 3x10 Tabelle für manuelle Eingaben anlegen
        self.erstelle_leere_start_tabelle()

        # 2. Signal verbinden: Wenn der Anwender eine Zelle editiert -> Live Neu berechnen!
        self.tabelle.cellChanged.connect(self.manuelle_eingabe_geandert)

        # EINMAL retranslate_ui aufrufen
        self.retranslate_ui()

    def get_infotext_html(self):
        if self.aktuelle_sprache == "de":
            return("Damit die Daten fehlerfrei eingelesen werden, beachte bitte folgendes (beispielhaftes) Format:<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            "  <tr style='background-color: #e0e0e0; font-weight: bold;'>"
            "    <td>Mittelwertspalte 1</td><td>Spalte 2(optional) </td><td>Spalte 3 (optional) </td><td>Spalte n</td>"
            "  </tr>"
            "  <tr><td>3.5</td><td>10.2</td><td>20.5</td><td>val1</td></tr>"
            "  <tr><td>3.6</td><td>11.4</td><td>20.1</td><td>val2</td></tr>"
            "  <tr><td>3.2</td><td>10.5</td><td>20.8</td><td>val3</td></tr>"
            "  <tr><td>3.7</td><td>10.8</td><td>20.1</td><td>val4</td></tr>"
            "</table><br>"

            "<b>Wichtige Regeln:</b>"
            "Das Programm berechnet für jede Spalte einen Mittelwert entlang der Spalte. Somit können auch mehrere Mittelwerte"
            " gleichzeitig berechnet werden: Dafür müssen einfach mehrere Spalten vorhanden sein (siehe optinale Spalten)"
            "<ul style='margin-top: 4px; padding-left: 20px;'>"
            "  <li>Erste Spalte = <b>Muss vorhanden sein</b>, alle weiteren Spalten = <b>weitere Mittelwerte</b>.</li>"
            "  <li>Spaltennamen (im obersten Feld der Spalte) sind erlaubt, haben aber keine Bedeutung. </li>"
            "  <li>Falls Spaltennamen verwendet werden muss natürlich jede Spalte einen Namen besitzen. </li>"
            "  <li>Keine leeren Zellen mitten in den Datenreihen.</li>"
            "  <li>Abgesehen von den Spalten und ihren Namen muss die Datei leer sein</li>"
            "</ul>")
        else:
            return(
            "To ensure your data is read correctly, please follow this (exemplary) format:<br><br>"
            "<table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse; text-align: center;'>"
            "  <tr style='background-color: #e0e0e0; font-weight: bold;'>"
            "    <td>Mean Column 1</td><td>Column 2 (optional)</td><td>Column 3 (optional)</td><td>Column n</td>"
            "  </tr>"
            "  <tr><td>3.5</td><td>10.2</td><td>20.5</td><td>val1</td></tr>"
            "  <tr><td>3.6</td><td>11.4</td><td>20.1</td><td>val2</td></tr>"
            "  <tr><td>3.2</td><td>10.5</td><td>20.8</td><td>val3</td></tr>"
            "  <tr><td>3.7</td><td>10.8</td><td>20.1</td><td>val4</td></tr>"
            "</table><br>"
            "<b>Important Rules:</b>"
            "The program calculates a mean value down each column. This allows multiple mean values "
            "to be computed simultaneously: simply include multiple columns in the file (see optional columns)."
            "<ul style='margin-top: 4px; padding-left: 20px;'>"
            "  <li>First column = <b>Mandatory</b>, all subsequent columns = <b>additional datasets</b>.</li>"
            "  <li>Column names (in the top row) are optional and ignored for calculations.</li>"
            "  <li>If column headers are used, every column must have one.</li>"
            "  <li>No empty cells within the data series.</li>"
            "  <li>Apart from the data columns and their headers, the sheet must be empty.</li>")
        
    def get_hilfetext(self):
        if self.aktuelle_sprache == "de":
            return(
                "<b>Bedienungsanleitung: Mittelwert-Rechner</b><br><br>"
                    "<b>1. Dateneingabe:</b><br>"
                "• <b>Manuell:</b> Du kannst Werte direkt in die Zellen der Tabelle eintippen oder ändern. "
                "Mittelwerte passen sich sofort live an.<br>"
                "• <b>Excel-Import:</b> Über den Button <code>Excel für Mittelwerte laden</code> kannst du "
                "ganze Messreihen importieren. Jede Spalte wird als eigene Messreihe verarbeitet.<br><br>"
                "<b>2. Berechnete Größen (unterste Zeile):</b><br>"
                "• <b>Mittelwert (x̄):</b> Arithmetisches Mittel der jeweiligen Spalte.<br>"
                "• <b>Fehler des Mittelwerts (s<sub>x̄</sub>):</b> Standardabweichung der Stichprobe "
                "geteilt durch die Quadratwurzel der Stichprobengröße.<br><br>"
                "<b>3. Nützliche Tipps:</b><br>"
                "• Dezimalzahlen können sowohl mit Komma (<code>,</code>) als auch mit Punkt (<code>.</code>) eingegeben werden.<br>"
                "• Die blau hervorgehobene Ergebniszeile ist geschützt und passt sich bei jeder Zelländerung automatisch an.")

        else: 
            return(
                "<b>User Guide: Mean Calculator</b><br><br>"
                "<b>1. Data Input:</b><br>"
                "• <b>Manual:</b> You can enter or edit values directly within the table cells. "
                "The mean values will update immediately in real time.<br>"
                "• <b>Excel Import:</b> Use the <code>Open Excel</code> button to import "
                "entire measurement series. Each column is processed as a separate dataset.<br><br>"
                "<b>2. Calculated Quantities (bottom row):</b><br>"
                "• <b>Mean value (x̄):</b> Arithmetic mean of the respective column.<br>"
                "• <b>Standard Error of the Mean (s<sub>x̄</sub>):</b> Sample standard deviation "
                "divided by the square root of the sample size.<br><br>"
                "<b>3. Useful Tips:</b><br>"
                "• Decimal numbers can be entered using either a comma (<code>,</code>) or a period (<code>.</code>).<br>"
                "• The blue highlighted result row is write-protected and updates automatically with every change to the cells.")

    def open_excel(self):
         # 1. Info-Box mit Beispiel-Tabelle anzeigen
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Hinweis zum Excel-Format für Mittelwerte")
        msgBox.setText("<b>Optimale Struktur für den Datei-Import</b>" if self.aktuelle_sprache == "de" else "<b>Optimized layout for data import</b>")
        
        # HTML-Tabelle mit Anschauungsbeispiel bauen
        msgBox.setInformativeText(self.get_infotext_html())
        msgBox.exec()


        dateiname, _ = QFileDialog.getOpenFileName(
        self, "Excel-Datei auswählen", "", "Excel-Dateien (*.xlsx *.xls)") # *xlsx etc. ist ein Filter, nur diese Dateien können ausgewählt werden! 
        if dateiname: # if dateiname is not none
            print(dateiname)

            try: 
                self.raw_df = pd.read_excel(dateiname, header = None)
                self.raw_df = self.raw_df.dropna(how = "all").reset_index(drop = True)
                self.raw_df = self.raw_df.dropna(how='all', axis=1)

                if self.raw_df.empty:
                    QMessageBox.warning(self, "Datei leer", "diese Datei enthält keine Daten!")
                    return 
                
                #Erste Zeile reine Zahlen?
                erste_zeile = self.raw_df.iloc[0]
                numerisch = True
                for val in erste_zeile:
                    try: 
                        float(val)
                    except (ValueError, TypeError):
                        numerisch = False
                        break
                # Spaltenname und Daten trennen
                if numerisch:
                    Messreihe_lang = "Messreihe" if self.aktuelle_sprache == "de" else "Series"
                    spalten_namen = [f"{Messreihe_lang} {i+1}" for i in range(self.raw_df.shape[1])]
                    datafile = self.raw_df.copy()
                else:
                    spalten_namen = [str(val) for val in self.raw_df.iloc[0, :]]
                    datafile = self.raw_df.iloc[1:].reset_index(drop=True)

                # Prüfen, ob nach dem Header irgendwo leere Felder (NaN) in den Daten sind
                if datafile.isnull().values.any():
                    QMessageBox.warning(
                        self, 
                        "Fehlende Datenwerte", 
                        "In deiner Excel-Datei fehlen einzelne Zahlenwerte (leere Zellen).\n\n"
                        "Bitte überprüfe deine Datei und stelle sicher, dass alle Messreihen vollständig ausgefüllt sind."
                    )
                    return

                # Alle Spalten abspeichern
                # Alle Spalten abspeichern & Tabelle neu aufbauen
                self.mittelwertspalten_dict = {}
                for idx, spalten_name in enumerate(spalten_namen):
                    spalten_name = str(spalten_name)
                    self.mittelwertspalten_dict[spalten_name] = datafile.iloc[:, idx].dropna().to_numpy(dtype=float)

                # --- NEU: Tabelle komplett für die neue Excel-Datei neu aufbauen ---
                self.tabelle.blockSignals(True)  # Signale blockieren während des Umbaus
                
                max_zeilen = max(len(v) for v in self.mittelwertspalten_dict.values())
                n_spalten = len(spalten_namen)

                self.tabelle.setRowCount(max_zeilen + 1)  # Messwerte + 1 Ergebniszeile
                self.tabelle.setColumnCount(n_spalten)
                self.tabelle.setHorizontalHeaderLabels(spalten_namen)

                # Messwerte aus der Excel-Datei in die Tabellenzellen schreiben
                for col_idx, s_name in enumerate(spalten_namen):
                    werte = self.mittelwertspalten_dict[s_name]
                    for row_idx in range(max_zeilen):
                        if row_idx < len(werte):
                            item_str = f"{werte[row_idx]:.4g}"
                        else:
                            item_str = ""  # Leere Zelle falls Spalten unterschiedlich lang sind
                        
                        self.tabelle.setItem(row_idx, col_idx, QTableWidgetItem(item_str))

                self.tabelle.blockSignals(False)

                # Erst jetzt die Mittelwerte berechnen und Ergebniszeile rendern!
                self.aktualisiere_tabelle()

            except Exception as e:
                QMessageBox.critical(
                    self, "Allgemeiner Fehler", f"Details zum Fehler:\n{type(e).__name__}: {str(e)}"
                )
        
    def calculate_mean(self):
        ergebnisse = {}
        if not hasattr(self, "mittelwertspalten_dict"):
            return ergebnisse

        for spalten_name, werte in self.mittelwertspalten_dict.items():
            if len(werte) == 0:
                continue
            
            mittelwert = np.mean(werte)
            
            # Fehler des Mittelwerts: Standardabweichung / sqrt(N)
            if len(werte) > 1:
                std_abw = np.std(werte, ddof=1)  # ddof=1 für korrigierte Stichproben-StdAbw
                sem = std_abw / np.sqrt(len(werte)) # Standard Error of Mean
            else:
                sem = 0.0

            ergebnisse[spalten_name] = {
                "mean": mittelwert,
                "sem": sem,
                "n": len(werte)
            }
            
        return ergebnisse

    def aktualisiere_tabelle(self):
        if not hasattr(self, "mittelwertspalten_dict") or not self.mittelwertspalten_dict:
            return

        # Signal kurz stummschalten, damit das Eintragen der Ergebnisse keine Dauerschleife auslöst
        self.tabelle.blockSignals(True)

        ergebnisse = self.calculate_mean()
        spalten_namen = list(self.mittelwertspalten_dict.keys())
        max_zeilen = self.tabelle.rowCount() - 1

        for col_idx, s_name in enumerate(spalten_namen):
            res = ergebnisse.get(s_name, None)
            
            if res and res['n'] > 0:
                erg_str = f"x̄ = {res['mean']:.4g} ± {res['sem']:.3g}"
            else:
                erg_str = "x̄ = - ± -"

            erg_item = QTableWidgetItem(erg_str)
            font = erg_item.font()
            font.setBold(True)
            erg_item.setFont(font)
            erg_item.setBackground(QColor("#e6f2ff"))
            # WICHTIG: Die Ergebnis-Zelle ist schreibgeschützt!
            erg_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            
            self.tabelle.setItem(max_zeilen, col_idx, erg_item)

        # Spaltenbreite automatisch anpassen & Mindestbreite garantieren
        self.tabelle.resizeColumnsToContents()
        for col in range(self.tabelle.columnCount()):
            if self.tabelle.columnWidth(col) < 180:
                self.tabelle.setColumnWidth(col, 180)

        self.tabelle.blockSignals(False)

    def erstelle_leere_start_tabelle(self, spalten=6, zeilen=10):
        """Erstellt zu Beginn eine leere Tabelle mit Standard-Eingabefeldern."""
        self.tabelle.blockSignals(True)  # Signale stoppen, um Schleifen zu verhindern
        Messreihe_lang = "Messreihe" if self.aktuelle_sprache == "de" else "Series"
        spalten_namen = [f"{Messreihe_lang} {i+1}" for i in range(spalten)]
        self.mittelwertspalten_dict = {s_name: np.array([]) for s_name in spalten_namen}

        self.tabelle.setRowCount(zeilen + 1)  # +1 Zeile für das Ergebnis
        self.tabelle.setColumnCount(spalten)
        self.tabelle.setHorizontalHeaderLabels(spalten_namen)

        for col in range(spalten):
            for row in range(zeilen):
                self.tabelle.setItem(row, col, QTableWidgetItem(""))
            
            # Ergebniszeile unten vorbereiten
            erg_item = QTableWidgetItem("x̄ = - ± -")
            font = erg_item.font()
            font.setBold(True)
            erg_item.setFont(font)
            erg_item.setBackground(QColor("#e6f2ff"))
            erg_item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Ergebnis-Zelle schreibgeschützt!
            self.tabelle.setItem(zeilen, col, erg_item)

        self.tabelle.blockSignals(False)

    def manuelle_eingabe_geandert(self, row, col):
        """Liest die Werte aus der Tabelle ab und berechnet die Mittelwerte neu."""
        max_row = self.tabelle.rowCount() - 1
        if row == max_row:
            return  # Die Ergebniszeile selbst reagiert nicht auf Äquivalenzänderungen

        # Dictionaries aus den Tabellenzellen aktualisieren
        spalten_namen = list(self.mittelwertspalten_dict.keys())
        
        for col_idx, s_name in enumerate(spalten_namen):
            neue_werte = []
            for r in range(max_row):
                item = self.tabelle.item(r, col_idx)
                if item and item.text().strip():
                    try:
                        # Versuche den Zellentext in eine Fließkommazahl umzuwandeln
                        val = float(item.text().strip().replace(",", "."))
                        neue_werte.append(val)
                    except ValueError:
                        pass  # Ignoriere Text/Ungültiges
            
            self.mittelwertspalten_dict[s_name] = np.array(neue_werte)

        # Mittelwerte neu berechnen & Ergebniszeile refreshen
        self.aktualisiere_tabelle()

    def save_excel(self):
        # 1. Ergebnisse abrufen
        ergebnisse = self.calculate_mean() 
        Warning_text = ("Es sind keine Messdaten zum Exportieren vorhanden" if self.aktuelle_sprache == "de" else "No data for export available")
        if not ergebnisse:
            QMessageBox.warning(self, "Keine Daten", Warning_text)
            return

        # 2. Daten für den DataFrame vorbereiten (auf 4 Dezimalstellen gerundet)
        export_daten = []
        for spalten_name, res in ergebnisse.items():
            if res["n"] > 0:
                export_daten.append({
                    "Messreihe": spalten_name,
                    "Anzahl N": res["n"],
                    "Mittelwert (x̄)": round(float(res["mean"]), 4),
                    "Fehler des Mittelwerts (s_x̄)": round(float(res["sem"]), 4)
                })

        if not export_daten:
            QMessageBox.warning(self, "Keine Daten", "Es wurden keine gültigen Zahlenwerte gefunden.")
            return

        df = pd.DataFrame(export_daten)

        # 3. Datei-Speicherdialog öffnen
        dateiname, _ = QFileDialog.getSaveFileName(
            self,
            "Mittelwerte speichern",
            "mittelwerte.xlsx",
            "Excel-Arbeitsmappe (*.xlsx);;CSV-Datei (*.csv)"
        )

        # 4. Datei auf die Festplatte schreiben
        if dateiname:
            try:
                if dateiname.endswith(".csv"):
                    df.to_csv(dateiname, index=False, sep=";", float_format="%.4f")
                else:
                    df.to_excel(dateiname, index=False, float_format="%.4f")

                QMessageBox.information(
                    self,
                    "Erfolg",
                    f"Die Mittelwerte wurden erfolgreich gespeichert unter:\n{dateiname}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Fehler beim Speichern",
                    f"Die Datei konnte nicht gespeichert werden (ist sie eventuell noch in Excel geöffnet?):\n\n{str(e)}"
                )

    def retranslate_ui(self):
        t = TRANSLATIONS.get(self.aktuelle_sprache, TRANSLATIONS["de"])

        self.setWindowTitle(t["Mittelwert_title"])
        self.lbl_mean_calculator.setText(f"<b>{t['Mittelwert_header']}</b>")

        self.btn_excel_laden.setText(t["Mittelwert_open"])
        self.btn_excel_save.setText(t["Mittelwert_save"])
        self.lbl_dataAndresult.setText(f"<b>{t['mean_preview_table']}</b>")
        


# --- Startpunkt der Anwendung ---x
if __name__ == "__main__": # Alles unter der if Abfrage wird nur dann ausgefsührt, wenn ich die Datei direkt starte
    app = QApplication(sys.argv)

    # Namen der Anwendung setzen
    app.setApplicationName("Protokollix")
    app.setApplicationDisplayName("Protokollix")
    #Icon der Anwednung setzen

    # Absoluten Pfad zur Bilddatei relativ zum Skript ermitteln
    basis_ordner = os.path.dirname(os.path.abspath(__file__))
    icon_pfad = os.path.join(basis_ordner, "icon.png")

    # Nur setzen, wenn die Datei wirklich existiert:
    if os.path.exists(icon_pfad):
        app_icon = QIcon(icon_pfad)
        app.setWindowIcon(app_icon)

    fenster = MeinPlotterApp()
    if os.path.exists(icon_pfad):
        fenster.setWindowIcon(app_icon)
    fenster.show()
    QApplication.instance().styleHints().setColorScheme(Qt.ColorScheme.Light)
    sys.exit(app.exec()) # App exec ist eine Endlosschleife, wenn ich das Programm schließe gibt es 0 zurück, wenn es abstürzt 1 