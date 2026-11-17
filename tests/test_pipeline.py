import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_samples import simulate, store_samples
from src.public_db_integration import cross_reference, validate_cross_reference


def test_at_least_800_samples():
    df = simulate()
    assert len(df) >= 800


def test_samples_store_in_sqlite(tmp_path):
    df = simulate()
    db_path = str(tmp_path / "test.db")
    store_samples(df, db_path)
    assert os.path.exists(db_path)


def test_cross_reference_adds_4_database_fields():
    df = simulate()
    cross_ref = cross_reference(df)
    for col in ["chromosome", "pathway", "disease", "drug"]:
        assert col in cross_ref.columns


def test_cross_reference_coverage_is_complete_for_known_genes():
    df = simulate()
    cross_ref = cross_reference(df)
    validation = validate_cross_reference(cross_ref)
    assert validation["pct_with_chromosome"] == 100.0
    assert validation["pct_with_pathway"] == 100.0
    assert validation["pct_with_disease"] == 100.0


def test_flask_api_endpoints_respond(tmp_path):
    df = simulate()
    db_path = str(tmp_path / "test.db")
    store_samples(df, db_path)

    import app as app_module
    app_module.DB_PATH = db_path
    client = app_module.app.test_client()

    assert client.get("/api/qc_summary").status_code == 200
    assert client.get("/api/gene_counts").status_code == 200
    assert client.get("/api/samples/NOT-REAL").status_code == 404
