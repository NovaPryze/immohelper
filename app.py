import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Immobilien-Vollkosten & Ertragsrechner Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR LIGHT ELEGANT / CREAM GOLD LUXURY THEME ---
st.markdown("""
<style>
    /* Haupt-Hintergrund und Textfarbe */
    .stApp {
        background-color: #F8F5EE !important;
        color: #2C2A29 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Titel & Header */
    .title-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1A1A1A;
        margin-bottom: 0.2rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    .title-header span {
        color: #C5A059;
    }

    .contact-bar {
        background-color: #FFFFFF;
        border: 1px solid #EAE3D2;
        border-radius: 50px;
        padding: 10px 24px;
        font-size: 0.88rem;
        color: #666666;
        margin: 0 auto 30px auto;
        text-align: center;
        max-width: 800px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }
    .contact-bar span {
        color: #B8860B;
        font-weight: 700;
    }

    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2C2A29;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* KPI Karten im hellen Look */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #EAE3D2;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        transition: transform 0.2s ease;
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #777777;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1A1A1A;
    }
    .kpi-sub {
        font-size: 0.82rem;
        color: #C5A059;
        font-weight: 600;
        margin-top: 6px;
    }
    .kpi-sub.negative {
        color: #D9534F;
    }

    /* Eingabefelder im edlen Look */
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border-color: #E2DBC9 !important;
        color: #1A1A1A !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #C5A059 !important;
        box-shadow: 0 0 0 1px #C5A059 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F1ECE1 !important;
        border-right: 1px solid #E2DBC9;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #B8860B !important;
    }

    /* Plotly Container Abrundung */
    .stPlotlyChart {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 12px;
        border: 1px solid #EAE3D2;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="title-header">Immobilien-Vollkosten & <span>Ertragsrechner</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="contact-bar">Bereitgestellt von <span>Immobilien-Analyse Pro</span> — Vollständige Investitionsrechnung inklusive Risikopuffer, Instandhaltung & Anschlussfinanzierung</div>',
    unsafe_allow_html=True
)

# --- SIDEBAR: PARAMETERS ---
st.sidebar.markdown("<h2 style='font-size: 1.3rem; font-weight: 700;'>⚙️ Investitionsparameter</h2>", unsafe_allow_html=True)

with st.sidebar.expander("🏢 1. Objekt- & Anschaffungskosten", expanded=True):
    flaeche = st.number_input("Wohnfläche (m²)", value=81.75, step=1.0)
    preis_pro_qm = st.number_input("Kaufpreis pro m² (€)", value=3800.0, step=50.0)
    stellplatz_preis = st.number_input("Kaufpreis Stellplatz (€)", value=10000.0, step=1000.0)
    kueche_preis = st.number_input("Kaufpreis Küche (€)", value=8000.0, step=500.0)
    nebenkosten_prozent = st.number_input("Kaufnebenkosten (Grunderwerbsteuer, Notar, Makler) (%)", value=7.0, step=0.5)
    sofort_sanierung = st.number_input("Sofortige Sanierungskosten bei Kauf (€)", value=0.0, step=1000.0)
    reservierung = st.number_input("Reservierung / Abzug (€)", value=2000.0, step=500.0)

with st.sidebar.expander("💰 2. Mieteinnahmen & Puffer", expanded=True):
    miete_kalt_wohnung = st.number_input("Soll-Miete Wohnraum (€/Monat)", value=1140.0, step=50.0)
    miete_stellplatz = st.number_input("Miete Stellplatz (€/Monat)", value=45.0, step=5.0)
    miete_kueche = st.number_input("Miete Küche (€/Monat)", value=75.0, step=5.0)
    mietsteigerung_prozent = st.number_input("Mietsteigerung alle 3 Jahre (%)", value=20.0, step=1.0)
    leerstand_prozent = st.number_input("Mietausfall- / Leerstandswagnis (%)", value=2.0, step=0.5)

with st.sidebar.expander("🛠️ 3. Bewirtschaftung & Instandhaltung", expanded=True):
    hausgeld_nicht_umlagefaehig = st.number_input("Nicht-umlagefähiges Hausgeld (€/Monat)", value=35.0, step=5.0)
    instandhaltung_pro_qm = st.number_input("Instandhaltungsrücklage (€/m²/Jahr)", value=12.0, step=1.0)

with st.sidebar.expander("🏦 4. Finanzierung & Zinsbindung", expanded=True):
    ek_nebenkosten_deckend = st.checkbox("Eigenkapital deckt mindestens Kaufnebenkosten", value=True)
    eigenkapital = st.number_input("Eingesetztes Eigenkapital (€)", value=22445.50, step=5000.0)
    sollzins = st.number_input("Anfänglicher Sollzins p.a. (%)", value=4.5, step=0.1)
    tilgung = st.number_input("Anfängliche Tilgung p.a. (%)", value=1.5, step=0.1)
    zinsbindung_jahre = st.number_input("Zinsbindungsdauer (Jahre)", value=10, step=1)
    anschlusszins = st.number_input("Prognostizierter Anschlusszins p.a. (%)", value=5.0, step=0.1)

with st.sidebar.expander("📈 5. Steuer & Wertentwicklung", expanded=True):
    gebaeudeanteil = st.number_input("Gebäudeanteil für AfA (%)", value=93.0, step=1.0)
    afa_satz = st.number_input("AfA-Satz p.a. (%)", value=3.0, step=0.5)
    grenzsteuersatz = st.number_input("Grenzsteuersatz (%)", value=40.0, step=1.0)
    wertsteigerung_prozent = st.number_input("Wertsteigerung p.a. (%)", value=3.0, step=0.5)

# --- KALKULATIONEN ---
kaufpreis_wohnung = flaeche * preis_pro_qm
kaufpreis_gesamt_objekt = kaufpreis_wohnung + stellplatz_preis
nebenkosten_euro = kaufpreis_gesamt_objekt * (nebenkosten_prozent / 100.0)
gesamtkosten = kaufpreis_gesamt_objekt + nebenkosten_euro + kueche_preis + sofort_sanierung - reservierung

fremdkapital = max(0.0, gesamtkosten - eigenkapital)

# Mieteinnahmen berechnen (inkl. Leerstand)
brutto_miete_monat = miete_kalt_wohnung + miete_stellplatz + miete_kueche
effektive_miete_monat = brutto_miete_monat * (1.0 - (leerstand_prozent / 100.0))

# Nicht umlagefähige Ausgaben
instandhaltung_monat = (flaeche * instandhaltung_pro_qm) / 12.0
betriebskosten_monat = hausgeld_nicht_umlagefaehig + instandhaltung_monat

# Kreditrate
kapitaldienst_prozent = sollzins + tilgung
bankrate_jahr = fremdkapital * (kapitaldienst_prozent / 100.0)
bankrate_monat = bankrate_jahr / 12.0

# Steuerberechnung Jahr 1
gebaeudewert = (kaufpreis_wohnung + sofort_sanierung) * (gebaeudeanteil / 100.0)
afa_jahr = gebaeudewert * (afa_satz / 100.0)
zins_jahr_1 = fremdkapital * (sollzins / 100.0)
kueche_afa = kueche_preis * 0.10

werbungskosten_jahr1 = afa_jahr + zins_jahr_1 + kueche_afa + (betriebskosten_monat * 12.0)
brutto_miete_jahr1 = effektive_miete_monat * 12.0
steuerlicher_gewinn_verlust = brutto_miete_jahr1 - werbungskosten_jahr1

steuervorteil_jahr_1 = -steuerlicher_gewinn_verlust * (grenzsteuersatz / 100.0) if steuerlicher_gewinn_verlust < 0 else 0.0
steuervorteil_monat_1 = steuervorteil_jahr_1 / 12.0

cashflow_vor_steuer = effektive_miete_monat - bankrate_monat - betriebskosten_monat
cashflow_nach_steuer = cashflow_vor_steuer + steuervorteil_monat_1

# --- TOP INPUTS BAR ---
st.markdown('<div class="section-header">⚙️ Vollkosten-Überblick</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.number_input("Gesamterwerbskosten (€)", value=round(gesamtkosten, 2), disabled=True)
with c2:
    st.number_input("Miete abgl. Leerstand (€/Monat)", value=round(effektive_miete_monat, 2), disabled=True)
with c3:
    st.number_input("Cashflow n. St. (Jahr 1) (€)", value=round(cashflow_nach_steuer, 2), disabled=True)
with c4:
    laufzeit_jahre = st.number_input("Betrachtungszeitraum (Jahre)", min_value=1, max_value=40, value=10, step=1)

# --- VERLAUFS-RECHNUNG DYNAMISCH ---
zeit_jahre = np.arange(0, laufzeit_jahre + 1)
immobilienwert_verlauf = []
restschuld_verlauf = []
cashflow_kumuliert = []
kumulierter_cashflow = 0.0

aktuelle_restschuld = fremdkapital
miete_aktuell = effektive_miete_monat
aktueller_zins = sollzins

for j in range(laufzeit_jahre + 1):
    wert_j = gesamtkosten * ((1 + wertsteigerung_prozent / 100.0) ** j)
    immobilienwert_verlauf.append(wert_j)
    
    if j == 0:
        restschuld_verlauf.append(fremdkapital)
        cashflow_kumuliert.append(0.0)
    else:
        # Mietsteigerung alle 3 Jahre
        if (j - 1) > 0 and (j - 1) % 3 == 0:
            miete_aktuell *= (1 + mietsteigerung_prozent / 100.0)
            
        # Refinanzierung nach Ablauf der Zinsbindung
        if j > zinsbindung_jahre:
            aktueller_zins = anschlusszins
            
        zins_anteil = aktuelle_restschuld * (aktueller_zins / 100.0)
        tilgung_anteil = bankrate_jahr - zins_anteil
        aktuelle_restschuld = max(0.0, aktuelle_restschuld - tilgung_anteil)
        restschuld_verlauf.append(aktuelle_restschuld)
        
        # Cashflow des Jahres berechnen
        jahres_cf = (miete_aktuell - bankrate_monat - betriebskosten_monat) * 12.0
        kumulierter_cashflow += jahres_cf
        cashflow_kumuliert.append(kumulierter_cashflow)

end_immobilienwert = immobilienwert_verlauf[-1]
end_restschuld = restschuld_verlauf[-1]
netto_eigenkapital_end = end_immobilienwert - end_restschuld
kumulierter_steuervorteil = steuervorteil_jahr_1 * laufzeit_jahre
gesamter_vermoegenszuwachs = netto_eigenkapital_end + kumulierter_steuervorteil + kumulierter_cashflow - eigenkapital

# --- KPI CARDS ---
st.markdown('<div class="section-header">📊 Rendite & Wertentwicklung</div>', unsafe_allow_html=True)

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-title">Finanzierungsstruktur</div>
        <div class="kpi-value">{gesamtkosten:,.2f} €</div>
        <div class="kpi-sub">EK: {eigenkapital:,.2f} € | FK: {fremdkapital:,.2f} €</div>
    </div>
    ''', unsafe_allow_html=True)

with kpi2:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-title">Prognostizierter Wert ({laufzeit_jahre} J.)</div>
        <div class="kpi-value">{end_immobilienwert:,.2f} €</div>
        <div class="kpi-sub">Restschuld Bank: {end_restschuld:,.2f} €</div>
    </div>
    ''', unsafe_allow_html=True)

with kpi3:
    sub_class = "positive" if gesamter_vermoegenszuwachs >= 0 else "negative"
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-title">Netto-Vermögenszuwachs ({laufzeit_jahre} J.)</div>
        <div class="kpi-value">{gesamter_vermoegenszuwachs:,.2f} €</div>
        <div class="kpi-sub {sub_class}">Inkl. Tilgung, Wertgewinn & Steuern</div>
    </div>
    ''', unsafe_allow_html=True)

# --- PLOTLY CHART (DESIGN ANGEPASST AN SCREENSHOT) ---
st.markdown('<div class="section-header">📈 Wertentwicklung im Zeitverlauf</div>', unsafe_allow_html=True)

fig = go.Figure()

# Goldene Hauptkurve mit hellgoldenem Verlauf
fig.add_trace(go.Scatter(
    x=zeit_jahre,
    y=immobilienwert_verlauf,
    mode='lines',
    name='Immobilienwert (inkl. Wertsteigerung)',
    line=dict(color='#C5A059', width=3),
    fill='tozeroy',
    fillcolor='rgba(197, 160, 89, 0.15)'
))

fig.add_trace(go.Scatter(
    x=zeit_jahre,
    y=restschuld_verlauf,
    mode='lines',
    name='Restschuld Bank',
    line=dict(color='#888888', width=2, dash='dash')
))

netto_ek_verlauf = [w - r for w, r in zip(immobilienwert_verlauf, restschuld_verlauf)]
fig.add_trace(go.Scatter(
    x=zeit_jahre,
    y=netto_ek_verlauf,
    mode='lines',
    name='Netto-Eigenkapital',
    line=dict(color='#2B7A4B', width=2.5)
))

fig.update_layout(
    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    font=dict(color='#333333', family='Inter'),
    margin=dict(l=30, r=30, t=30, b=30),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=12, color='#333333')
    ),
    xaxis=dict(
        title="Laufzeit (Jahre)", 
        gridcolor='#F0ECE1', 
        zerolinecolor='#F0ECE1', 
        showgrid=True,
        dtick=1
    ),
    yaxis=dict(
        title="Wert in Euro (€)", 
        gridcolor='#F0ECE1', 
        zerolinecolor='#F0ECE1', 
        showgrid=True,
        tickformat=',.0f'
    ),
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# --- DETAILED TABULAR BREAKDOWN ---
st.markdown('<div class="section-header">📑 Vollständige Jahrestabelle</div>', unsafe_allow_html=True)

df_detail = pd.DataFrame({
    'Jahr': zeit_jahre,
    'Immobilienwert (€)': [round(x, 2) for x in immobilienwert_verlauf],
    'Restschuld Bank (€)': [round(x, 2) for x in restschuld_verlauf],
    'Netto-Eigenkapital (€)': [round(x, 2) for x in netto_ek_verlauf],
    'Kumulierter Cashflow vor St. (€)': [round(x, 2) for x in cashflow_kumuliert]
})

st.dataframe(df_detail, use_container_width=True, height=300)