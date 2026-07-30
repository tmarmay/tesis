"""Convierte el dump de PostgreSQL run_results.sql a una base sqlite en thesis/database/.

Uso:
    python scripts/build_results_db.py
"""
import re
import sqlite3
from io import StringIO
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "run_results.sql"
DST = ROOT / "thesis" / "database" / "run_results.sqlite"

COPY_RE = re.compile(r"COPY public\.run_results \((.+?)\) FROM stdin;\n(.*?)\\\.", re.DOTALL)


def main():
    sql = SRC.read_text()
    match = COPY_RE.search(sql)
    columns = [c.strip() for c in match.group(1).split(",")]
    data = match.group(2)

    df = pd.read_csv(StringIO(data), sep="\t", names=columns, na_values=["\\N"])

    for col in ("feasible", "valid"):
        if col in df.columns:
            df[col] = df[col].map({"t": True, "f": False, True: True, False: False})

    DST.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DST)
    df.to_sql("run_results", conn, if_exists="replace", index=False)
    conn.execute("CREATE INDEX idx_run_results_experiment_id ON run_results(experiment_id)")
    conn.execute("CREATE INDEX idx_run_results_solver ON run_results(solver)")
    conn.commit()
    conn.close()

    print(f"{DST} generado con {len(df)} filas")


if __name__ == "__main__":
    main()
