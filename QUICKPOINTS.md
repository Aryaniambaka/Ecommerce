when ever creating alembic for first time import base from app.model do not from db as it need model access
targetmetadata=Base.metadata
alembic revision --autogenerate -m "feat: create initial user and habit tables"
pip install psycopg2-binary must be pre downloaded
in alembicinit we need to put sql link but rnv file wont work so we do config.set_main_option("sqlalchemy.url", settings.DEV_DB)