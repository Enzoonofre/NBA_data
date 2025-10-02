import streamlit as st

st.markdown(
    """
    <style>
    /* Reduz a largura da sidebar */
    [data-testid="stSidebar"][aria-expanded="true"] {
        width: 200px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 60px;
    }

    /* Ajusta o conteúdo dentro da sidebar */
    .css-1d391kg {  /* classe interna do Streamlit (pode mudar) */
        padding-left: 10px;
        padding-right: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuração inicial
st.set_page_config(page_title="🏀 Dashboard NBA", layout="wide")
st.title("🏀 Dashboard NBA 23/24 - Home")

# Logos oficiais (CDN da NBA)
team_logos = {
    "Celtics": "https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg",
    "Thunder": "https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg",
    "Nuggets": "https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg",
    "Knicks": "https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg",
    "Bucks": "https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg",
    "Timberwolves": "https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg",
    "Cavaliers": "https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg",
    "Clippers": "https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg",
    "Mavericks": "https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg",
    "Magic": "https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg",
    "Pacers": "https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg",
    "Suns": "https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg",
    "Pelicans": "https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg",
    "76ers": "https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg",
    "Lakers": "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg",
    "Heat": "https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg",
    "Bulls": "https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg",
    "Kings": "https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg",
    "Hawks": "https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg",
    "Warriors": "https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg",
    "Rockets": "https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg",
    "Nets": "https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg",
    "Raptors": "https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg",
    "Jazz": "https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg",
    "Grizzlies": "https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg",
    "Hornets": "https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg",
    "Spurs": "https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg",
    "Wizards": "https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg",
    "Trail Blazers": "https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg",
    "Pistons": "https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg",
}

# Lista de times
teams = list(team_logos.keys())

st.markdown("""
Bem-vindo ao **Dashboard NBA 23/24**! 📊  

Aqui você pode explorar estatísticas detalhadas de cada time da temporada.  
Selecione um time abaixo para abrir a página de estatísticas.
""")

# Grid de times
cols = st.columns(5)
for i, team in enumerate(teams):
    with cols[i % 5]:
        st.image(team_logos[team], width=80)
        if st.button(team):
            st.session_state["selected_team"] = team
            st.switch_page("pages/front.py")  # 🔥 redireciona para front.py
