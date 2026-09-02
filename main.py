# ==============================================================================
# DOC ATHLETIC EVOLUTION - SKISPRINGEN (Version 34.0)
# Architektur: Autarke Edition (Erweiterter 8-Punkte-Variantenkatalog, Altersgradierte Protokolle)
# ==============================================================================
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Doc Athletic Evolution - Skispringen", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #000000; color: #ffffff; }
h1, h2, h3, h4, h5, h6, p, label { color: #ffffff !important; }
button[title="View fullscreen"] { display: none !important; }
.stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
    background-color: #ffffff !important;
    color: #000000 !important;
}
.stButton>button {
    background-color: #1f2833; color: #66fcf1;
    border: 2px solid #45a29e; border-radius: 8px;
    width: 100%; font-weight: bold;
}
.stDownloadButton > button {
    background-color: #1f2833 !important; color: #ffffff !important;
    font-weight: 900 !important; font-size: 15px !important;
    border: 3px solid #66fcf1 !important; border-radius: 8px !important;
    width: 100% !important; padding: 12px !important;
}
.steuermatrix {
    background-color: #111111; border: 2px solid #333333;
    border-radius: 5px; padding: 15px; margin-bottom: 20px;
}
.badge-skispringen { 
    background-color: #3498db; color: #ffffff; padding: 8px 15px; 
    border-radius: 6px; font-weight: bold; font-size: 16px; display: inline-block; margin-top: 10px; border: 1px solid #ffffff;
}
.druck-tabelle {
    width: 100%; border-collapse: collapse; margin-top: 10px;
    font-family: Arial, sans-serif; font-size: 14px; color: #ffffff;
}
.druck-tabelle th {
    background-color: #1f2833; color: #66fcf1 !important;
    border: 1px solid #45a29e; padding: 10px; text-align: left;
}
.druck-tabelle td { border: 1px solid #333333; padding: 8px; }
.druck-tabelle tr:nth-child(even) { background-color: #0b0c10; }
.druck-tabelle tr:nth-child(odd) { background-color: #111111; }
/* DRUCKOPTIMIERUNG */
@media print {
    @page { size: landscape; margin: 10mm; }
    body { background-color: #ffffff !important; color: #000000 !important; }
    .stApp, .steuermatrix, .footer-box { background-color: #ffffff !important; color: #000000 !important; border: none !important; }
    h1, h2, h3, h4, h5, h6, p, label, span { color: #000000 !important; }
    .stButton, .stDownloadButton, [data-testid="stSidebar"], .stRadio { display: none !important; }
    .druck-tabelle { width: 100% !important; border-collapse: collapse !important; }
    .druck-tabelle th { background-color: #e0e0e0 !important; color: #000000 !important; border: 1px solid #000000 !important; }
    .druck-tabelle td { border: 1px solid #000000 !important; color: #000000 !important; background-image: none !important; background-color: #ffffff !important; }
}
</style>
""", unsafe_allow_html=True)

def lade_bild(dateinamen_liste, use_col=False):
    for name in dateinamen_liste:
        if os.path.exists(name):
            if use_col:
                st.image(name, width="stretch")
            return True
    return False

# AUTHENTIFIZIERUNG
GAST_CODE = "gast2026"
TRAINER_CODE = "DocAthletic#2026!"
if 'auth_modus' not in st.session_state:
    st.session_state.auth_modus = None

if st.session_state.auth_modus is None:
    col_11, col_12, col_13 = st.columns([1, 2, 1])
    with col_12:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<p style='text-align: center; color: #c5c6c7; margin-top: 20px;'>Bitte Zugriffscode eingeben</p>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
        with col_p2:
            eingabe_code = st.text_input("Zugriffscode", type="password")
            if st.button("ZUGRIFF BESTÄTIGEN"):
                if eingabe_code == TRAINER_CODE:
                    st.session_state.auth_modus = "trainer"
                    st.rerun()
                elif eingabe_code == GAST_CODE:
                    st.session_state.auth_modus = "gast"
                    st.rerun()
                else:
                    st.error("Ungültiger Code. Bitte prüfen.")
    st.stop()

if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

# KADER DATENBANK SKISPRINGEN
if 'kader_db_skispringen' not in st.session_state:
    st.session_state.kader_db_skispringen = {
        "DSV Kader A (Senior m)": {"alter": 24, "groesse": 1.76, "gewicht": 62.0, "f_max": 130.0, "profil": "Senior m", "sbe": "SR 0"},
        "DSV Kader B (U20 w)": {"alter": 19, "groesse": 1.65, "gewicht": 54.0, "f_max": 105.0, "profil": "U20 w", "sbe": "SR 1"},
        "NLZ Nachwuchs 1 (U15 m)": {"alter": 14, "groesse": 1.60, "gewicht": 50.0, "f_max": 75.0, "profil": "U15 m", "sbe": "SR 2"}
    }

def navigiere(ziel):
    st.session_state.navigations_status = ziel

# ZENTRALE PARAMETER-MATRIZE SKISPRINGEN (Altersgruppierung für Strecken & Protokolle)
skispringen_parameter = {
    "U11 w": {"hw_basis": 0.0, "hw_winkel": "0°", "max_zl": 0.0, "abc_last": 0.0, "gruppe": "U11_U13", "drop_hoehe": "20-30 cm", "indiv": False},
    "U11 m": {"hw_basis": 0.0, "hw_winkel": "0°", "max_zl": 0.0, "abc_last": 0.0, "gruppe": "U11_U13", "drop_hoehe": "20-30 cm", "indiv": False},
    "U13 w": {"hw_basis": 10.0, "hw_winkel": "6°", "max_zl": 10.0, "abc_last": 2.0, "gruppe": "U11_U13", "drop_hoehe": "20-30 cm", "indiv": False},
    "U13 m": {"hw_basis": 10.0, "hw_winkel": "6°", "max_zl": 15.0, "abc_last": 2.0, "gruppe": "U11_U13", "drop_hoehe": "20-30 cm", "indiv": False},
    "U15 w": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 20.0, "abc_last": 3.0, "gruppe": "U15_U17", "drop_hoehe": "35-45 cm", "indiv": False},
    "U15 m": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 30.0, "abc_last": 3.0, "gruppe": "U15_U17", "drop_hoehe": "35-45 cm", "indiv": False},
    "U17 w": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 30.0, "abc_last": 3.0, "gruppe": "U15_U17", "drop_hoehe": "35-45 cm", "indiv": False},
    "U17 m": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 45.0, "abc_last": 3.0, "gruppe": "U15_U17", "drop_hoehe": "35-45 cm", "indiv": False},
    "U20 w": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 40.0, "abc_last": 3.0, "gruppe": "U20_Elite", "drop_hoehe": "50-70 cm", "indiv": False},
    "U20 m": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 55.0, "abc_last": 3.0, "gruppe": "U20_Elite", "drop_hoehe": "50-70 cm", "indiv": False},
    "U23 w": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 45.0, "abc_last": 3.0, "gruppe": "U20_Elite", "drop_hoehe": "50-70 cm", "indiv": True},
    "U23 m": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 60.0, "abc_last": 3.0, "gruppe": "U20_Elite", "drop_hoehe": "50-70 cm", "indiv": True},
    "Senior w": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 50.0, "abc_last": 3.0, "gruppe": "U20_Elite", "drop_hoehe": "50-70 cm", "indiv": True},
    "Senior m": {"hw_basis": 35.0, "hw_winkel": "11°", "max_zl": 70.0, "abc_last": 3.0, "gruppe": "U20_Elite", "drop_hoehe": "50-70 cm", "indiv": True}
}

if st.session_state.auth_modus == "gast":
    st.sidebar.warning("GAST-MODUS (Nur Leserechte)")

# NAVIGATION: START
if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important; margin-top: 30px;'>DOC ATHLETIC EVOLUTION - SKISPRINGEN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #c5c6c7; font-size: 16px;'>Autarke Architektur Skispringen (Version 34.0 - Positionssprints & Altersgrading)</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Operativ',))

# NAVIGATION: OPERATIV
elif st.session_state.navigations_status == 'Operativ':
    col_top1, col_top2 = st.columns([1, 4])
    with col_top1:
        st.button("<< START", on_click=navigiere, args=('Start',))
    with col_top2:
        st.markdown("## Operative Trainingssteuerung - SKISPRINGEN (v34.0)")
    
    st.markdown("<div class='steuermatrix'>", unsafe_allow_html=True)
    st.markdown("<span class='badge-skispringen'>Modul: Skispringen (Positionsspezifische Ansteuerung & Kader-Logistik)</span><br><br>", unsafe_allow_html=True)
    
    aktive_athleten_db = st.session_state.kader_db_skispringen
    profil_schluessel = list(skispringen_parameter.keys())
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        modus = st.selectbox("Steuerungs-Ebene", ["Einzelathlet", "Kader / Profil"])
        if modus == "Einzelathlet":
            ziel = st.selectbox("Ziel (Name)", list(aktive_athleten_db.keys()))
            aktuelle_daten = aktive_athleten_db[ziel]
            profil_soll = aktuelle_daten["profil"]
        else:
            ziel = st.selectbox("Ziel (Profil)", profil_schluessel)
            profil_soll = ziel
            aktuelle_daten = {"alter": 16, "groesse": 1.70, "gewicht": 55.0, "f_max": 80.0, "sbe": "SR 2"}
    with c2:
        alter = st.number_input("Alter (Jahre)", min_value=8, max_value=40, value=int(aktuelle_daten["alter"]), disabled=(st.session_state.auth_modus == "gast"))
        groesse = st.number_input("Körpergröße (m)", min_value=1.20, max_value=2.15, value=float(aktuelle_daten["groesse"]), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
    with c3:
        gewicht_akt = st.number_input("Körpergewicht (kg)", min_value=30.0, max_value=100.0, value=float(aktuelle_daten.get("gewicht", 50.0)), step=0.5, disabled=(st.session_state.auth_modus == "gast"))
        f_max_akt = st.number_input("1RM Tief-Kniebeuge (kg)", min_value=20.0, max_value=200.0, value=float(aktuelle_daten.get("f_max", 50.0)), step=1.0, disabled=(st.session_state.auth_modus == "gast"))
    with c4:
        te_wahl = st.selectbox("Trainingseinheit (TE)", [f"TE {i}" for i in range(1, 15)])
        sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"], disabled=(st.session_state.auth_modus == "gast"))
    
    st.markdown("---")
    st.markdown("#### Spezifische Trainingsmittel & Methodik")
    haupt_kategorie = st.selectbox("Haupt-Trainingsblock auswählen:", [
        "1. Kommandosprints / Positionssprints (8-Punkte-Katalog)",
        "2. Maximale Beschleunigung",
        "3. Spezielles Sprung-ABC (Explosivkraft / RFD)",
        "4. Sprintschnelligkeit",
        "5. Schnelligkeitsausdauer (Tempoläufer)",
        "6. Schanzentisch-Simulation (Hardware-Kinetik)",
        "7. Exzentrische Landedämpfung & Telemark"
    ])

    # Wenn Kommandosprints ausgewählt sind, Auswahl der Startvarianten ermöglichen
    start_variante = "Standard"
    reaktiv_zusatz = False
    if "1. Kommandosprints" in haupt_kategorie:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 8-Punkte-Variantenkatalog (Startpositionen)")
        start_variante = st.selectbox("Wähle Startvariante (3-4 im Wechsel pro TE):", [
            "1. Liegestütz in Bauchlage (flach)",
            "2. Liegestütz mit gestreckten Armen (obere Position)",
            "3. Hocke mit Blick gegen die Laufrichtung",
            "4. Hocke mit Blick in Laufrichtung",
            "5. Rückenlage - linkes Bein 90° nach oben gestreckt",
            "6. Rückenlage - rechtes Bein 90° nach oben gestreckt",
            "7. Ausfallschritt - linkes Bein vorn",
            "8. Ausfallschritt - rechtes Bein vorn"
        ])
        vorgaben_check = skispringen_parameter.get(profil_soll, {"gruppe": "U11_U13"})
        if vorgaben_check["gruppe"] == "U20_Elite":
            reaktiv_zusatz = st.checkbox("Sensorische Überraschungskommandos & stationäre Reaktivkomplexe aktivierbar (U20+ Elite)")

    st.markdown("</div>", unsafe_allow_html=True)

    # DIAGNOSTIK & TELEMETRIE (SKISPRINGEN)
    st.subheader("Telemetrie-Schnittstelle & Biologische Sperren")
    diag_col1, diag_col2, diag_col3 = st.columns(3)
    
    vorgaben = skispringen_parameter.get(profil_soll, {"hw_basis": 0.0, "hw_winkel": "0°", "max_zl": 0.0, "abc_last": 0.0, "gruppe": "U11_U13", "drop_hoehe": "30 cm", "indiv": False})

    with diag_col1:
        st.markdown("#### Kinetik (Maschine)")
        hubgeschwindigkeit = st.number_input("Hubgeschwindigkeit (m/s)", min_value=0.0, max_value=3.0, value=1.35, step=0.01)
        hubhoehe = st.number_input("Hubhöhe (m)", min_value=0.0, max_value=1.5, value=0.95, step=0.01)
    
    with diag_col2:
        st.markdown("#### Biomechanik")
        asymmetrie = st.number_input("L/R Symmetrie-Abweichung (%)", min_value=0.0, max_value=15.0, value=0.5, step=0.1)
        if asymmetrie > 2.0:
            st.error("⚠️ ASYMMETRIE > 2.0%! Zusatzlast systemseitig auf 0,0 kg blockiert.")
            zusatzlast_freigabe = 0.0
            abc_zusatzlast = 0.0
        else:
            st.success("✅ Funktionelle Symmetrie im Normbereich.")
            zusatzlast_freigabe = vorgaben["max_zl"]
            abc_zusatzlast = vorgaben["abc_last"]

    with diag_col3:
        st.markdown("#### Morphologie")
        f_rel = f_max_akt / gewicht_akt if gewicht_akt > 0 else 0
        st.write(f"Relative Druckkraft ($F_{{rel}}$): **{f_rel:.2f}**")
        if gewicht_akt < aktuelle_daten.get("gewicht", 50.0) and f_max_akt < aktuelle_daten.get("f_max", 50.0):
            st.error("⚠️ KATABOLISMUS-ALARM! Laktazide Volumina gesperrt. ZNS-Schutz aktiv.")
        else:
            st.info("Morphologie stabil.")

    st.markdown("---")
    st.subheader(f"Operatives Trainingsprotokoll: {ziel} ({te_wahl}) - {haupt_kategorie}")
    
    # Altersgradierte Parameter-Zuordnung
    gruppe = vorgaben["gruppe"]
    if gruppe == "U11_U13":
        dist_kommando = "10 bis 15 m"
        reps_kommando = "3 bis 5 Durchgänge"
        dist_beschleunigung = "20 bis 25 m"
        reps_beschleunigung = "Mindestens 6 Durchgänge"
        dist_sprint = "30 bis 40 m"
        reps_sprint = "4 bis 6 Durchgänge"
        tempo_info = "Keine extensiven Tempoläufe (Fokus ZNS & Fast-Twitch)"
    elif gruppe == "U15_U17":
        dist_kommando = "15 bis 20 m"
        reps_kommando = "4 bis 5 Durchgänge"
        dist_beschleunigung = "25 bis 30 m"
        reps_beschleunigung = "Mindestens 6 Durchgänge"
        dist_sprint = "35 bis 45 m"
        reps_sprint = "4 bis 5 Durchgänge"
        tempo_info = "Technikläufe (max. 90% Int.) / Tempoläufe max. 80% Int., 60-80m (4-5 Dg.)"
    else: # U20_Elite
        dist_kommando = "20 m"
        reps_kommando = "3 bis 5 Durchgänge"
        dist_beschleunigung = "30 bis 40 m"
        reps_beschleunigung = "6 bis 8 Durchgänge"
        dist_sprint = "50 bis 60 m"
        reps_sprint = "4 bis 6 Durchgänge"
        tempo_info = "Tempoläufe (bis 80m: 6-8 Dg. | bis 150m: 4-6 Dg. bei max. 80% Int.)"

    protokoll = []
    
    if "1. Kommandosprints" in haupt_kategorie:
        extra_text = " + Reaktivkomplexe (Fußgelenksprünge/Burpees vor Start)" if reaktiv_zusatz else ""
        protokoll = [
            {"Block": "Ausgangsposition", "Trainingsmittel": start_variante, "Vorgabe/Gerät": f"Zusatzlast: {abc_zusatzlast} kg{extra_text}", "Tonnage / Serien": f"Distanz: {dist_kommando} | {reps_kommando} | Explosiver Antritt auf akustisches Kommando"}
        ]
    elif "2. Maximale Beschleunigung" in haupt_kategorie:
        protokoll = [
            {"Block": "Phase A", "Trainingsmittel": "Gebückter Hochstart (Beschleunigung)", "Vorgabe/Gerät": f"Zusatzlast: {abc_zusatzlast} kg", "Tonnage / Serien": f"Distanz: {dist_beschleunigung} | {reps_beschleunigung} | Pause: 120s-180s | Maximaler horizontaler Impuls"}
        ]
    elif "3. Spezielles Sprung-ABC" in haupt_kategorie:
        protokoll = [
            {"Block": "Phase A", "Trainingsmittel": "Wechselsprünge & Hopserlauf hoch", "Vorgabe/Gerät": f"Zusatzlast: {abc_zusatzlast} kg", "Tonnage / Serien": "3-4 Serien | Minimale Bodenkontaktzeit | Vertikaler Impuls"},
            {"Block": "Phase B", "Trainingsmittel": "Seitliche Nachstellschritte & Überkreuzlauf", "Vorgabe/Gerät": "Ohne Zusatzlast", "Tonnage / Serien": "2 Serien je Richtung | Laterale Stabilität & Rumpfkontrolle"}
        ]
    elif "4. Sprintschnelligkeit" in haupt_kategorie:
        protokoll = [
            {"Block": "Phase A", "Trainingsmittel": "Maximale Sprintschnelligkeit", "Vorgabe/Gerät": "Ohne Zusatzlast (Frequenz-Optimum)", "Tonnage / Serien": f"Distanz: {dist_sprint} | {reps_sprint} | Pause: 180s | Absolute Höchstgeschwindigkeit"}
        ]
    elif "5. Schnelligkeitsausdauer" in haupt_kategorie:
        protokoll = [
            {"Block": "Phase A", "Trainingsmittel": "Tempoläufe & Techniksteigerungen", "Vorgabe/Gerät": "Kontrollierte Laktat-Steuerung", "Tonnage / Serien": f"{tempo_info} | SBE-Überwachung aktiv"}
        ]
    elif "6. Schanzentisch-Simulation" in haupt_kategorie:
        protokoll = [
            {"Block": "Phase A", "Trainingsmittel": f"Linearführung Vorneigung {vorgaben['hw_winkel']}", "Vorgabe/Gerät": f"Basisgewicht Schlitten: {vorgaben['hw_basis']} kg", "Tonnage / Serien": "2 Aufwärmsätze (50% Fmax)"},
            {"Block": "Phase B", "Trainingsmittel": "Schanzentisch-Absprung (Explosiv)", "Vorgabe/Gerät": f"Freigegebene Zusatzlast: {zusatzlast_freigabe} kg", "Tonnage / Serien": f"4 Sätze x 4 Wiederholungen | Pause: 120s | Ziel: Hubgeschw. > 1.3 m/s"},
            {"Block": "Phase C", "Trainingsmittel": "Slackline / Gleichgewichts-Integration", "Vorgabe/Gerät": "Freistehendes System", "Tonnage / Serien": "3 x 45 Sekunden | Fokus: Propriozeption"}
        ]
    else:
        protokoll = [
            {"Block": "Phase A", "Trainingsmittel": "Drop & Hold (Einbeinige Landung)", "Vorgabe/Gerät": f"Kastensprünge abwärts ({vorgaben['drop_hoehe']})", "Tonnage / Serien": "4 Sätze x 5 Wiederholungen pro Bein | Pause: 90s"},
            {"Block": "Phase B", "Trainingsmittel": "Telemark-Ausfallschritt unter Last", "Vorgabe/Gerät": "Kurzhantel / Weste (fixiert)", "Tonnage / Serien": "3 Sätze x 6 Wiederholungen | Strikte Valgus-Prävention"},
            {"Block": "Phase C", "Trainingsmittel": "Statische Rumpf- & Kettenstabilisierung", "Vorgabe/Gerät": "Eigengewicht", "Tonnage / Serien": "3 x 60 Sekunden Core-Integrität"}
        ]

    df_proto = pd.DataFrame(protokoll)
    html_tabelle = df_proto.to_html(index=False, classes="druck-tabelle")
    st.markdown(html_tabelle, unsafe_allow_html=True)

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("""
            <script>
            function druckeQuerformat() { window.print(); }
            </script>
            <button onclick="window.print();" style="background-color: #1f2833; color: #66fcf1; border: 3px solid #66fcf1; border-radius: 8px; width: 100%; font-weight: 900; font-size: 15px; padding: 12px; cursor: pointer; margin-top: 15px;">
            🖨️ PLAN DIREKT DRUCKEN (WLAN)
            </button>
        """, unsafe_allow_html=True)
    with col_w2:
        csv_data = df_proto.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="CSV PROTOKOLL HERUNTERLADEN",
            data=csv_data, file_name=f"Skispringen_Protokoll_{ziel.replace(' ', '_')}.csv", mime="text/csv"
        )