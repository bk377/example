# -*- coding: utf-8 -*-

from odoo import models, fields

class WeatherData(models.Model):
    _name = 'weather.data'
    _description = 'Weather Data'
    _order = 'time desc'

    location_id = fields.Many2one('weather.location', string='Location', required=True, ondelete='cascade')
    time = fields.Datetime(string='Time', required=True)
    temperature = fields.Float(string='Temperature (°C)')
    windspeed = fields.Float(string='Wind Speed (km/h)')
    winddirection = fields.Float(string='Wind Direction (°)')
    weathercode = fields.Integer(string='Weather Code')
