# -*- coding: utf-8 -*-

import requests
from odoo import models, fields

class WeatherLocation(models.Model):
    _name = 'weather.location'
    _description = 'Weather Location'

    name = fields.Char(string='Location Name', required=True)
    latitude = fields.Float(string='Latitude', digits=(10, 7), required=True)
    longitude = fields.Float(string='Longitude', digits=(10, 7), required=True)
    weather_data_ids = fields.One2many('weather.data', 'location_id', string='Weather History')

    def get_weather_data(self):
        for location in self:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current_weather=true"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                current_weather = data.get('current_weather')
                if current_weather:
                    self.env['weather.data'].create({
                        'location_id': location.id,
                        'time': current_weather.get('time'),
                        'temperature': current_weather.get('temperature'),
                        'windspeed': current_weather.get('windspeed'),
                        'winddirection': current_weather.get('winddirection'),
                        'weathercode': current_weather.get('weathercode'),
                    })
            except requests.exceptions.RequestException:
                # In a real app, you would raise an Odoo UserError.
                # from odoo.exceptions import UserError
                # raise UserError(f"Could not fetch weather data: {e}")
                pass
        return True
