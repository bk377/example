FROM odoo:14.0

USER root

COPY . /mnt/extra-addons/example
COPY requirements.txt requirements.txt

USER odoo

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

ENV DB_NAME test

RUN python3 moduler_updater.py 

