from os import environ

if "MAPSEARCH_INSTANCE_URL" in environ:
    MAPSEARCH_INSTANCE_URL = environ["MAPSEARCH_INSTANCE_URL"]
else:
    MAPSEARCH_INSTANCE_URL = "http://localhost:5000/mapsearch"
