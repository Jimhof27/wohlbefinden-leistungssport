import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="Methodik: Performance vs Pressure", layout="wide")

st.title("Performance vs Pressure and their Influence on Well-Being")
st.write("Klicke auf eine Athleten-Box, eine Achsenbeschriftung oder den unteren Farbstreifen, um die Definitionen und Beispiele anzuzeigen.")

# --- 1. Einheitliche Datenstruktur für interaktive Elemente ---
unified_data = pd.DataFrame({
    'Id': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'Type': ['Athlete', 'Athlete', 'Athlete', 'Athlete', 'Athlete', 'Athlete', 'Athlete', 'Axis', 'Axis', 'Axis', 'Axis', 'LegendText', 'LegendText', 'LegendText', 'LegendText', 'LegendText'],
    'X': [5, 18, 89, 47, 79, 95, 70, 50, 50, -12, 112, 10, 90, 35, 50, 65], 
    'Y': [88, 15, 95, 55, 38, 57, 10, 105, -5, 50, 50, -21, -21, -21, -21, -21],
    'Text': ['Jelena', 'Janis', 'Melea', 'Eva', 'Hans', 'Luca', 'Dario', 'High Pressure', 'Low Pressure', 'Low Performance', 'High Performance', 'High Well-Being', 'Low Well-Being', '', '', ''],
    'Farbe': ['black']*16, 
    'HoverLabel': [
        'Jelena analysieren', 'Janis analysieren', 'Melea analysieren', 
        'Eva analysieren', 'Hans analysieren', 'Luca analysieren', 'Dario analysieren',
        'Definition: High Pressure', 'Definition: Low Pressure', 
        'Definition: Low Performance', 'Definition: High Performance',
        'Details: High Well-Being', 'Details: Low Well-Being',
        'Details zu Well-Being', 'Details zu Well-Being', 'Details zu Well-Being'
    ],
    'Titel': [
        "JELENA (QUADRANT A)", "JANIS (QUADRANT C)", "MELEA (QUADRANT B)", "EVA (MITTE / ZENTRUM)", "HANS (WOHLBEFINDENS-ZONE)", "LUCA (SWEET SPOT)", "DARIO (QUADRANT D)",
        "Dimension: High Pressure", "Dimension: Low Pressure", "Dimension: Low Performance", "Dimension: High Performance",
        "What is Well-Being?", "What is Well-Being?", "What is Well-Being?", "What is Well-Being?", "What is Well-Being?"
    ],
    'Sport': ["Snowboard Big Air", "Freestyle Skiing", "Freestyle Skiing", "Freestyle Skiing", "Freestyle Skiing", "Freestyle Skiing", "Freestyle Skiing", "", "", "", "", "", "", "", "", ""],
    'Birthplace': ["Innsbruck", "Innsbruck", "Chur", "Zürich", "Zürich", "Luzern", "St. Moritz", "", "", "", "", "", "", "", "", ""],
    'Born': ["2005", "2006", "2003", "2004", "2001", "2002", "2000", "", "", "", "", "", "", "", "", ""],
    'Status': ["CHALLENGER", "ROOKIE", "WORLD CUP WINNER", "PRO ATHLETE", "PRO ATHLETE", "ELITE SQUAD", "NATIONAL TEAM", "", "", "", "", "", "", "", "", ""],
    
    'Beschreibung': [
        "**Jelena (High Pressure / Low Performance):**\n\n* Sie erlebt mehrere Rückschläge in kurzer Zeit.\n* Materialprobleme und fehlende Resultate verstärken den Druck.\n* Sie fürchtet, aus dem Team zu fallen.\n* Sie fühlt sich „verflucht“ und beginnt zu grübeln.\n* Die hohe interne Anspannung blockiert ihre Leistung.",
        "**Janis (Low Pressure / Low Performance):**\n\n* Er geht mit wenig Druck in den Wettkampf.\n* Unterschätzt die Situation -> „ich packe das easy“.\n* Das Warm-up wurde nicht ernst genommen.\n* Dadurch fehlt ihm die letzte Schärfe und Readiness.",
        "**Melea (High Pressure / High Performance):**\n\n* Sie performt auf sehr hohem Niveau in Top-Events wie den X Games.\n* Der Konkurrenzdruck und die Bedeutung der Events sind sehr hoch.\n* Sie kann unter diesem Druck Leistung abrufen.\n* Der dichte Kalender lässt aber wenig Raum für Erholung.\n* Über die Zeit akkumuliert sich der Stress -> Es kommt zu einem mentalen Breakdown.",
        "**Eva (Mitte / Zentrum):**\n\n* Sie hat realistische Erwartungen an ihren Wettkampf.\n* Sie orientiert sich an ihrer Form der letzten Wochen.\n* Sie spürt Nervosität, bleibt aber handlungsfähig -> notwendiger Druck.\n* Sie folgt ihrem Plan, ohne etwas erzwingen zu wollen.\n* Ihre Eltern unterstützen sie optimal.\n* Keine anstehende Selektion in der Nähe.",
        "**Hans (Flow-Zone):** Erlebt maximale Spielfreude und intrinsische Motivation. Hohes Wohlbefinden im geschützten grünen Bereich ermöglicht exzellente, stabile Leistungen.",
        "**Luca (Sweet Spot):**\n\n* Normaler und notwendiger Druck beim Wettkampf vorhanden.\n* Die Vorbereitung ist gut gelaufen -> starkes Selbstvertrauen.\n* Er ist rein intrinsisch motiviert.\n* Sein Platz im Nationalteam ist langfristig gesichert.\n* Seine Eltern unterstützen ihn vollumfänglich.",
        "**Dario (Low Pressure / High Performance):**\n\n* Er kommt nach einer schweren Verletzung zurück.\n* Die Erwartungen an Resultate sind bewusst gesenkt.\n* Sein Ziel ist nicht sofort das Podium, sondern die Freude, wieder zurück zu sein.\n* Er fährt kontrolliert und prozessorientiert.\n* Gerade weil er keinen Resultatdruck jagt, kann er frei und gut performen.\n* Die Leistung ist hoch, gemessen an seiner aktuellen Situation.",
        "High Pressure Platzhalter", "Low Pressure Platzhalter", "Low Performance Platzhalter", "High Performance Platzhalter",
        "High Well-Being Platzhalter", "Low Well-Being Platzhalter", "", "", ""
    ]
})

athletes = unified_data[unified_data['Type'] == 'Athlete']
axes = unified_data[unified_data['Type'] == 'Axis']
legend_texts_visible = unified_data[(unified_data['Type'] == 'LegendText') & (unified_data['Text'] != '')]
legend_bar_clickers = unified_data[(unified_data['Type'] == 'LegendText') & (unified_data['Text'] == '')]

# --- 2. Definition der Pop-up-Dialoge ---

# A) Athleten Pop-up
@st.dialog("Athleten-Profil", width="large")
def show_athlete_profile(profile):
    st.markdown("""
        <style>
        .hero-header { background-color: #222222; padding: 30px; border-radius: 8px; color: white; margin-bottom: 25px; font-family: 'Arial Black', Gadget, sans-serif; }
        .hero-title { font-size: 42px; font-weight: 900; letter-spacing: 1px; margin: 0; color: white; }
        .hero-subtitle { font-size: 14px; color: #aaaaaa; text-transform: uppercase; letter-spacing: 2px; margin-top: 5px; }
        .fast-facts-box { background-color: #eaf5f9; padding: 20px; border-radius: 8px; border-left: 5px solid #5492b3; font-family: Arial, sans-serif; }
        .facts-title { font-size: 11px; color: #555555; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }
        .fast-facts-header { font-size: 20px; font-weight: bold; color: #111111; margin-bottom: 15px; text-transform: uppercase; }
        .fact-item { border-bottom: 1px solid #cce2ec; padding: 8px 0; font-size: 14px; }
        .fact-label { font-weight: bold; color: #333333; }
        .fact-value { float: right; color: #555555; }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="hero-header">
            <div class="hero-title">{profile['Titel']}</div>
            <div class="hero-subtitle">NATIONAL ATHLETE PLAN: {profile['Status']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col_bio, col_facts = st.columns([1.8, 1.0])
    with col_bio:
        st.subheader("Biography")
        st.write(profile['Beschreibung'])
    with col_facts:
        st.markdown(f"""
            <div class="fast-facts-box">
                <div class="facts-title">ATHLETE</div>
                <div class="fast-facts-header">FAST FACTS</div>
                <div class="fact-item"><span class="fact-label">Sport:</span><span class="fact-value">{profile['Sport']}</span></div>
                <div class="fact-item"><span class="fact-label">Birth place:</span><span class="fact-value">{profile['Birthplace']}</span></div>
                <div class="fact-item"><span class="fact-label">Born:</span><span class="fact-value">{profile['Born']}</span></div>
            </div>
            """, unsafe_allow_html=True)

# B) Achsen Pop-ups
@st.dialog("Dimension Details", width="large")
def show_axis_profile(profile):
    st.markdown("""
        <style>
        .axis-hero { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px; font-family: 'Arial', sans-serif; }
        .axis-red-title { color: #d80b2a; font-size: 48px; font-weight: bold; margin: 0; }
        .axis-black-title { color: #222; font-size: 42px; font-weight: bold; text-align: right; margin: 0; line-height: 1.1; }
        .axis-quote { font-size: 17px; font-style: italic; color: #333; margin-bottom: 18px; line-height: 1.5; }
        .axis-summary-title { font-size: 22px; font-weight: bold; margin-top: 30px; margin-bottom: 10px; color: #000; }
        .axis-list { margin-bottom: 20px; }
        .axis-list li { font-size: 18px; margin-bottom: 8px; color: #222; }
        </style>
        """, unsafe_allow_html=True)
        
    if profile['Text'] == 'Low Performance':
        st.markdown("""
            <div class="axis-hero">
                <div class="axis-red-title">What is Performance?</div>
                <div class="axis-black-title">Low <br>Performance &#8592;</div>
            </div>
            <div class="axis-quote">"A bad performance would have to actually have mistakes in these plans, in your plan, meaning, I don't know, probably missing a grab early off on the rails, a bad landing, stuff like this" (A, p.3)</div>
            <div class="axis-quote">"But then you need to think if those technical mistakes comes from only a technical part, or if it is because you could not handle the pressure of the competition, for example. So it's not only a technical mistake. The technical mistake would come from not being able to handle the pressure of the competition, for example." (A, p.3)</div>
            <div class="axis-quote">"Dass so plötzlich so vielleicht Wind ist, also die äusseren Voraussetzungen ein bisschen schwieriger sind wie normal. Und dass man eigentlich die zum Thema macht, anstatt sich eigentlich auf das konzentriert" (B, p.4)</div>
            <div class="axis-quote">"Auseinanderfallen kann es auch wegen neuem Park, andere Schneebedingungen etc" (B, p.4)</div>
            <div class="axis-summary-title">&#10132; Mistakes in the plan</div>
            <ul class="axis-list">
                <li>Technical Mistake</li>
                <li>Choking under Pressure</li>
                <li>Verhältnisse (Wetter, Park)</li>
            </ul>
            """, unsafe_allow_html=True)
            
    elif profile['Text'] == 'High Performance':
        st.markdown("""
            <div class="axis-hero">
                <div class="axis-red-title">What is Performance?</div>
                <div class="axis-black-title">High <br>Performance &#8594;</div>
            </div>
            <div class="axis-quote">"In general, a good performance is that when you achieve your plan,(...). And if you're able to perform those tricks with a really good execution, the way you planned it, then it's a good performance,(...). (A, p.3)"</div>
            <div class="axis-quote">"Eine gute Leistung für mich im Sport ist, wenn ein Athlet oder ein Athlet das am Tag X anrufen kann, was man erwartet hat oder kann erwarten. (...). Und die Erwartungen für mich als Coach ist immer, man sieht ja eigentlich die Athleten über mehrere Wochen, Monate und weiss eigentlich, wo auf welcher Flughöhe oder wo das gerade sind, was das sie gerade können, und wo sie auch regelmässig abrufen können."</div>
            <div class="axis-summary-title">&#10132; Execute the plan</div>
            """, unsafe_allow_html=True)
            
    elif profile['Text'] == 'High Pressure':
        st.markdown("""
            <div class="axis-hero">
                <div class="axis-red-title">What is Pressure?</div>
                <div class="axis-black-title">High Pressure<br>&#8593;</div>
            </div>
            <div class="axis-summary-title">High Pressure Situation</div>
            <ul class="axis-list">
                <li>One Chance</li>
                <li>Selections</li>
                <li>Expectations of Parents</li>
                <li>Competition</li>
            </ul>
            <div class="axis-summary-title">Symptoms of High Pressure</div>
            <ul class="axis-list">
                <li>Breathing</li>
                <li>Talking to random people</li>
                <li>Losing your routine</li>
                <li>Coughing</li>
            </ul>
            <div class="axis-summary-title">Consequence of High Pressure</div>
            <div class="axis-quote">"So if you're too loose, you're losing that tension to be able to perform. <strong>But if you're too tense, then you're losing the looseness of, you know, being able to, to let it go.</strong>" (A, p.4)</div>
            
            <hr style="margin-top:40px; margin-bottom:30px; border-top: 1px solid #ccc;">
            <div class="axis-red-title" style="font-size: 38px;">Pressure Sweetspot?</div>
            
            <div class="axis-summary-title">Medium Pressure?</div>
            <div class="axis-quote">"Sometimes to be too much low pressure is, it's not helpful because you're losing a bit of focus. So I think a good balance is really important." (A,p.4)</div>
            <div class="axis-quote">"If we put pressure in terms of stress, so you produce cortisol, and you know, like, it's the same for the body, if you produce too much cortisol, it's toxic for the body. <strong>But a little cortisol is the fuel of performance.</strong> So you need that little stress to be to have all your sense aware." (A,p.5)</div>
            <div class="axis-quote">"So all your awareness to be able to get to really focus to, to be in the moment and all that." (A,p.5)</div>
            
            <div class="axis-summary-title">Finding the balance</div>
            <div class="axis-quote">"So the last mix, yeah, good mix, like, it's hard to find the line, actually, because sometimes you're trying to be to lose, because you want to not have that pressure. And then you're losing that tension. And when you over tense, because, like, especially the second run and stuff, sometimes it's, yeah, it's a tough one. So it's hard to find the balance." (A,p.5)</div>
            """, unsafe_allow_html=True)
            
    elif profile['Text'] == 'Low Pressure':
        st.markdown("""
            <div class="axis-hero">
                <div class="axis-red-title">What is Pressure?</div>
                <div class="axis-black-title"><br>Low Pressure<br>&#8595;</div>
            </div>
            <div class="axis-summary-title">Symptoms of Low Pressure</div>
            <div class="axis-quote">"Wenn kein Druck gekommen ist, ja, dann sind sie einfach allein irgendwo auf der Seite, und sind ruhig, und eben so 5 Minuten vorher sind sie noch irgendwo am Sitzen, oder machen ihre spezifischen Warmup-Übungen. Und dann 1-2 Minuten vorher, tun sie nochmal das Aktivieren machen, und nochmal wirklich schauen, so mit der Atmung, dass sie unten sind, und dann siehst du einfach, dass sie dort wissen auch, was sie machen müssen. ja. Und, erstaunlicherweise, das können etwa 30-40% der Athleten, die das schaffen, und wirklich entspannt, ohne Druck entfallen." (B, p.7)</div>
            """, unsafe_allow_html=True)

# C) Well-Being Pop-up (DYNAMISCH)
@st.dialog("Well-Being Details", width="large")
def show_wellbeing_profile(profile):
    st.markdown("""
        <style>
        .wb-hero { margin-bottom: 25px; font-family: 'Arial', sans-serif; }
        .wb-red-title { color: #d80b2a; font-size: 48px; font-weight: bold; margin: 0; }
        .wb-red-quote { font-size: 18px; font-style: italic; color: #d80b2a; margin-bottom: 18px; line-height: 1.5; }
        .wb-black-quote { font-size: 18px; font-style: italic; color: #222; margin-bottom: 18px; line-height: 1.5; }
        .wb-summary-title { font-size: 26px; font-weight: bold; margin-top: 40px; margin-bottom: 15px; color: #222; }
        </style>
        """, unsafe_allow_html=True)
        
    html_content = """
        <div class="wb-hero">
            <div class="wb-red-title">What is Well-Being?</div>
        </div>
        
        <div class="wb-summary-title" style="color:#d80b2a; margin-top:10px;">Importance of Well-Being</div>
        <div class="wb-red-quote">"Wellbeing is really, really important. I think it's important to have a balance, to find a balance as well, uh, in the planification and in the calendar to give them a space and give them time to actually be able to ski on their own, uh, to be able to shred, not only focus on competition." (A, p.19)</div>
        <div class="wb-red-quote">"Das Training muss nicht immer, wohlfühle Oase sein, Wettkampf aber schon." (B, p.21)</div>
        <div class="wb-red-quote">"Ich finde schlussendlich, Sport ist etwas Schönes, Leistungssport ist etwas Geiles, es ist etwas Herz, es sind Entbehrungen, aber es darf ruhig auch ein bisschen Spass machen und man soll sich wohlfühlen, und man soll nicht als ein psychologisches Frack aus dem Sport rausgehen. Also, man muss sich wohlfühlen. ja, man hat ja schlussendlich irgendwann mal mit dem Sport angefangen, das wahrscheinlich das Geilste ist, für einen selber. Und das soll es bis zum Schluss so sein." (B, p.21)</div>
        
        <div class="wb-summary-title">Balance</div>
        <div class="wb-black-quote">"So well-being would be able to, to find a good balance between pushing yourself and having fun." (A,p.6)</div>
        <div class="wb-black-quote">"You need to always, to not forget that why you do sport for, and to always put back the, the pleasure as well in the center. I know we do competition. I know we want to perform, but we also, it's also important that you have pleasure doing it." (A,p.5)</div>

        <div class="wb-summary-title">Selbstwirksamkeit</div>
        <div class="wb-black-quote">"Ein höchstes Wohlbefinden hat ein Athlet oder eine Athletin, wo, da gehe ich wirklich auf den Leistungssport, eher auf die Elite ein, ähm, die wenig brauchen. Leute, die wenig brauchen. Sie wissen, wann sie etwas brauchen, bei wem, bei welcher Person sie das holen können. dann sind sie bei sich, sie sind sich der Situation bewusst, wo sie drin sind, und, ja, und wissen auch, wie handeln." (B,p.7)</div>
        
        <div style="text-align: center; font-size: 32px; font-weight: bold; margin-top: 35px; margin-bottom: 25px;">&#10132; Eudamonic</div>
    """
    
    if profile['Text'] != 'High Well-Being':
        html_content += """
        <hr style="margin-top:30px; margin-bottom:20px; border-top: 1px solid #ccc;">
        <div class="wb-summary-title">Symptoms of Low Well-Being</div>
        <div class="wb-black-quote">"irgendjemand, der plötzlich mich noch fragt, wie ist der Wind? Und dann geht er, in zwei Sekunden später, eine andere Athletin zu fragen, und, nochmal irgendjemand, der merkt eigentlich, Situationen überfordert ihn, und zweitens, er weiss auch nicht auf welche Leute, er sich verlassen kann. weil, je nachdem, oder die meisten wissen jetzt, okay, ich muss eine Person fragen, und dann ist gut. Weil, es kann ja mal sieben, man muss nachfragen, das kann man nicht selber einschätzen." (B, p.8)</div>
        """
        
    st.markdown(html_content, unsafe_allow_html=True)

# --- 3. Mathematische Generierung des exakten Farbverlaufs (0 bis 100) ---
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

custom_colorscale = [[0.0, '#7bcd7b'], [0.5, '#EAEAEA'], [1.0, '#E05638']]

# --- 4. Grafik zusammenbauen ---
fig = go.Figure()

fig.add_trace(go.Heatmap(x=x_grid, y=y_grid, z=Z, colorscale=custom_colorscale, showscale=False, hoverinfo='skip'))

bar_x = [x for x in range(25, 76, 1)]
bar_y = [y for y in range(-24, -17, 1)]
bar_Z = [[(x - 25) / 50 for x in bar_x] for y in bar_y]
fig.add_trace(go.Heatmap(x=bar_x, y=bar_y, z=bar_Z, colorscale=custom_colorscale, showscale=False, hoverinfo='skip'))

# Gekürzte Achsenlinien & Pfeile
fig.add_shape(type="line", x0=3, y0=50, x1=97, y1=50, line=dict(color="black", width=4))
fig.add_shape(type="line", x0=50, y0=3, x1=50, y1=97, line=dict(color="black", width=4))
arrow_style = dict(xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor="black", standoff=0)
fig.add_annotation(x=100, y=50, ax=50, ay=50, **arrow_style)
fig.add_annotation(x=0, y=50, ax=50, ay=50, **arrow_style)
fig.add_annotation(x=50, y=100, ax=50, ay=50, **arrow_style)
fig.add_annotation(x=50, y=0, ax=50, ay=50, **arrow_style)

# Athleten-Boxen
fig.add_trace(go.Scatter(
    x=athletes['X'], y=athletes['Y'], mode='markers+text',
    marker=dict(symbol='square', size=52, color='#5492b3', line=dict(width=5, color='white')),
    text=athletes['Text'], textposition="middle center", textfont=dict(color="white", size=11, family="Arial", weight="bold"),
    hoverinfo='text', hovertext=athletes['HoverLabel'], customdata=athletes['Id']
))

# Achsentexte (High Performance, etc.)
fig.add_trace(go.Scatter(
    x=axes['X'], y=axes['Y'], mode='text', text=axes['Text'],
    textfont=dict(size=18, color="black", family="Arial", weight="bold"),
    hoverinfo='text', textposition="middle center", hovertext=axes['HoverLabel'], customdata=axes['Id']
))

# Well-Being Texte (Sichtbar)
fig.add_trace(go.Scatter(
    x=legend_texts_visible['X'], y=legend_texts_visible['Y'], mode='text', text=legend_texts_visible['Text'],
    textfont=dict(size=15, color="#333333", family="Arial", weight="bold"),
    hoverinfo='text', textposition="middle center", hovertext=legend_texts_visible['HoverLabel'], customdata=legend_texts_visible['Id']
))

# UNSICHTBARE KLICK-BEREICHE FÜR DEN FARBSTREIFEN
fig.add_trace(go.Scatter(
    x=legend_bar_clickers['X'], y=legend_bar_clickers['Y'], mode='markers',
    marker=dict(size=45, opacity=0), 
    hoverinfo='text', hovertext=legend_bar_clickers['HoverLabel'], customdata=legend_bar_clickers['Id']
))

fig.update_layout(clickmode='event+select', xaxis=dict(visible=False, range=[-25, 125], fixedrange=True), yaxis=dict(visible=False, range=[-32, 118], fixedrange=True), paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=820, margin=dict(l=10, r=10, t=10, b=10))

selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", config={'displayModeBar': False, 'doubleClick': False})

# --- 5. Event-Auswertung & Pop-up Trigger ---
if selected_point and "selection" in selected_point and selected_point["selection"]["points"]:
    clicked_id = selected_point["selection"]["points"][0]["customdata"]
    current_selection = unified_data[unified_data['Id'] == clicked_id].iloc[0]
    
    if current_selection['Type'] == 'Athlete':
        show_athlete_profile(current_selection)
    
    elif current_selection['Type'] == 'Axis':
        show_axis_profile(current_selection)
        
    elif current_selection['Type'] == 'LegendText':
        show_wellbeing_profile(current_selection)
else:
    st.write("💡 *Tipp: Klicke auf eine blaue Athleten-Box, die Achsen oder den Farbstreifen, um die Detail-Ansichten zu öffnen.*")