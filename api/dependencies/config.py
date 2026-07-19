import os


class conf:
    db_host = "localhost"
    db_name = "mammoth_3155"
    db_port = 3306
    db_user = "mammoth_app"
    db_password = os.getenv("MAMMOTH_DB_PASSWORD", "")
    app_host = "localhost"
    app_port = 8000
