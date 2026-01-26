import argparse

from src.extract import main as extractor
from src.transform import main as transformer
from src.load import main as loader


def main(year: int = 2025):
    print(f"ETL started for year {year}")

    extractor.run(year)
    transformer.run(year)
    loader.run(year)

    print("ETL completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full ETL")
    parser.add_argument("--year", "-y", type=int, default=2025, help="Survey year to ingest (default: 2025)")
    args = parser.parse_args()

    main(args.year)
