# -*- coding: utf-8 -*-

import requests
from odoo import models, fields, api


class example(models.Model):
    _name = 'example.example'
    _description = 'example.example'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    text = fields.Char(compute="_compute_text")
    text2 = fields.Char()

    @api.depends('name')
    def _compute_text(self):
        txt = requests.get('https://raw.githubusercontent.com/Julian/jsonschema/main/json/package.json').json().get('name')
        for record in self:
            record.text = '%s = %s' % (str(record.name), txt)

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
