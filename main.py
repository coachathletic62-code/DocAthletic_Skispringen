# ==============================================================================
# DOC ATHLETIC EVOLUTION - SKISPRINGEN (Version 35.2)
# Architektur: Fehlerbereinigte HTML-Rendering (Dedent), Kader-Datenbank & Trainingsteuerung
# ==============================================================================
import streamlit as st
import pandas as pd
import os
import textwrap

st.set_page_config(page_title="Doc Athletic Evolution - Skispringen 35.2", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #000000; color: #ffffff; }
h1, h2, h3, h4, h5, h6, p, label, td, th { color: #ffffff !important; }
button[title="View fullscreen"] { display: none !important; }
.stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
    background-color: #ffffff !important; color: #000000 !important;
}
.stButton>button {
    background-color: #1f2833; color: #66fcf1; border: 2px solid #45a29e; border-radius: 8px; width: 100%; font-weight: bold;
}
.steuermatrix {
    background-color: #111111; border: 2px solid #333333; border-radius: 5px; padding: 15px; margin-bottom: 20px;
}
.badge-ski { background-color: #f39c12; color: #ffffff; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block; margin-top: 10px; }
.footer-box {
    text-align: center; border: 2px solid #66fcf1; border-radius: 10px; padding: 25px; margin-top: 40px; margin-bottom: 20px; background-color: #0b0c10;
}
@media print {
    @page { size: landscape; margin: 10mm; }
    body { background-color: #ffffff !important; color: #000000 !important; }
    .stApp, .steuermatrix, .footer-box { background-color: #ffffff !important; color: #000000 !important; border: none !important; }
    h1, h2, h3, h4, h5, h6, p, label, span { color: #000000 !important; }
    .stButton, [data-testid="stSidebar"], .stRadio { display: none !important; }
}
</style>
""", unsafe_allow_html=True)

def lade_bild(dateinamen_liste, use_col=False):
    for name in dateinamen_liste:
        if os.path.exists(name):
            if use_col:
                st.image(name, use_container_width=True)
            return True
    return False

if 'auth_modus' not in st.session_state:
    st.session_state.auth_modus = None

if st.session_state.auth_modus is None:
    col_11, col_12, col_13 = st.columns([1, 2, 1])
    with col_12:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<p style='text-align: center; color: #c5c6c7; margin-top: 20px;'>Bitte Zugriffscode eingeben (Skispringen v35.2)</p>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
        with col_p2:
            eingabe_code = st.text_input("Zugriffscode", type="password")
            if st.button("ZUGRIFF BESTÄTIGEN"):
                if eingabe_code == "DocAthletic#2026!":
                    st.session_state.auth_modus = "trainer"
                    st.rerun()
                elif eingabe_code == "gast2026":
                    st.session_state.auth_modus = "gast"
                    st.rerun()
                else:
                    st.error("Ungültiger Code.")
    st.stop()

# Kader-Datenbank Skispringen im Session State verankern
if 'skisprung_kader_db' not in st.session_state:
    st.session_state.skisprung_kader_db = {
        "Skisprung Kader A": {"alter": 18, "groesse": 1.78, "fasertyp": "Sprungkraft (Fast-Twitch IIx)", "reife": "Normalentwickler", "sbe": "SR 1"},
        "Skisprung Talent U16": {"alter": 15, "groesse": 1.70, "fasertyp": "Sprungkraft (Fast-Twitch IIx)", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 2"}
    }

st.markdown("<h1 style='text-align: center; color: #66fcf1 !important;'>DOC ATHLETIC EVOLUTION 35.2</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #c5c6c7;'>Modul: Skispringen (Trainingsteuerung, Kraft & Symmetrie)</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'><span class='badge-ski'>Trainingsteuerung Skispringen aktiv</span></div><br>", unsafe_allow_html=True)

st.markdown("<div class='steuermatrix'>", unsafe_allow_html=True)
st.markdown("### Biometrische Live-Steuerung & Athleten-Auswahl")

c1, c2, c3, c4 = st.columns(4)
with c1:
    modus = st.selectbox("Steuerungs-Ebene", ["Einzelathlet", "Kader / Profil"])
    aktive_kader = list(st.session_state.skisprung_kader_db.keys())
    if modus == "Einzelathlet":
        ziel = st.selectbox("Athlet wählen", aktive_kader)
        aktuelle_daten = st.session_state.skisprung_kader_db[ziel]
    else:
        ziel = st.selectbox("Kader wählen", aktive_kader)
        aktuelle_daten = st.session_state.skisprung_kader_db[ziel]

    geschlecht_wahl = st.selectbox("Geschlecht (Hormoneller Status)", ["Männlich", "Weiblich"])

with c2:
    alter = st.number_input("Alter (Jahre)", min_value=10, max_value=40, value=int(aktuelle_daten["alter"]), disabled=(st.session_state.auth_modus == "gast"))
    groesse = st.number_input("Körpergröße (m)", min_value=1.30, max_value=2.15, value=float(aktuelle_daten["groesse"]), step=0.01, disabled=(st.session_state.auth_modus == "gast"))

with c3:
    ft_liste = ["Sprungkraft (Fast-Twitch IIx)", "Schnelligkeit", "Hybrid"]
    reife_liste = ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]
    ft_idx = ft_liste.index(aktuelle_daten["fasertyp"]) if aktuelle_daten["fasertyp"] in ft_liste else 0
    r_idx = 0 if "Spät" in aktuelle_daten["reife"] else 2 if "Früh" in aktuelle_daten["reife"] else 1
    
    ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx, disabled=(st.session_state.auth_modus == "gast"))
    reife = st.selectbox("Entwicklungsstatus", reife_liste, index=r_idx, disabled=(st.session_state.auth_modus == "gast"))

with c4:
    te_wahl = st.selectbox("Trainingseinheit (Modul)", [
        "TE 1: Ansteuerung & Kommando-Sprints",
        "TE 2: Reaktive Kraftausdauer",
        "TE 3: 8-Punkte-Variantenkatalog",
        "TE 4: Biomechanische Ketten",
        "TE 5: Maximale Kraftübertragung",
        "TE 6: Geschwindigkeitssicherung",
        "TE 7: Sensorische Überraschungskommandos",
        "TE 8: Integration & Komplex",
        "TE 9: Seitensymmetrie & Unilaterale Explosivität",
        "TE 10: Kurzsprint-Volumen & Laktattoleranz",
        "TE 11: Neuromuskuläre Maximalrekrutierung",
        "TE 12: Spezifische Wettkampf-Synthese"
    ])
    sbe_ziel = st.text_input("SBE (Beanspruchung)", value=aktuelle_daten["sbe"], disabled=(st.session_state.auth_modus == "gast"))

# Neuer Athlet anlegen (Trainer-Modus)
if modus == "Einzelathlet" and st.session_state.auth_modus == "trainer":
    st.markdown("<br>", unsafe_allow_html=True)
    neuer_name = st.text_input("Neuen Athleten-Namen eingeben (zum Speichern):", value="")
    if st.button("Athleten-Profil in Datenbank speichern"):
        if neuer_name:
            st.session_state.skisprung_kader_db[neuer_name] = {
                "alter": int(alter), "groesse": float(groesse),
                "fasertyp": ft, "reife": reife, "sbe": sbe_ziel
            }
            st.success(f"Athlet {neuer_name} erfolgreich angelegt.")
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Hardware-Logik für Zusatzlasten (Sperre ab U16)
reife_intern = "Spätentwickler" if "Spät" in reife else "Normalentwickler"
if int(alter) <= 14 and reife_intern == "Spätentwickler":
    zl_speed_jumper = "GZ Entlastung"
else:
    zl_speed_jumper = "ZL individuell"

farben = {
    "Vorbereitung": "#FFF2CC",
    "Block 1: ABC": "#DDEBF7",
    "Block 1: Reiz": "#BDD7EE",
    "Block 2: Komplex": "#FCE4D6",
    "Block 2: Laktat": "#FCE4D6",
    "Block 3: Kraft": "#E2EFDA",
    "Block 3: Athletik": "#E2EFDA",
    "Cool-Down": "#F2F2F2"
}

einheiten_db = {
    "TE 1: Ansteuerung & Kommando-Sprints": [
            {"block": "Vorbereitung", "uebung": "Mobilisation Kapsel-Band-Apparat & Sprunggelenke", "s": "1", "w": "8 Min", "zl": "-", "int": "Leicht", "p": "-"},
            {"block": "Block 1: ABC", "uebung": "Fußgelenksprünge (Reaktiv-Fokus)", "s": "3", "w": "20m", "zl": "-", "int": "Frequenz", "p": "60s"},
            {"block": "Block 1: ABC", "uebung": "Kniehebelauf & Anfersen im Wechsel", "s": "3", "w": "20m", "zl": "-", "int": "Frequenz", "p": "60s"},
            {"block": "Block 1: ABC", "uebung": "Stechhub- & Nachstellschritte (Laterale Kette)", "s": "3", "w": "15m", "zl": "-", "int": "Dynamisch", "p": "60s"},
            {"block": "Block 1: Reiz", "uebung": "Kommando-Sprint (Start: Bauchlage)", "s": "2", "w": "20m", "zl": "-", "int": "Maximal", "p": "120s"},
            {"block": "Block 1: Reiz", "uebung": "Kommando-Sprint (Start: Rückenlage)", "s": "2", "w": "20m", "zl": "-", "int": "Maximal", "p": "120s"},
            {"block": "Block 1: Reiz", "uebung": "Kommando-Sprint (Start: Liegestütz)", "s": "2", "w": "20m", "zl": "-", "int": "Maximal", "p": "120s"},
            {"block": "Block 1: Reiz", "uebung": "Kommando-Sprint (Start: Stand / Drop)", "s": "2", "w": "20m", "zl": "-", "int": "Maximal", "p": "120s"},
            {"block": "Block 2: Komplex", "uebung": "Squat-Stoß-Jumps (Explosivkraft IIx)", "s": "4", "w": "6 Wdh.", "zl": "Power Bar", "int": "Maximal", "p": "90s"},
            {"block": "Block 2: Komplex", "uebung": "Speed Jumper / Squat Master (RFD-Fokus)", "s": "3", "w": "8 Wdh.", "zl": "GZ-Entlastung", "int": "Explosiv", "p": "90s"},
            {"block": "Block 3: Kraft", "uebung": "Leg Speed Curler (Ischiocrurale Sicherung)", "s": "3", "w": "10 Wdh.", "zl": "Körpergewicht", "int": "Widerstand", "p": "60s"},
            {"block": "Block 3: Kraft", "uebung": "T-Bar Rumpf-Rotationsstabilität", "s": "3", "w": "10 Wdh.", "zl": "15 kg", "int": "Submaximal", "p": "60s"},
            {"block": "Cool-Down", "uebung": "Auslaufen (Shuttle niedrigintensiv)", "s": "1", "w": "400m", "zl": "-", "int": "Sehr locker", "p": "-"},
            {"block": "Cool-Down", "uebung": "Regeneration & Tonus-Regulation (Faszien)", "s": "1", "w": "10 Min", "zl": "-", "int": "Passiv", "p": "-"}
        ],
    "TE 2: Reaktive Kraftausdauer": [
        {"block": "Vorbereitung", "uebung": "Spezifische Erwärmung (STL)", "s": "3", "w": "60m", "zl": "–", "int": "80%", "p": "Gehp.", "fokus": "Temperaturerhöhung"},
        {"block": "Block 1: Reiz", "uebung": "Drop Jumps (niedrige Box)", "s": "4", "w": "8 Wdh", "zl": "–", "int": "Max", "p": "120s", "fokus": "Minimale Bodenkontaktzeit"},
        {"block": "Block 2: Komplex", "uebung": "Reaktive Mehrfachsprünge", "s": "3", "w": "10 Knt.", "zl": "–", "int": "Reaktiv", "p": "90s", "fokus": "Dehnungs-Verkürzungs-Zyklus"},
        {"block": "Block 2: Komplex", "uebung": "Seilspringen (Double Unders)", "s": "4", "w": "30s", "zl": "–", "int": "Hoch", "p": "60s", "fokus": "Frequenzsicherung laktazid"},
        {"block": "Cool-Down", "uebung": "Passive Dehnung", "s": "1", "w": "10 Min", "zl": "–", "int": "Passiv", "p": "–", "fokus": "Detonisierung"}
    ],
    "TE 3: 8-Punkte-Variantenkatalog": [
        {"block": "Vorbereitung", "uebung": "Spezifisches Warm-Up", "s": "1", "w": "10 Min", "zl": "–", "int": "Leicht", "p": "–", "fokus": "Aufwärmung"},
        {"block": "Block 1: ABC", "uebung": "Vektor-Modifikation (Horizontale vs. Vertikale Kraftvektoren)", "s": "3", "w": "Variabel", "zl": "–", "int": "Hoch", "p": "90s", "fokus": "Vermeidung Adaptationsblockade"},
        {"block": "Block 1: Reiz", "uebung": "Reaktions-Dichte (Frequenz Richtungswechsel)", "s": "3", "w": "10s", "zl": "–", "int": "Maximal", "p": "90s", "fokus": "Neuromuskuläre Vielfalt"},
        {"block": "Block 2: Komplex", "uebung": "Speed Master & Bungee-Systeme (Elastische Last)", "s": "4", "w": "8 Wdh", "zl": "Variabel", "int": "Explosiv", "p": "120s", "fokus": "Elastische Zusatzlast"},
        {"block": "Block 3: Kraft", "uebung": "Untergrund-Varia / Visuelle & Akustische Restriktion", "s": "3", "w": "Variabel", "zl": "–", "int": "Konzentriert", "p": "90s", "fokus": "Reizverarbeitung"},
        {"block": "Cool-Down", "uebung": "Regeneration", "s": "1", "w": "300m", "zl": "–", "int": "Locker", "p": "–", "fokus": "Ausgleich"}
    ],
    "TE 4: Biomechanische Ketten": [
        {"block": "Vorbereitung", "uebung": "Mobilisation / Kinetische Kette", "s": "1", "w": "5 Min", "zl": "–", "int": "Leicht", "p": "–", "fokus": "Gelenkfunktion"},
        {"block": "Block 3: Kraft", "uebung": "Planks mit frontaler/lateraler Erschütterung", "s": "3", "w": "45s", "zl": "Körpergewicht", "int": "Stabil", "p": "60s", "fokus": "Core-Integrität & Rumpfstabilisation"},
        {"block": "Block 3: Kraft", "uebung": "3D-Zugübungen (Elastische Bänder)", "s": "3", "w": "12 Wdh", "zl": "Widerstandszug", "int": "Submaximal", "p": "60s", "fokus": "Ketten-Kraftübertragung"},
        {"block": "Block 3: Kraft", "uebung": "Einbeinige Kniebeugen (Sensorische Kontrolle)", "s": "3", "w": "6/Bein", "zl": "–", "int": "Kontrolliert", "p": "90s", "fokus": "Gelenk-Stabilität / Valgussicherung"},
        {"block": "Cool-Down", "uebung": "Detonisierung", "s": "1", "w": "5 Min", "zl": "–", "int": "Passiv", "p": "–", "fokus": "Muskelentspannung"}
    ],
    "TE 5: Maximale Kraftübertragung": [
        {"block": "Vorbereitung", "uebung": "Dynamische Rumpfaufrichtung", "s": "1", "w": "5 Min", "zl": "–", "int": "Leicht", "p": "–", "fokus": "Kinetische Kette"},
        {"block": "Block 2: Komplex", "uebung": "Squat Stoß Jumps", "s": "5", "w": "3 Wdh", "zl": "30% KG", "int": "Explosiv", "p": "180s", "fokus": "Rekrutierung IIx / RFD"},
        {"block": "Block 2: Komplex", "uebung": "Speed Jumper / One Leg Jumper", "s": "4", "w": "4/Bein", "zl": zl_speed_jumper, "int": "Maximal", "p": "150s", "fokus": "Unilaterale Kraftübertragung"},
        {"block": "Block 3: Kraft", "uebung": "Abbruch-Steuerung (Zeitmessung)", "s": "–", "w": "–", "zl": "–", "int": "–", "p": "–", "fokus": "Stopp bei V-Verlust > 10%"},
        {"block": "Cool-Down", "uebung": "Auslaufen", "s": "1", "w": "300m", "zl": "–", "int": "Locker", "p": "–", "fokus": "Laktatabbau"}
    ],
    "TE 6: Geschwindigkeitssicherung": [
        {"block": "Vorbereitung", "uebung": "Lauf-ABC spezifisch", "s": "3", "w": "20m", "zl": "–", "int": "Frequenz", "p": "Gehp.", "fokus": "Neuronale Feuerungsrate"},
        {"block": "Block 2: Komplex", "uebung": "Fliegende Sprints (20m Anlauf)", "s": "4", "w": "30m", "zl": "–", "int": "100%", "p": "180s", "fokus": "Erhalt Höchstgeschwindigkeit"},
        {"block": "Block 2: Komplex", "uebung": "Over-Speed Sprints (Elastische Zugunterstützung)", "s": "3", "w": "20m", "zl": "Zugunterstützung", "int": "Supra-Max", "p": "120s", "fokus": "Frequenzüberhöhung ohne Erschöpfung"},
        {"block": "Cool-Down", "uebung": "Aktive Regeneration", "s": "1", "w": "400m", "zl": "–", "int": "Sehr locker", "p": "–", "fokus": "Stoffwechselausgleich"}
    ],
    "TE 7: Sensorische Überraschungskommandos": [
        {"block": "Vorbereitung", "uebung": "Erwärmung & Gelenkschmierung", "s": "1", "w": "10 Min", "zl": "–", "int": "Leicht", "p": "–", "fokus": "Temperaturerhöhung"},
        {"block": "Block 1: Reiz", "uebung": "Zyklische Beschleunigung / Sprungbewegungen", "s": "4", "w": "15m", "zl": "–", "int": "Dynamisch", "p": "90s", "fokus": "Bewegungsbereitschaft"},
        {"block": "Block 2: Komplex", "uebung": "Unerwartetes Aktionskommando (Richtungswechsel/Stopp)", "s": "4", "w": "Aktion", "zl": "–", "int": "Maximal reaktiv", "p": "120s", "fokus": "Kognitive & neuromuskuläre Flexibilität"},
        {"block": "Block 3: Kraft", "uebung": "Erfassung Entscheidungszeit (MyFreelap Timing)", "s": "–", "w": "Messung", "zl": "–", "int": "Fokus", "p": "–", "fokus": "Reduzierung Latenzzeit"},
        {"block": "Cool-Down", "uebung": "Regeneration", "s": "1", "w": "300m", "zl": "–", "int": "Locker", "p": "–", "fokus": "ZNS Erholung"}
    ],
    "TE 8: Integration & Komplex": [
        {"block": "Vorbereitung", "uebung": "Mobilisation", "s": "1", "w": "5 Min", "zl": "–", "int": "Leicht", "p": "–", "fokus": "Vorbereitung Ketten"},
        {"block": "Block 1: ABC", "uebung": "Lauf-ABC Drill (Komplexer Ablauf)", "s": "3", "w": "20m", "zl": "–", "int": "Hoch", "p": "60s", "fokus": "Technik-Vorermüdung"},
        {"block": "Block 1: Reiz", "uebung": "Unmittelbarer Kommando-Sprint", "s": "3", "w": "15m", "zl": "–", "int": "Maximal", "p": "120s", "fokus": "ZNS Umschaltung"},
        {"block": "Block 2: Komplex", "uebung": "Sprung-Kombination (3x Reaktiv)", "s": "3", "w": "3 Knt.", "zl": "–", "int": "Explosiv", "p": "120s", "fokus": "Wettkampfspezifische Kopplung"},
        {"block": "Block 3: Kraft", "uebung": "Sensorischer Reiz zur Abschlussaktion (Landung)", "s": "3", "w": "Aktion", "zl": "–", "int": "Fokus", "p": "90s", "fokus": "Ganzheitliche Integration"},
        {"block": "Cool-Down", "uebung": "Aktive & Passive Regeneration", "s": "1", "w": "10 Min", "zl": "–", "int": "Regenerativ", "p": "–", "fokus": "Vollständige Erholung"}
    ],
    "TE 9: Seitensymmetrie & Unilaterale Explosivität": [
        {"block": "Vorbereitung", "uebung": "Dynamische Erwärmung", "s": "1", "w": "400m", "zl": "–", "int": "Locker", "p": "–", "fokus": "Gewebeelastizität"},
        {"block": "Block 1: ABC", "uebung": "Einbeinsprünge im 3er-Rhythmus", "s": "3", "w": "20m (L/R)", "zl": "–", "int": "Rhythmisch", "p": "60s", "fokus": "Reaktive Symmetrie"},
        {"block": "Block 2: Komplex", "uebung": "One Leg Jumper (Unilateral)", "s": "4", "w": "6/Bein", "zl": zl_speed_jumper, "int": "Maximal explosiv", "p": "120s", "fokus": "Ausgleich Kraftdefizite"},
        {"block": "Block 2: Komplex", "uebung": "Kurzsprints aus lateralem Start", "s": "4", "w": "15m", "zl": "–", "int": "Maximal", "p": "90s", "fokus": "Explosive Richtungsänderung"},
        {"block": "Block 3: Kraft", "uebung": "Ausfallschritt-Jumps", "s": "3", "w": "20m", "zl": "4-6 kg Power Bar", "int": "Dynamisch", "p": "60s", "fokus": "Beinachsenstabilität (Valgus)"},
        {"block": "Cool-Down", "uebung": "Shuttle-Auslaufen", "s": "1", "w": "300m", "zl": "–", "int": "Regenerativ", "p": "–", "fokus": "Laktatabbau"}
    ],
    "TE 10: Kurzsprint-Volumen & Laktattoleranz": [
        {"block": "Vorbereitung", "uebung": "Technik-Steigerungslauf (STL)", "s": "4", "w": "50m", "zl": "–", "int": "Bis 80% Vmax", "p": "Gehp.", "fokus": "Temperaturerhöhung"},
        {"block": "Block 1: Reiz", "uebung": "Hürdensteigesprünge (12 Hürden)", "s": "2", "w": "4 Dg.", "zl": "–", "int": "Explosiv", "p": "3 Min.", "fokus": "Alpha-Motoneuronen"},
        {"block": "Block 2: Komplex", "uebung": "Kurzsprint-Volumen", "s": "6", "w": "20m", "zl": "–", "int": "100%", "p": "90s", "fokus": "Rekrutierung Fast-Twitch"},
        {"block": "Block 2: Laktat", "uebung": "Tempoläufe (Kappungsgrenze)", "s": "4", "w": "150m", "zl": "–", "int": "80% Vmax", "p": "30s Wende", "fokus": "Skisprung-Spezifisches Laktatlimit"},
        {"block": "Block 3: Athletik", "uebung": "Aufricht-Einwurfcrunch", "s": "3", "w": "15 Wdh", "zl": "3-5 kg", "int": "Explosiv", "p": "Wechsel", "fokus": "Rumpfbeschleunigung"},
        {"block": "Cool-Down", "uebung": "Statische Dehnung", "s": "1", "w": "10 Min", "zl": "–", "int": "Passiv", "p": "–", "fokus": "Detonisierung Beuger"}
    ],
    "TE 11: Neuromuskuläre Maximalrekrutierung": [
        {"block": "Vorbereitung", "uebung": "Shuttle-Einlaufen", "s": "1", "w": "400m", "zl": "–", "int": "Leicht", "p": "–", "fokus": "Gelenkvorbereitung"},
        {"block": "Block 1: Reiz", "uebung": "Fallstarts", "s": "4", "w": "15m", "zl": "–", "int": "Max. Frequenz", "p": "90s", "fokus": "Neuronale Zündung"},
        {"block": "Block 2: Komplex", "uebung": "Squat Master", "s": "5", "w": "4 Wdh", "zl": zl_speed_jumper, "int": "Maximal explosiv", "p": "150s", "fokus": "Vertikaler Streckimpuls"},
        {"block": "Block 2: Komplex", "uebung": "Fliegende Sprints", "s": "3", "w": "20m (15m Anlauf)", "zl": "–", "int": "100%", "p": "120s", "fokus": "Top-Speed Transfer"},
        {"block": "Block 3: Kraft", "uebung": "Leg Speed Curler (Beincurl)", "s": "3", "w": "20 Wdh", "zl": "Körpergewicht", "int": "Submaximal", "p": "60s", "fokus": "Ischiocrurale Sicherung"},
        {"block": "Cool-Down", "uebung": "Auslaufen", "s": "1", "w": "300m", "zl": "–", "int": "Locker", "p": "–", "fokus": "Aktive Erholung"}
    ],
    "TE 12: Spezifische Trainingsteuerung-Synthese": [
        {"block": "Vorbereitung", "uebung": "Spez. Erw. (STL locker/freq.)", "s": "4", "w": "60m", "zl": "–", "int": "80% Vmax", "p": "Trinkp.", "fokus": "Systemaktivierung"},
        {"block": "Block 1: Reiz", "uebung": "Reaktive Mehrfachsprünge (Barriere)", "s": "3", "w": "8 Knt.", "zl": "–", "int": "Maximal reaktiv", "p": "120s", "fokus": "Minimale Kontaktzeit"},
        {"block": "Block 2: Komplex", "uebung": "Spezifische Anlauf-Imitation", "s": "4", "w": "5 Wdh", "zl": zl_speed_jumper, "int": "Wettkampf", "p": "180s", "fokus": "Absprung-Präzision & Flugphase"},
        {"block": "Block 3: Athletik", "uebung": "TRX-Zug im Schrägliegehang", "s": "3", "w": "15 Wdh", "zl": "Körpergewicht", "int": "Zügig / stabil", "p": "Wechsel", "fokus": "Flugphasen-Stabilität (Skapula)"},
        {"block": "Cool-Down", "uebung": "Regeneration & Tonus-Regulation", "s": "1", "w": "10 Min", "zl": "–", "int": "Individuell", "p": "–", "fokus": "Wettkampf-Nachbereitung"}
    ]
}

aktuelle_te_daten = einheiten_db.get(te_wahl, einheiten_db["TE 1: Ansteuerung & Kommando-Sprints"])

te_titel = te_wahl.split(":")[0]

html_matrix = f"""<div style="background-color: #111111; padding: 20px; border: 2px solid #45a29e; border-radius: 8px;">
<h3 style="border-bottom: 2px solid #66fcf1; padding-bottom: 5px; margin-top: 0; color: #66fcf1 !important;">MATRIX SKISPRINGEN - {te_titel}</h3>
<p style="color: #ffffff !important; font-size: 15px;"><strong>Athlet:</strong> {ziel} | <strong>Geschlecht:</strong> {geschlecht_wahl} | <strong>Fasertyp:</strong> {ft} | <strong>SBE:</strong> {sbe_ziel}</p>
<table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #000000; border: 1px solid #7F7F7F;">
<thead>
<tr style="background-color: #1F4E78; color: #FFFFFF; font-weight: bold; text-align: left;">
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 15%;">Block / Phase</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 25%;">Trainingsmittel / Übung</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 8%; text-align: center;">Sätze</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 14%;">Wdh. / Distanz</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 13%;">Zusatzlast (ZL)</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 10%;">Intensität</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 7%; text-align: center;">Pause</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 8%;">SBE(Ist)</th>
</tr>
</thead>
<tbody>"""

for row in aktuelle_te_daten:
    bg_color = farben.get(row["block"], "#FFFFFF")
    html_matrix += f'<tr style="background-color: {bg_color};"><td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold; color: #000000 !important;">{row["block"]}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; color: #000000 !important;">{row["uebung"]}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center; color: #000000 !important;">{row["s"]}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; color: #000000 !important;">{row["w"]}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; color: #000000 !important;">{row["zl"]}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; color: #000000 !important;">{row["int"]}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center; color: #000000 !important;">{row["p"]}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; color: #000000 !important;"></td></tr>'

html_matrix += "</tbody></table></div>"

st.markdown(html_matrix, unsafe_allow_html=True)

st.markdown("---")
st.download_button(
    label="💾 Trainingsplan als HTML direkt im Download-Ordner speichern",
    data=html_matrix,
    file_name=f"Skispringen_{ziel.replace(' ', '_')}.html",
    mime="text/html"
)

col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
with col_f2:
    st.markdown("""<div class="footer-box"><h2 style="color: #66fcf1 !important; margin-bottom: 10px; font-family: Arial, sans-serif;">Aufgeben gilt nicht!</h2><p style="color: #ffffff; font-size: 14px; letter-spacing: 1px;">DOC ATHLETIC EVOLUTION - SKISPRINGEN 35.2</p></div>""", unsafe_allow_html=True)
    lade_bild(["Foto.jpg", "Foto.jpg.jpg", "foto.jpg", "foto.jpg.jpg"], use_col=True)
