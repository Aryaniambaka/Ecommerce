when ever creating alembic for first time import base from app.model do not from db as it need model access
targetmetadata=Base.metadata
alembic revision --autogenerate -m "feat: create initial user and habit tables"
pip install psycopg2-binary must be pre downloaded
in alembicinit we need to put sql link but rnv file wont work so we do config.set_main_option("sqlalchemy.url", settings.DEV_DB)
postgresql	PostgreSQL server	✅ Yes
postgresql-client	psql command-line client	✅ Yes
postgresql-contrib	Extra extensions (e.g., uuid-ossp, pg_trgm)	⭐ Recommended
libpq-dev	PostgreSQL development headers (needed by some Python packages)	⭐ Recommended
python3-dev	Python headers for compiling extensions	⭐ Recommended
pip install sqlalchemy psycopg2-binary alembic
sudo -u postgres psql
psql -U postgres -h localhost
cd /etc/systemd/system nano servicr name 

sudo systemctl daemon-reload
sudo systemctl enable ecommerce
sudo systemctl start ecommerce
cd /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/sudo nginx -t
sudo systemctl enable nginx
sudo rm /etc/nginx/sites-enabled/default
sudo certbot --nginx -d aryanapi.mooo.com
nano /etc/postgresql/16/main/pg_hba.conf /etc/postgresql/16/main/postgresql.conf sudo nano /etc/systemd/system/ecommerce.service sudo systemctl enable ecommerce sudo nano /etc/nginx/sites-available/ecommerce