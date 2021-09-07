import json
import os

# abs path to /.../tradingbot/helpers/spreadsheet_snippets.py
abs_path = os.path.dirname(__file__)
# abs to project root folder /.../tradingbot/
root_path = abs_path[:abs_path.find('helpers')].strip()
# abs to credentials folder
creds_path = os.path.join(root_path, 'credentials')
# abs to historical_data folder
historicals_path = os.path.join(root_path, 'historical_data')