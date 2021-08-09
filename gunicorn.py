import os

bind = "0.0.0.0:8000"
reload = os.environ.get("DEBUG") == "True"
loglevel = os.environ.get("LOG_LEVEL", "INFO")
workers = int(os.environ.get("WORKERS", 1))
accesslog = "-"