FROM odoo:14.0

USER root

COPY . /mnt/extra-addons/example
COPY requirements.txt requirements.txt
COPY moduler_updater.py moduler_updater.py

USER odoo

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

ENV DB_NAME test

CMD ["python3", "moduler_updater.py", ";", "/entrypoint.sh", "odoo"]



