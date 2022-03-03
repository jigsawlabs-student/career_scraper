pip3 install -r requirements.txt
`python3 manage.py get_card`




# generate the database

export FLASK_APP=src/__init__.py
create database career_scraper;
python3 -m flask db init
python3 flask db migrate -m "Initial migration."


For querying see the following
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/


See flask db library -> https://flask-migrate.readthedocs.io/en/latest/
# position
# company
# skills
# location

# https://medium.com/@sutharprashant199722/how-to-use-alembic-for-your-database-migrations-d3e93cacf9e8

# https://medium.datadriveninvestor.com/migrating-flask-script-to-flask-2-0-cli-4a5eee269139