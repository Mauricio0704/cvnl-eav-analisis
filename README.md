# CVNL Survey Analysis

This repository contains the data ingestion, transformation, and reporting pipeline for CVNL's ["Encuesta Así Vamos"](https://comovamosnl.org/encuesta-asi-vamos/) survey results. The final reports produced by this pipeline serve as the analytical foundation for the annual *Encuesta Así Vamos* magazine, where insights and visualizations are created to communicate findings based on statistically representative responses from citizens across Nuevo León.

**Goals:**
- Provide repeatable ETL for survey data
- Produce cleaned, documented datasets and disaggregations
- Enable reproducible reporting and exports

**Contents:**
- Data ingestion and cleaning: `src/ingestion`, `src/cleaning`, `src/mapping`
- Database schema and loaders: `src/db`
- Reporting and exports: `src/reporting`, `src/io`
- Top-level scripts: `scripts/run_ingestion.py`, `scripts/run_db_load.py`, `scripts/run_report.py`

## Quick start

1. Create and activate a Python virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies. This project uses `pyproject.toml`; install via pip or your preferred tool:

```bash
pip3 install -e .
```

3. Run ingestion, load, and report scripts:

```bash
# Ingest raw files and produce cleaned CSVs
python3 -m scripts.run_ingestion

# Create DB schema and load processed data into the database
python3 -m scripts.run_db_load

# Build reports / exports from the loaded data
python3 -m scripts.run_report
```

## Project layout

- `data/`
	- `raw/` : raw survey files (organized by year)
	- `processed/` : cleaned CSVs and JSON artifacts used for loading and reporting
	- `db/` : database files
- `scripts/` : top-level runner scripts for ingest, DB load, and report
- `src/` : primary application code
	- `src/cleaning` : cleaning and transformation logic for survey, household, and disaggregation data
	- `src/ingestion` : orchestration for ingesting raw files into the processing pipeline
	- `src/mapping` : schema normalization, block extraction, derived variables, disaggregation expansion
	- `src/db` : repository pattern, schema creation, and data loaders
	- `src/io` : CSV/JSON export utilities and helpers
	- `src/reporting` : report builder and table extension utilities
	- `src/utils` : database connectors and helpers

## Configuration

Project paths and survey-specific settings live in `src/config`. 

## Data flow overview

1. Raw files are placed in `data/raw/<year>/`.
2. `scripts/run_ingestion.py` runs ingestion that normalizes schemas, extracts blocks, and writes cleaned CSVs into `data/processed/`.
3. `scripts/run_db_load.py` creates the target schema (if needed) and loads processed CSVs into the database using `src/db/load_data.py`.
4. `scripts/run_report.py` builds reporting tables and exports disaggregations using `src/reporting` and `src/io`.

## Next steps

- Implement full support for all survey years present under `data/raw/<year>/` that are not yet fully integrated, including schema compatibility, data ingestion, database loading, and reporting/exports.
- Add automated tests for cleaning and mapping logic.
