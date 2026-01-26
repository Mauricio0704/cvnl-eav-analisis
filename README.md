# CVNL Survey ETL

This repository provides the ETL pipeline for CVNL's ["Encuesta Así Vamos"](https://comovamosnl.org/encuesta-asi-vamos/) survey results. It performs ingestion, cleaning/transformations, and loads a cleaned, analysis-ready database.

**Goals:**
- Provide a repeatable ETL that produces a cleaned, documented database
- Ensure processed datasets and disaggregations are stored in `data/processed/` and loaded into `data/db/`

## Quick start

1. Create and activate a Python virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip3 install -e .
```

3. Run the full ETL for a given year (default 2025):

```bash
python3 run_etl.py --year 2025
```

The script will run extraction, transform, and load phases and produce a cleaned database under `data/db/` (or other configured location).

## Project layout

- `data/`
	- `source/` : original source (organized by year)
	- `raw/` : raw survey files (organized by year)
	- `processed/` : cleaned CSVs and JSON artifacts produced by the transform step
	- `db/` : resulting cleaned database files
- `src/` : application code (extraction, transformation, loading)

## Configuration

Project paths and survey-specific settings live in `src/config`.

## Data flow overview


1. Place original source exports (can be downloaded [here](https://comovamosnl.org/encuesta-asi-vamos/)) in `data/source/<year>/`.
2. Run `run_etl.py` to perform:
	- Extraction: read from `data/source/<year>/` and copy/prepare files into `data/raw/<year>/`
	- Transformation: clean data, expand disaggregations, derive variables, and write processed CSVs to `data/processed/`
	- Load: create or update the target database schema and load processed data into `data/db/`

The final product of the pipeline is a cleaned, analysis-ready database. Reporting and export workflows are maintained in a separate repository.


## Next steps

- Continue adding support for additional survey years under `data/raw/<year>/`.
- Add automated tests for cleaning and mapping logic.
- For reporting/export work, consult the dedicated [reporting repository](https://github.com/Mauricio0704/encuesta-asi-vamos-survey-reporting).