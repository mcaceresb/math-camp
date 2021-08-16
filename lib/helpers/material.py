from pathlib import Path
import json

MATERIAL_FILE = Path(__file__).resolve().parent / 'material.json'

material = json.loads(open(MATERIAL_FILE).read())
