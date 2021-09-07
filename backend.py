import os
import json
from model import participants as part
DATABASE_PATH = os.path.join(os.path.abspath("."), r"database.conf")


class Backend:
    def __init__(self):
        with open(DATABASE_PATH, "r") as f:
            self.data = json.load(f)
        # self.