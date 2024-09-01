from dotenv import load_dotenv
import os

load_dotenv()

app_id = os.getenv("APIID")
app_hash = os.getenv("APIHASH")