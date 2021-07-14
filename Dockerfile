FROM odoo:14.0

USER root

COPY . /mnt/extra-addons/example
COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

USER odoo

