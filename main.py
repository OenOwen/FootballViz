from pathlib import Path
import pandas as pd

ARCHIVE_ROOT = Path("archive/understats")

def read_match_csv(csv_path: Path) -> pd.DataFrame:
    # Some leagues use commas, others semicolons; sniff header to pick the delimiter.
    with csv_path.open("r", encoding="utf-8") as f:
        header = f.readline()
    sep = ";" if header.count(";") > header.count(",") else ","
    return pd.read_csv(csv_path, sep=sep)

def load_match_data(root: Path = ARCHIVE_ROOT) -> dict[str, pd.DataFrame]:
    leagues: dict[str, pd.DataFrame] = {}
    for league_dir in root.iterdir():
        if not league_dir.is_dir():
            continue
        match_path = league_dir / "match_data.csv"
        if not match_path.exists():
            continue
        df = read_match_csv(match_path)
        if {"goals_h", "goals_a"}.issubset(df.columns):
            leagues[league_dir.name] = df
    return leagues

match_data = load_match_data()

avg_total_goals = {}
for league, df in match_data.items():
    total_goals = df["goals_h"] + df["goals_a"]
    avg_total_goals[league] = total_goals.mean()

print(avg_total_goals)
