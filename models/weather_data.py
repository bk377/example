# -*- coding: utf-8 -*-
"""
This module defines the Weather Data model, which stores the weather information
fetched from the API for a specific location and time.
"""

from odoo import models, fields

class WeatherData(models.Model):
    """
    Represents a single weather data point for a specific location and time.

    This model stores denormalized data from the weather API. The `_order`
    attribute ensures that by default, records are shown in descending
    chronological order.
    """
    _name = 'weather.data'
    _description = 'Weather Data'
    _order = 'time desc'

    location_id = fields.Many2one('weather.location', string='Location', required=True, ondelete='cascade', help="The location this weather data belongs to.")
    time = fields.Datetime(string='Time', required=True, help="The timestamp for this weather data point.")
    temperature = fields.Float(string='Temperature (°C)', help="The air temperature in degrees Celsius.")
    windspeed = fields.Float(string='Wind Speed (km/h)', help="The wind speed in kilometers per hour.")
    winddirection = fields.Float(string='Wind Direction (°)', help="The wind direction in degrees.")
    weathercode = fields.Integer(string='Weather Code', help="A code representing the weather conditions (e.g., clear, rain). See Open-Meteo documentation for details.")
