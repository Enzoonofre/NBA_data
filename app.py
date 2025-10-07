import streamlit as st
import pandas as pd
import altair as alt

# Configuração inicial
st.set_page_config(page_title="🏀 Dashboard NBA", layout="wide")
st.title("🏀 Dashboard NBA")

# Estilo customizado
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] {
        width: 200px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 60px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- CARREGAMENTO DOS DADOS ---
# (ajuste o caminho conforme seu projeto)
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("data/processed/data_all_teams_all_seasons.csv")  # arquivo unificado
        return df
    except FileNotFoundError:
        st.error("Arquivo 'data_all_teams.csv' não encontrado!")
        return None

df = carregar_dados()

# --- DEFINIÇÃO DAS ABAS ---
aba_home, aba_melhores, aba_evolucao, aba_ranking = st.tabs([
    "🏠 Home",
    "🏆 Melhores Times por Temporada",
    "📈 Evolução de Desempenho",
    "📊 Ranking Geral"
])

# Dicionário de logos (mantém o seu original)
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

teams = list(team_logos.keys())

# --- ABA HOME ---
with aba_home:
    st.markdown("""
    Bem-vindo ao **Dashboard NBA**! 📊  

    Explore estatísticas, rankings e evolução dos times ao longo dos anos.  
    Selecione um time abaixo para visualizar sua página individual.
    """)
    cols = st.columns(5)
    for i, team in enumerate(teams):
        with cols[i % 5]:
            st.image(team_logos[team], width=80)
            if st.button(team):
                st.session_state["selected_team"] = team
                st.switch_page("pages/front.py")

# --- ABA MELHORES TIMES POR TEMPORADA ---
with aba_melhores:
    if df is not None:
        st.subheader("🏆 Melhor Time por Temporada")

        if "SeasonID" in df.columns and "WINS" in df.columns:
            # Seleciona o time com mais vitórias em cada temporada
            melhores = df.loc[df.groupby("SeasonID")["WINS"].idxmax()]

            for _, row in melhores.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    # Exibe o logo do time, se existir no dicionário
                    st.image(team_logos.get(row["TeamName"], ""), width=80)
                with col2:
                    st.markdown(
                        f"### {row['TeamCity']} {row['TeamName']} ({row['SeasonID']}) — {row['WINS']} vitórias"
                    )

# --- ABA EVOLUÇÃO DE DESEMPENHO ---
with aba_evolucao:
    if df is not None:
        st.subheader("📈 Evolução de Desempenho por Time")

        time_sel = st.selectbox("Selecione o time:", teams)
        df_time = df[df["TeamName"] == time_sel].copy()

        if not df_time.empty:
            # Criar coluna com apenas o ano (opcional)
            df_time.loc[:, "Season"] = df_time["SeasonID"].astype(str).str[-4:]

            chart = alt.Chart(df_time).mark_line(point=True, color="#EC0A36").encode(
                x=alt.X("Season:O", title="Temporada"),
                y=alt.Y("WinPCT:Q", title="Win %"),
                tooltip=["Season", "WinPCT"]
            ).properties(width=700, height=400)

            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Nenhum dado disponível para este time.")

# --- ABA RANKING GERAL ---
with aba_ranking:
    if df is not None:
        st.subheader("📊 Ranking Geral (por vitórias totais)")

        # Agrupar por nome do time e somar as vitórias
        ranking = (
            df.groupby("TeamName")["WINS"]
            .sum()
            .reset_index()
            .sort_values(by="WINS", ascending=False)
        )

        # Exibir tabela
        st.dataframe(ranking, width='stretch')

        # Exibir gráfico de barras
        st.bar_chart(ranking.set_index("TeamName")["WINS"])
