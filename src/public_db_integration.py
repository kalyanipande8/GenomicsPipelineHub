"""Real cross-referencing logic against 4 local reference tables
standing in for 4 public bioinformatics databases (gene info, pathway
membership, disease association, drug target) -- see README for the
disclosure that no live network calls to real public APIs are made
in this environment; the join/cross-reference logic itself is real."""
from __future__ import annotations

import pandas as pd

GENE_INFO_DB = pd.DataFrame({  # stand-in for NCBI Gene
    "gene_symbol": ["TP53", "BRCA1", "BRCA2", "EGFR", "KRAS"],
    "chromosome": ["17", "17", "13", "7", "12"],
})
PATHWAY_DB = pd.DataFrame({  # stand-in for KEGG
    "gene_symbol": ["TP53", "BRCA1", "BRCA2", "EGFR", "KRAS"],
    "pathway": ["p53 signaling", "DNA repair", "DNA repair", "MAPK signaling", "MAPK signaling"],
})
DISEASE_DB = pd.DataFrame({  # stand-in for ClinVar/OMIM
    "gene_symbol": ["TP53", "BRCA1", "BRCA2", "EGFR", "KRAS"],
    "disease": ["Li-Fraumeni syndrome", "Hereditary breast/ovarian cancer",
                "Hereditary breast/ovarian cancer", "NSCLC", "Colorectal cancer"],
})
DRUG_TARGET_DB = pd.DataFrame({  # stand-in for DrugBank
    "gene_symbol": ["EGFR", "KRAS"], "drug": ["Erlotinib", "Sotorasib"],
})


def cross_reference(samples: pd.DataFrame) -> pd.DataFrame:
    df = samples.merge(GENE_INFO_DB, on="gene_symbol", how="left") \
                .merge(PATHWAY_DB, on="gene_symbol", how="left") \
                .merge(DISEASE_DB, on="gene_symbol", how="left") \
                .merge(DRUG_TARGET_DB, on="gene_symbol", how="left")
    return df


def validate_cross_reference(df: pd.DataFrame) -> dict:
    return {"n_samples": len(df), "pct_with_chromosome": round(100 * df["chromosome"].notna().mean(), 2),
            "pct_with_pathway": round(100 * df["pathway"].notna().mean(), 2),
            "pct_with_disease": round(100 * df["disease"].notna().mean(), 2),
            "pct_with_drug_target": round(100 * df["drug"].notna().mean(), 2)}
