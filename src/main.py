import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import os

def load_all_teams():
    df = pd.DataFrame(teams.get_teams())
    file_path="data/raw/data_all_teams.csv"

    df.to_csv(file_path, index = False)

    print(f"Arquivos dos times salvos com sucesso em: {file_path}")


def load_all_teams_statistics():
    year = [str(y) for y in range(2010, 2025)]
    standings_by_year = {}

    for y in year:
        standings = leaguestandings.LeagueStandings(season=y).get_data_frames()[0]
        standings_by_year[y] = standings  # salva no dicionário

        # cria o caminho do arquivo com o ano
        file_path = f"data/raw/data_all_teams_{y}-seasons.csv"

        # salva o CSV
        standings.to_csv(file_path, index=False)


def load_clean_teams_statistics(raw_folder="data/raw", output_file="data/processed/data_all_teams_all_seasons.csv"):
    all_cleaned = []

    # percorre todos os arquivos CSV na pasta
    for file in os.listdir(raw_folder):
        if file.endswith(".csv") and file != "data_all_teams.csv":
            path = os.path.join(raw_folder, file)
            standings = pd.read_csv(path)

            performance_standings = standings[
                ['WINS', 'LOSSES', 'WinPCT', 'DivisionRank', 'HOME', 'ROAD', 'ThreePTSOrLess', 'TenPTSOrMore',
                 'LongWinStreak', 'LongLossStreak', 'PointsPG', 'OppPointsPG', 'DiffPointsPG', 'vsEast', 'vsAtlantic',
                 'vsCentral', 'vsSoutheast', 'vsWest', 'vsNorthwest', 'vsPacific', 'vsSouthwest', 'Jan', 'Feb', 'Mar',
                 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            ]

            reference_standings = standings[
                ['LeagueID', 'SeasonID', 'TeamID', 'TeamCity', 'TeamName', 'Conference', 'Division']
            ]

            clean_standings = pd.concat([reference_standings, performance_standings], axis=1)

            all_cleaned.append(clean_standings)

    # junta tudo em um único DataFrame final
    final_df = pd.concat(all_cleaned, ignore_index=True)

    # salva o CSV final
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_df.to_csv(output_file, index=False)

    print(f"✅ Arquivos limpos de todas as temporadas salvos em: {output_file}")

load_all_teams()
load_all_teams_statistics()
load_clean_teams_statistics()