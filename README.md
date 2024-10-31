# FastApi app to monitor/control the home
## Running instructions
FastApi server:
python3 -m venv .api-venv
pip3 install -r api-requirements.txt
source .api-venv/bin/activate
fastapi dev app/main.py

Pi Requirements:
python3 -m venv .pi-venv
pip3 install -r pi-requirements.txt

Create a .env in house-api directory eg.
MYSQL_USER=*username*
MYSQL_PASSWORD=*password*

RABBITMQ_USER=*username*
RABBITMQ_PASSWORD*password*
