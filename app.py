import streamlit as st
import plotly.graph_objects as go
import textwrap

# --- Seiteneinstellungen ---
st.set_page_config(page_title="Performance vs Pressure", layout="wide")

# --- Datenstruktur der Faktoren ---
risk_env = ["Sport-specific stressors", "Stigma towards help-seeking", "Lack of social support", "Crisis-type retirement", "Individual/aesthetic sports features"]
risk_pers = ["Injury and Overtraining", "Poor general health", "Adverse life events", "Risk behavior & ineffective coping", "Female athlete triad", "Poor eating/sleeping/drinking habits", "Chronic life Stress", "Maladaptive personality & identity", "Negative social relationships", "Basic needs & career dissatisfaction"]

prot_env = ["MH literacy and support", "Trusting & mastery-orientated climate", "Positive sporting relationships", "Successful retirement adjustment"]
prot_pers = ["Positive social relationships", "Recovery", "Feeling of competence", "Basic needs & career satisfaction", "Feeling of autonomy", "Protective behavior"]

all_risks = risk_env + risk_pers
all_prots = prot_env + prot_pers

# --- Session State Initialisierung (Für automatische Klicks) ---
for f in all_risks + all_prots:
    if f not in st.session_state:
        st.session_state[f] = False

if "athlete" not in st.session_state:
    st.session_state.athlete = "Keine Auswahl / Reset"

# Profile für die automatische Checkbox-Auswahl
athlete_profiles = {
    "Elena (Quad A)": {
        "risk": ["Adverse life events", "Risk behavior & ineffective coping", "Sport-specific stressors"],
        "prot": []
    },
    "Marc (Quad B)": {
        "risk": ["Chronic life Stress", "Sport-specific stressors"],
        "prot": ["Feeling of competence"]
    },
    "Julian (Quad C)": {
        "risk": ["Basic needs & career dissatisfaction", "Maladaptive personality & identity"],
        "prot": []
    },
    "Sina (Quad D)": {
        "risk": [],
        "prot": ["Feeling of autonomy", "Protective behavior", "Feeling of competence"]
    },
    "Keine Auswahl / Reset": {"risk": [], "prot": []}
}

# Callback-Funktion: Aktualisiert die Checkboxen, wenn ein Athlet geklickt wird
def on_athlete_change():
    selected = st.session_state.athlete
    profile = athlete_profiles[selected]
    for f in all_risks:
        st.session_state[f] = (f in profile["risk"])
    for f in all_prots:
        st.session_state[f] = (f in profile["prot"])

# --- Layout Start ---
st.title("Methodik: Performance vs Pressure Modell")

# 1. Sprung-Ergebnisse
st.write("### 1. Sprung-Ergebnisse (Wettkampf)")
c1, c2, c3 = st.columns(3)
run1 = c1.radio("Run 1", ["Ausstehend", "Gestanden 👍", "Nicht gestanden 👎"])
run2 = c2.radio("Run 2", ["Ausstehend", "Gestanden 👍", "Nicht gestanden 👎"])
run3 = c3.radio("Run 3", ["Ausstehend", "Gestanden 👍", "Nicht gestanden 👎"])

st.markdown("---")
st.write("### 2. Athleten & Einflussfaktoren (Küttel & Larsen, 2020)")

# Athleten-Auswahl (Triggert die Checkboxen automatisch)
st.radio("Wähle einen Athleten, um sein Profil zu laden:", 
         list(athlete_profiles.keys()), 
         key="athlete", 
         horizontal=True, 
         on_change=on_athlete_change)

# 2. Layout: 3 Spalten
col_risk, col_graph, col_prot = st.columns([1.2, 2.5, 1.2])

active_risk = 0
active_prot = 0

# Linke Spalte: Risikofaktoren
with col_risk:
    st.markdown("<h5 style='color: #d62728;'>🚨 Risk Factors</h5>", unsafe_allow_html=True)
    st.write("**Sport-environmental**")
    for f in risk_env:
        if st.checkbox(f"🔴 {f}", key=f): active_risk += 1
    st.write("**Personal**")
    for f in risk_pers:
        if st.checkbox(f"🔴 {f}", key=f): active_risk += 1

# Rechte Spalte: Schutzfaktoren
with col_prot:
    st.markdown("<h5 style='color: #2ca02c;'>🛡️ Protective Factors</h5>", unsafe_allow_html=True)
    st.write("**Sport-environmental**")
    for f in prot_env:
        if st.checkbox(f"🟢 {f}", key=f): active_prot += 1
    st.write("**Personal**")
    for f in prot_pers:
        if st.checkbox(f"🟢 {f}", key=f): active_prot += 1

# --- 3. Logik für Hintergrund und Punkte ---
net_score = active_prot - active_risk

# Hintergrundfarbe berechnen
if net_score > 0:
    alpha = min(0.35, (net_score / 6) * 0.35) 
    bg_color = f"rgba(44, 160, 44, {alpha})"
elif net_score < 0:
    alpha = min(0.35, (abs(net_score) / 8) * 0.35)
    bg_color = f"rgba(214, 39, 40, {alpha})"
else:
    bg_color = "rgba(0,0,0,0)"

# Dynamischer Startpunkt (t1) des Wettkämpfers anpassen
# Start Performance = 50 (Exakt in der Mitte), Start Pressure = 70 (hohe Körperspannung)
base_perf = max(10, min(90, 50 + (active_prot * 3) - (active_risk * 3)))
base_pres = max(10, min(90, 70 - (active_prot * 3) + (active_risk * 3)))

def get_color(perf, pres):
    if pres > 50 and perf < 50: return "red"
    if pres > 50 and perf >= 50: return "#FFD700"
    if pres <= 50 and perf < 50: return "orange"
    return "lightgreen"

pts = [{"t": "t1", "perf": base_perf, "pres": base_pres, "color": get_color(base_perf, base_pres)}]

# Runs berechnen
if run1 != "Ausstehend":
    pts.append({"t": "t2", "perf": base_perf + (10 if run1 == "Gestanden 👍" else -15), 
                "pres": base_pres + (-10 if run1 == "Gestanden 👍" else 15), "color": ""})
    pts[-1]["color"] = get_color(pts[-1]["perf"], pts[-1]["pres"])

    if run2 != "Ausstehend":
        pts.append({"t": "t3", "perf": pts[-1]["perf"] + (10 if run2 == "Gestanden 👍" else -15), 
                    "pres": pts[-1]["pres"] + (-10 if run2 == "Gestanden 👍" else 15), "color": ""})
        pts[-1]["color"] = get_color(pts[-1]["perf"], pts[-1]["pres"])

        if run3 != "Ausstehend":
            pts.append({"t": "t4", "perf": pts[-1]["perf"] + (10 if run3 == "Gestanden 👍" else -15), 
                        "pres": pts[-1]["pres"] + (-20 if run3 == "Gestanden 👍" else 15), "color": ""})
            pts[-1]["color"] = get_color(pts[-1]["perf"], pts[-1]["pres"])

# Begrenzung im Diagramm
for p in pts:
    p["perf"] = max(5, min(95, p["perf"]))
    p["pres"] = max(5, min(95, p["pres"]))

# --- 4. Athleten-Profile für das Chart formatieren ---
def format_text(title, text, width=32):
    wrapped = "<br>".join(textwrap.wrap(text, width=width))
    return f"<b>{title}</b><br><br>{wrapped}"

athletes_data = {
    "Elena (Quad A)": {
        "x": 35, "y": 65, "ax": -30, "ay": -30, "xanchor": "right", "yanchor": "bottom",
        "text": format_text("Elena (Low Well-Being)", "Emotional überfordert. Hoher Druck führt zu technischem Versagen und massivem Verlust des Selbstvertrauens.")
    },
    "Marc (Quad B)": {
        "x": 65, "y": 65, "ax": 30, "ay": -30, "xanchor": "left", "yanchor": "bottom",
        "text": format_text("Marc (Low Well-Being)", "Nutzt hohen Druck als Treibstoff. Die toxische Anspannung verhindert jedoch ein dauerhaft stabiles Wohlbefinden.")
    },
    "Julian (Quad C)": {
        "x": 35, "y": 35, "ax": -30, "ay": 30, "xanchor": "right", "yanchor": "top",
        "text": format_text("Julian (Low Well-Being)", "Innere Gleichgültigkeit und Desinteresse. Resultiert in geringem Wohlbefinden, da jegliche Spannung fehlt.")
    },
    "Sina (Quad D)": {
        "x": 65, "y": 35, "ax": 30, "ay": 30, "xanchor": "left", "yanchor": "top",
        "text": format_text("Sina (High Well-Being)", "Innere Gelassenheit und starkes Vertrauen in die eigene Vorbereitung ermöglichen Spitzenleistung bei höchstem Wohlbefinden.")
    }
}

# --- 5. Modell zeichnen ---
with col_graph:
    fig = go.Figure()
    
    # Schwarzes Achsenkreuz
    fig.add_shape(type="line", x0=50, y0=-10, x1=50, y1=110, line=dict(color="black", width=4))
    fig.add_shape(type="line", x0=-10, y0=50, x1=110, y1=50, line=dict(color="black", width=4))

    # Wettkampf-Punkte zeichnen
    for p in pts:
        fig.add_trace(go.Scatter(
            x=[p['perf']], y=[p['pres']], mode='markers+text',
            marker=dict(size=22, color=p['color'], line=dict(width=2, color='black')),
            text=[p['t']], textposition="top center",
            hovertemplate=f"<b>Zeitpunkt {p['t']}</b><extra></extra>"
        ))

    # Skifahrer-Piktogramm und Textbox einblenden
    if st.session_state.athlete != "Keine Auswahl / Reset":
        ath = athletes_data[st.session_state.athlete]
        # Das Skifahrer Emoji
        fig.add_trace(go.Scatter(x=[ath['x']], y=[ath['y']], mode='text', text=["⛷️"], textfont=dict(size=45), hoverinfo='skip'))
        # Die Sprechblase (dynamisch in die Raumecken verankert)
        fig.add_annotation(
            x=ath['x'], y=ath['y'], text=ath['text'], showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
            ax=ath['ax'], ay=ath['ay'], xanchor=ath['xanchor'], yanchor=ath['yanchor'],
            bgcolor="white", bordercolor="black", borderwidth=2, borderpad=10, 
            font=dict(size=11, color="black"), align="left"
        )

    # Styling
    label_style = dict(size=16, color="black", family="Arial")
    fig.add_annotation(x=50, y=115, text="High Pressure", showarrow=False, font=label_style)
    fig.add_annotation(x=50, y=-15, text="Low Pressure", showarrow=False, font=label_style)
    fig.add_annotation(x=-25, y=50, text="Low Performance", showarrow=False, font=label_style)
    fig.add_annotation(x=125, y=50, text="High Performance", showarrow=False, font=label_style)

    fig.update_layout(
        xaxis=dict(visible=False, range=[-40, 140]), 
        yaxis=dict(visible=False, range=[-30, 130]),
        plot_bgcolor=bg_color, 
        paper_bgcolor="rgba(0,0,0,0)", 
        showlegend=False, 
        height=650, 
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})