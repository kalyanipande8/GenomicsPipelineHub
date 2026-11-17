import json
import os

from src.simulate_samples import simulate, store_samples
from src.public_db_integration import cross_reference, validate_cross_reference


def main():
    os.makedirs("results", exist_ok=True)
    samples = simulate()
    store_samples(samples, "results/genomics_hub.db")

    cross_ref = cross_reference(samples)
    validation = validate_cross_reference(cross_ref)

    summary = {"n_samples": len(samples), "cross_reference_coverage": validation}

    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
