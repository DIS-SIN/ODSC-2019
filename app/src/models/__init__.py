from typing import Optional
from flask import Flask

def init_base(app: Optional[Flask] = None, db_path: Optional[str] = None):
    from neomodel import config
    if app is not None:
        config.DATABASE_URL = app.config["NEOMODEL_DATABASE_URI"]
    elif db_path is not None:
        config.DATABASE_URL = db_path
    
