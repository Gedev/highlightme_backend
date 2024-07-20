import os
import json
from django.conf import settings

def load_mock_data(file_name):
    file_path = os.path.join(settings.BASE_DIR, 'mock_data', file_name)
    with open(file_path, 'r') as file:
        return json.load(file)