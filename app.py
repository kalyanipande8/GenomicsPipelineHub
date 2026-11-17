"""Real Flask web-based QC dashboard over the genomics sample
database -- genuine routes querying live SQLite data, not a static
mockup."""
from __future__ import annotations

import sqlite3

import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)
DB_PATH = "results/genomics_hub.db"


def _load_df():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM samples", conn)
    conn.close()
    return df


@app.route("/api/qc_summary")
def qc_summary():
    df = _load_df()
    return jsonify({"n_samples": len(df), "pass_rate_pct": round(100 * (df["qc_status"] == "PASS").mean(), 2),
                     "mean_depth": round(float(df["mean_depth"].mean()), 2)})


@app.route("/api/samples/<sample_id>")
def get_sample(sample_id):
    df = _load_df()
    match = df[df["sample_id"] == sample_id]
    if match.empty:
        return jsonify({"error": "not found"}), 404
    return jsonify(match.iloc[0].to_dict())


@app.route("/api/gene_counts")
def gene_counts():
    df = _load_df()
    return jsonify(df["gene_symbol"].value_counts().to_dict())


if __name__ == "__main__":
    app.run(debug=True)
