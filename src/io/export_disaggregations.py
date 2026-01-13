import json

from src.config.paths import PROCESSED_DATA_DIR


def dissagregations_to_json(dissagregations: dict) -> None:
   file_path = PROCESSED_DATA_DIR / "disaggregations.json"

   with open(file_path, 'w') as json_file:
    json.dump(dissagregations, json_file, indent=4)    
    