FROM odoo:14.0

USER root


RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

USER odoo

