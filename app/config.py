from quart import Quart
import os

API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')

app = Quart(__name__)
