import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="Methodik: Performance vs Pressure", layout="wide")

st.title("Performance vs Pressure Modell and its Influence on Well-Being" )
st.write("Klicke auf eine Athleten-Box, eine Achsenbeschriftung oder die Well-Being-Texte, um die Definition und Beispieleanzuzeigen.")

# --- 1. Einheitliche Datenstruktur für interaktive Elemente ---
unified_data = pd.DataFrame({
    'Id': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'Type': ['Athlete', 'Athlete', 'Athlete', 'Athlete', 'Athlete', 'Athlete', 'Athlete', 'Axis', 'Axis', 'Axis', 'Axis', 'LegendText', 'LegendText'],
    'X': [5, 18, 89, 47, 79, 95, 70, 50, 50, -12, 112, 10, 90], 
    'Y': [88, 15, 95, 55, 38, 57, 10, 105, -5, 50, 50, -21, -21],
    'Text': ['Hans', 'Sarah', 'mathilde', 'Hans', 'Hans', 'Hans', 'Hans', 'High Pressure', 'Low Pressure', 'Low Performance', 'High Performance', 'High Well-Being', 'Low Well-Being'],
    'Farbe': ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], 
    'HoverLabel': [
        'Hans (Oben Links) analysieren', 'Sarah (Unten Links) analysieren', 'mathilde (Oben Rechts) analysieren', 
        'Hans (Zentrum) analysieren', 'Hans (Flow-Zone) analysieren', 
        'Hans (Rechte Achse) analysieren', 'Hans (Unten Rechts) analysieren',
        'Definition: High Pressure', 'Definition: Low Pressure', 
        'Definition: Low Performance', 'Definition: High Performance',
        'Definition: High Well-Being', 'Definition: Low Well-Being'
    ],
    'Titel': [
        "Athleten-Profil: Hans (Quadrant A)",
        "Athleten-Profil: Sarah (Quadrant C)",
        "Athleten-Profil: mathilde (Quadrant B)",
        "Athleten-Profil: Hans (Zentraler Übergang)",
        "Athleten-Profil: Hans (Wohlbefindens-Zone)",
        "Athleten-Profil: Hans (Leistungs-Fokus)",
        "Athleten-Profil: Hans (Geringer Druck)",
        "Dimension: High Pressure (Hoher Druck)",
        "Dimension: Low Pressure (Tiefer Druck)",
        "Dimension: Low Performance (Tiefe Leistung)",
        "Dimension: High Performance (Hohe Leistung)",
        "Konzept: High Well-Being (Hohes Wohlbefinden)",
        "Konzept: Low Well-Being (Geringes Wohlbefinden)"
    ],
    'Beschreibung': [
        "**Hans (Top Left):** Befindet sich in einer akuten Überlastungsphase ('Choking under Pressure'). Hoher externer Erwartungsdruck führt zu mentalen Blockaden und beeinträchtigt sein Wohlbefinden massiv.",
        "**Sarah (Bottom Left):** Erlebt eine Phase der sportlichen Unterforderung oder Resignation. Es fehlt an notwendiger Aktivierung und klaren Zielen, was zu einem niedrigen Wohlbefinden führt.",
        "**mathilde (Top Right):** Zeigt absolute 'Peak Performance' unter hohem Druck. Sie kann die Aktivierung produktiv nutzen, steht durch die dauerhafte Belastung jedoch nahe an der Erschöpfungsgrenze.",
        "**Hans (Zentrum):** Befindet sich im neutralen Übergangsbereich des Achsenkreuzes. Weder Belastungsspitzen noch außergewöhnliche Leistungsausschläge sind aktuell sichtbar.",
        "**Hans (Flow-Zone):** Erlebt maximale Spielfreude und intrinsische Motivation. Hohes Wohlbefinden im geschützten grünen Bereich ermöglicht exzellente, stabile Leistungen.",
        "**Hans (Far Right):** Liefert punktgenaue Spitzenleistungen ab. Das Vertrauen in die eigenen Fähigkeiten ist extrem hoch, während der Druck im optimalen, kontrollierbaren Bereich bleibt.",
        "**Hans (Bottom Right):** Trainiert und agiert völlig stressfrei. Das Wohlbefinden ist stabil, die sportliche Leistung befindet sich im absolut soliden, unaufgeregten Bereich.",
        "**High Pressure:** Externe oder interne Belastungsfaktoren, die eine hohe psychische oder physische Aktivierung vom Athleten fordern (z.B. Wettkampfdruck, Erwartungshaltung).",
        "**Low Pressure:** Ein Zustand geringer äußerer Reize oder Stressoren. Kann zu Entspannung und Gelassenheit, unter Umständen aber auch zu Unteraktivierung führen.",
        """**Low Performance (Experten-Zitate & Definitionen):**

* *“A bad performance would have to actually have mistakes in these plans, in your plan, meaning, I don't know, probably missing a grab early off on the rails, a bad landing, stuff like this.”* (A, p.3)
* *“But then you need to think if those technical mistakes comes from only a technical part, or if it is because you could not handle the pressure of the competition, for example. So it's not only a technical mistake. The technical mistake would come from not being able to handle the pressure of the competition, for example.”* (A, p.3)
* *“Eine schlechte Leistung ist für mich einerseits, wenn man nicht realistisch umgehen kann mit den Erwartungen, also mit den Erwartungen. Sprich, man hat jetzt zwei Monate trainiert, man weiss, wo man ist und plötzlich setzt man die Erwartungen viel höher. und man hat das Gefühl, jetzt, bei dem Tag X, er verändert man die Welt neu und hat dadurch eigentlich mehr Druck und Leistung als solches.”* (B, p.4)
* *“Wenn wirklich das Ganze, was du eben trainiert hast, und das wirklich völlig auseinandergekehrt und absolut völlig, nicht einmal annähernd, dorthin kommst du, wo du eigentlich könntest oder müsstest, also aufgrund von einer Leistung in den letzten zwei Monaten.”* (B, p.4)
* * silent_wind *“Dass so plötzlich so vielleicht Wind ist, also die äusseren Voraussetzungen ein bisschen schwieriger sind wie normal. Und dass man eigentlich die zum Thema macht, anstatt sich eigentlich auf das konzentriert.”* (B, p.4)
* *“Auseinanderfallen kann es auch wegen neuem Park, andere Schneebedingungen etc.”*""",
        """**High Performance (Experten-Zitate & Definitionen):**

* *“In general, a good performance is that when you achieve your plan, (…). And if you're able to perform those tricks with a really good execution, the way you planned it, then it's a good performance, (…).”* (A, p.3)
* *“Eine gute Leistung für mich im Sport ist, wenn ein Athlet oder ein Athlet das am Tag X anrufen kann, was man erwartet hat oder kann erwarten. (…). Und die Erwartungen für mich als Coach ist immer, man sieht ja eigentlich die Athleten über mehrere Wochen, Monate und weiss eigentlich, wo auf welcher Flughöhe oder wo das gerade sind, was das sie gerade können, und wo sie auch regelmässig abrufen können.”*""",
        "**High Well-Being:** Ein Zustand im Leistungssport, der durch hohe psychische Ressourcen, emotionale Balance, intrinsische Motivation und ein starkes Gefühl der Selbstwirksamkeit gekennzeichnet ist.",
        "**Low Well-Being:** Ein kritischer Zustand psychischer Erschöpfung oder Überlastung. Häufig ausgelöst durch anhaltenden Stress, Verletzungen oder mangelnde soziale Unterstützung."
    ]
})

athletes = unified_data[unified_data['Type'] == 'Athlete']
axes = unified_data[unified_data['Type'] == 'Axis']
legend_texts = unified_data[unified_data['Type'] == 'LegendText']

# --- 2. Mathematische Generierung des exakten Farbverlaufs (0 bis 100) ---
x_grid = [x for x in range(0, 101, 2)]
y_grid = [y for y in range(0, 101, 2)]
Z = []

for y in y_grid:
    row = []
    for x in x_grid:
        if x <= 50:
            pct = (50 - x) / 50
            val = 0.5 + pct * 0.45
            if y > 50:
                val += ((y - 50) / 50) * pct * 0.15
            val = min(1.0, val)
        else:
            mask_x = max(0, 1 - (abs(x - 90) / 35)**2)
            mask_y = max(0, 1 - (abs(y - 50) / 31)**2)
            intensity = mask_x * mask_y * 0.42
            val = 0.5 - intensity
        
        if y > 85:
            top_factor = (y - 85) / 15
            top_factor = min(1.0, max(0.0, top_factor))
            
            if x > 50:
                val = 0.5 * (1 - top_factor) + 1.0 * top_factor
            else:
                val = val * (1 - top_factor) + 1.0 * top_factor
            
        row.append(val)
    Z.append(row)

custom_colorscale = [
    [0.0, '#7bcd7b'],  # Vibrant Green
    [0.5, '#EAEAEA'],  # Neutral Light Gray/White
    [1.0, '#E05638']   # Warm Red/Orange
]

# --- 3. Grafik zusammenbauen ---
fig = go.Figure()

# Hintergrund-Verlauf exakt auf den Bereich 0-100 begrenzt
fig.add_trace(go.Heatmap(
    x=x_grid, y=y_grid, z=Z,
    colorscale=custom_colorscale,
    showscale=False,
    hoverinfo='skip'
))

# Der große, zentrierte Farbstreifen unter dem Modell (Y = -24 bis -18, X = 25 bis 75)
bar_x = [x for x in range(25, 76, 1)]
bar_y = [y for y in range(-24, -17, 1)]
bar_Z = [[(x - 25) / 50 for x in bar_x] for y in bar_y]

fig.add_trace(go.Heatmap(
    x=bar_x, y=bar_y, z=bar_Z,
    colorscale=custom_colorscale,
    showscale=False,
    hoverinfo='skip'
))

# Gekürzte Achsenlinien
fig.add_shape(type="line", x0=3, y0=50, x1=97, y1=50, line=dict(color="black", width=4))   # Horizontale Achse gekürzt
fig.add_shape(type="line", x0=50, y0=3, x1=50, y1=97, line=dict(color="black", width=4))  # Vertikale Achse gekürzt

# Pfeilspitzen exakt auf den Außenkanten verankert
arrow_style = dict(xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor="black", standoff=0)
fig.add_annotation(x=100, y=50, ax=50, ay=50, **arrow_style)  # Spitze Rechts
fig.add_annotation(x=0, y=50, ax=50, ay=50, **arrow_style)    # Spitze Links
fig.add_annotation(x=50, y=100, ax=50, ay=50, **arrow_style)   # Spitze Oben
fig.add_annotation(x=50, y=0, ax=50, ay=50, **arrow_style)     # Spitze Unten

# Die 7 Athleten-Boxen im Vordergrund
fig.add_trace(go.Scatter(
    x=athletes['X'], y=athletes['Y'],
    mode='markers+text',
    marker=dict(symbol='square', size=52, color='#5492b3', line=dict(width=1, color='#1b3f54')),
    text=athletes['Text'], textposition="middle center",
    textfont=dict(color="white", size=11, family="Arial", weight="bold"),
    hoverinfo='text', hovertext=athletes['HoverLabel'], customdata=athletes['Id']
))

# Die interaktiven Achsentexte hinzufügen
fig.add_trace(go.Scatter(
    x=axes['X'], y=axes['Y'],
    mode='text', text=axes['Text'],
    textfont=dict(size=18, color="black", family="Arial", weight="bold"),
    hoverinfo='text', textposition="middle center", hovertext=axes['HoverLabel'], customdata=axes['Id']
))

# Die interaktiven Legenden-Texte links und rechts neben dem Balken hinzufügen
fig.add_trace(go.Scatter(
    x=legend_texts['X'], y=legend_texts['Y'],
    mode='text', text=legend_texts['Text'],
    textfont=dict(size=15, color="#333333", family="Arial", weight="bold"),
    hoverinfo='text', textposition="middle center", hovertext=legend_texts['HoverLabel'], customdata=legend_texts['Id']
))

# Layout-Einstellungen
fig.update_layout(
    clickmode='event+select',
    xaxis=dict(visible=False, range=[-25, 125], fixedrange=True), 
    yaxis=dict(visible=False, range=[-32, 118], fixedrange=True),
    paper_bgcolor='rgba(0,0,0,0)', 
    showlegend=False,
    height=820,
    margin=dict(l=10, r=10, t=10, b=10)
)

# Render
selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", config={'displayModeBar': False, 'doubleClick': False})

# Interaktive Auswertung unter dem Modell
if selected_point and "selection" in selected_point and selected_point["selection"]["points"]:
    clicked_id = selected_point["selection"]["points"][0]["customdata"]
    current_selection = unified_data[unified_data['Id'] == clicked_id].iloc[0]
    st.markdown(f"### {current_selection['Titel']}")
    st.info(current_selection['Beschreibung'])
else:
    st.write("💡 *Tipp: Klicke auf eine blaue Athleten-Box, die Achsentexte oder die Well-Being-Labels, um die Definitionen einzublenden.*")