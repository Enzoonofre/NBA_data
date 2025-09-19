import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import pprint

def load_all_teams():
    df = pd.DataFrame(teams.get_teams())
    file_path="C:/Users/enzoo/OneDrive/NBA_DATA/data/raw/data_all_teams.csv"

    df.to_csv(file_path, index = False)

    print(f"Arquivos dos times salvos com sucesso em: {file_path}")

def load_teams_statistics():
    standings = leaguestandings.LeagueStandings(season='2023-24').get_data_frames()[0]

    file_path = "C:/Users/enzoo/OneDrive/NBA_DATA/data/raw/data_all_teams_23-24_season.csv"
    standings.to_csv(file_path, index = False)

    print(f"Arquivos não limpos das estatísticas gerais dos times salvos com sucesso em: {file_path}")


def load_clean_teams_statistics():
    standings = pd.read_csv("C:/Users/enzoo/OneDrive/NBA_DATA/data/raw/data_all_teams_23-24_season.csv")

    performance_standings = pd.DataFrame()
    performance_standings = standings[
        ['WINS', 'LOSSES', 'WinPCT', 'DivisionRank', 'HOME', 'ROAD', 'ThreePTSOrLess', 'TenPTSOrMore', 'LongWinStreak',
         'LongLossStreak', 'PointsPG', 'OppPointsPG', 'DiffPointsPG', 'vsEast', 'vsAtlantic', 'vsCentral',
         'vsSoutheast', 'vsWest', 'vsNorthwest', 'vsPacific', 'vsSouthwest', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]

    reference_standings = pd.DataFrame()
    reference_standings = standings[
        ['LeagueID', 'SeasonID', 'TeamID', 'TeamCity', 'TeamName', 'Conference', 'Division']]

    clean_standings = pd.concat([reference_standings, performance_standings], axis=1)

    file_path = "C:/Users/enzoo/OneDrive/NBA_DATA/data/processed/data_all_teams_23-24_season.csv"

    clean_standings.to_csv(file_path, index=False)
    print(f"Arquivos limpos das estatísticas dos times salvos com sucesso em: {file_path}")

load_all_teams()
load_teams_statistics()
load_clean_teams_statistics()