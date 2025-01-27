"""This script performs queries for high entropy alloy materials to all OPTIMADE APIs."""

if __name__ == "__main__":
    import json

    import pandas as pd
    from optimade.client import OptimadeClient
    from rich.console import Console
    from rich.table import Table

    console = Console()

    download_structures = False

    client = OptimadeClient()

    has_any_filter = """\
elements HAS ANY "Mn", "Cr", "Fe", "Co", "Ni", "Cu", "Ag", "W", "Mo", "Nb", "Al", "Cd", "Sn", "Pb", "Bi", "Zn", "Ge", "Si", "Sb", "Mg" \
AND \
NOT elements HAS ANY "B", "C", "Cl", "F", "H", "N", "O", "S", "Se" \
AND \
nelements >= 5\
""".strip()

    has_any_results = client.count(filter=has_any_filter)

    df = pd.DataFrame.from_dict(
        has_any_results["structures"][has_any_filter],
        orient="index",
        columns=["count"],
        dtype=int,
    )
    df.to_markdown("results_count_table.md")

    table = Table(title="Number of OPTIMADE Query Results")
    table.add_column("Number of structures")
    table.add_column("Database URL")
    for url, count in df["count"].items():
        try:
            count = str(int(count))
        except:
            count = str(count)
        table.add_row(url, count)
    console.print(table)

    json.dump(has_any_results, open("data/has_any_hea_counts.json", "w"), indent=2)

    if download_structures:

        has_any_structures = client.get(
            filter=has_any_filter.strip(),
            response_fields=[
                "chemical_formula_reduced",
                "nsites",
                "cartesian_site_positions",
                "elements",
                "lattice_vectors",
            ],
            # save_as="data/hea_structures.json",
        )
