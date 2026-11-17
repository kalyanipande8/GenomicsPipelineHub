"""Simulate 820 NGS sample processing results, stored in a real
SQLite database -- the central data store this hub's web dashboard
and public-database cross-referencing query."""
from __future__ import annotations

import sqlite3

import numpy as np
import pandas as pd

N_SAMPLES = 820
SEED = 1049


def simulate(n: int = N_SAMPLES, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "sample_id": [f"NGS-{i:05d}" for i in range(n)],
        "gene_symbol": rng.choice(["TP53", "BRCA1", "BRCA2", "EGFR", "KRAS"], n),
        "variant_count": rng.poisson(12, n), "mean_depth": np.round(rng.normal(80, 15, n), 1),
        "qc_status": rng.choice(["PASS", "FAIL"], n, p=[0.93, 0.07]),
    })


def store_samples(df: pd.DataFrame, db_path: str):
    conn = sqlite3.connect(db_path)
    df.to_sql("samples", conn, if_exists="replace", index=False)
    conn.close()


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
