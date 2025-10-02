import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown("""
    <style>
    
    /* Título com estilo NBA */
    h1 {
        color: #EC0A36 !important;
        text-transform: uppercase;
        font-weight: bold;
    }

    /* Subtítulos */
    h2, h3, h4 {
        color: #F0A500 !important; /* amarelo tipo Lakers */
    }

    /* Cards e métricas */
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 28px;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #1F2833;
    }
    </style>
""", unsafe_allow_html=True)


# Carrega o dataframe
df = pd.read_csv("data/processed/data_all_teams_23-24_season.csv")

# ========================
# Seleção do time
# ========================
st.set_page_config(page_title="📊 Dashboard NBA 23/24", layout="wide")

if "selected_team" not in st.session_state:
    st.warning("Nenhum time selecionado. Volte para a Home e escolha um time.")
    st.stop()

team = st.session_state["selected_team"]
team_data = df[df["TeamName"] == team].iloc[0]

# Texto introdutório
st.markdown(f"""
Bem-vindo ao **Dashboard NBA 23/24**! 🏀

Esta página apresenta **estatísticas detalhadas dos jogos de uma temporada** da NBA, incluindo desempenho geral, confrontos por divisão, vitórias e derrotas em diferentes situações de jogo, e análise mês a mês.

### Informações do time selecionado
- **Time:** {team_data['TeamCity']} {team_data['TeamName']}
- **Divisão:** {team_data['Division']}
- **Conferência:** {team_data['Conference']}
- **Vitórias na temporada:** {team_data['WINS']}
- **Derrotas na temporada:** {team_data['LOSSES']}
- **Win %:** {team_data['WinPCT']*100:.1f}%
""")



# ========================
# Resumo geral
# ========================
st.header(f"{team_data['TeamCity']} {team_data['TeamName']}")

col1, col2, col3 = st.columns(3)
col1.metric("Vitórias", team_data["WINS"])
col2.metric("Derrotas", team_data["LOSSES"])
col3.metric("Win %", f"{team_data['WinPCT']*100:.1f}%")

# Gráfico principal de vitórias x derrotas
fig = px.pie(
    names=["Vitórias", "Derrotas"],
    values=[team_data["WINS"], team_data["LOSSES"]],
    title=f"{team} - WINS vs LOSSES",
    color_discrete_sequence=["#EC0A36", "#F0A500"]
)
st.plotly_chart(fig, use_container_width=True)

# ========================
# Desempenho em casa e fora
# ========================
st.subheader("🏟️ Desempenho em casa e fora")

home_wins, home_losses = map(int, team_data["HOME"].split("-"))
road_wins, road_losses = map(int, team_data["ROAD"].split("-"))

fig_home = px.pie(
    names=["Vitórias em casa", "Derrotas em casa"],
    values=[home_wins, home_losses],
    title=f"HOME ({team_data['HOME']})",
    color_discrete_sequence=["#EC0A36", "#F0A500"]
)

fig_road = px.pie(
    names=["Vitórias fora", "Derrotas fora"],
    values=[road_wins, road_losses],
    title=f"ROAD ({team_data['ROAD']})",
    color_discrete_sequence=["#EC0A36", "#F0A500"]
)

col_home, col_road = st.columns(2)
col_home.plotly_chart(fig_home, use_container_width=True)
col_road.plotly_chart(fig_road, use_container_width=True)

# ========================
# Diferença de pontos
# ========================
st.subheader("⚖️ Pontos por jogo")

diff = team_data["DiffPointsPG"]

fig_points = go.Figure(data=[
    go.Bar(name="Pontos Marcados", x=["Pontos"], y=[team_data["PointsPG"]], marker_color="#EC0A36"),
    go.Bar(name="Pontos Sofridos", x=["Pontos"], y=[team_data["OppPointsPG"]], marker_color="#F0A500")
])

# Ajusta posição do texto dependendo do valor (acima se positivo, abaixo se negativo)
text_pos = "top center" if diff >= 0 else "bottom center"

fig_points.add_trace(go.Scatter(
    x=["Pontos"], y=[diff],
    mode="markers+text",
    text=[f"Diff: {diff}"],
    textposition=text_pos,
    name="Diferença",
    marker=dict(color="blue", size=12)
))

fig_points.update_layout(
    yaxis_title="Pontos",
    xaxis_title="",
    title=f"{team_data['TeamName']} - Pontos por Jogo"
)

st.plotly_chart(fig_points, use_container_width=True)
# ========================
# Streaks
# ========================
st.subheader("🔥 Sequências")
col1, col2 = st.columns(2)
col1.metric("Maior sequência de vitórias", team_data["LongWinStreak"])
col2.metric("Maior sequência de derrotas", team_data["LongLossStreak"])

# ========================
# Clutch games
# ========================
st.subheader("⏱️ Jogos decididos - Vitorias x Derrotas")

# Função para separar vitórias e derrotas do formato "x-y"
def split_record(record):
    try:
        w, l = map(int, record.split('-'))
        return w, l
    except:
        return 0, 0

# Separando vitórias e derrotas
three_w, three_l = split_record(team_data["ThreePTSOrLess"])
ten_w, ten_l = split_record(team_data["TenPTSOrMore"])

# Categorias e dados
categories = ["≤3 pts", "≥10 pts"]
wins = [three_w, ten_w]
losses = [three_l, ten_l]

# Criar gráfico de barras lado a lado
fig_clutch = go.Figure()
fig_clutch.add_trace(go.Bar(
    x=categories,
    y=wins,
    name="Vitórias",
    marker_color="#EC0A36"
))
fig_clutch.add_trace(go.Bar(
    x=categories,
    y=losses,
    name="Derrotas",
    marker_color="#F0A500"
))

fig_clutch.update_layout(
    barmode="group",
    title=f"{team_data['TeamName']} - Jogos decididos",
    yaxis_title="Quantidade de Jogos",
    xaxis_title="Margem de pontos",
)

st.plotly_chart(fig_clutch, use_container_width=True)


# ========================
# Performance por mês
# ========================
st.subheader("📅 Desempenho por mês")

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Separar vitórias e derrotas de cada mês
wins_per_month = []
losses_per_month = []

for m in months:
    record = team_data[m]  # formato "x-y"
    if isinstance(record, str) and "-" in record:
        w, l = map(int, record.split("-"))
    else:
        w, l = 0, 0  # caso não tenha jogo naquele mês
    wins_per_month.append(w)
    losses_per_month.append(l)

# Criar gráfico de barras agrupadas
fig_months = go.Figure(data=[
    go.Bar(name="Vitórias", x=months, y=wins_per_month, marker_color="#EC0A36"),
    go.Bar(name="Derrotas", x=months, y=losses_per_month, marker_color="#F0A500")
])

fig_months.update_layout(
    barmode="group",
    title="Vitórias e Derrotas por Mês",
    xaxis_title="Mês",
    yaxis_title="Jogos"
)

st.plotly_chart(fig_months, use_container_width=True)

# ========================
# Performance contra outras divisões
# ========================
st.subheader("🏀 Desempenho contra outras divisões")

# Função para separar vitórias e derrotas do formato "x-y"
def split_record(record):
    try:
        w, l = map(int, record.split('-'))
        return w, l
    except:
        return 0, 0

# Lista de divisões adversárias
div_cols = ["vsAtlantic","vsCentral","vsSoutheast","vsNorthwest","vsPacific","vsSouthwest"]

# Preparar dados de vitórias e derrotas
wins = []
losses = []
hover_texts = []

for col in div_cols:
    w, l = split_record(team_data[col])
    wins.append(w)
    losses.append(l)
    hover_texts.append(f"{w}-{l} (Divisão: {team_data['Division']})")

# Criar gráfico de barras lado a lado
fig_divisions = go.Figure()
fig_divisions.add_trace(go.Bar(
    x=div_cols,
    y=wins,
    name="Vitórias",
    marker_color="#EC0A36",
    text=[f"{w}" for w in wins],
    textposition="auto"
))
fig_divisions.add_trace(go.Bar(
    x=div_cols,
    y=losses,
    name="Derrotas",
    marker_color="#F0A500",
    text=[f"{l}" for l in losses],
    textposition="auto"
))

fig_divisions.update_layout(
    barmode="group",
    title=f"{team_data['TeamName']} - Desempenho contra cada divisão",
    yaxis_title="Jogos",
    xaxis_title="Divisão adversária",
    hovermode="x"
)

st.plotly_chart(fig_divisions, use_container_width=True)


if st.button("⬅️ Voltar para Home"):
    st.switch_page("app.py")