# -*- coding: utf-8 -*-
"""
This module defines the Weather Location model, which stores geographical locations
for which weather data can be fetched.
"""

import requests
from odoo import models, fields
from odoo.exceptions import UserError

class WeatherLocation(models.Model):
    """
    Represents a geographical location for weather forecasting.

    Each location is defined by a name, latitude, and longitude. It also holds
    a history of weather data fetched for it.
    """
    _name = 'weather.location'
    _description = 'Weather Location'

    name = fields.Char(string='Location Name', required=True, help="The name of the location (e.g., a city).")
    latitude = fields.Float(string='Latitude', digits=(10, 7), required=True, help="The latitude of the location.")
    longitude = fields.Float(string='Longitude', digits=(10, 7), required=True, help="The longitude of the location.")
    weather_data_ids = fields.One2many('weather.data', 'location_id', string='Weather History', readonly=True, help="A history of weather data records for this location.")

    def get_weather_data(self):
        """
        Fetches the current weather data for the location(s) from the Open-Meteo API.

        This method iterates over a recordset of locations, makes an API call
        for each, and creates a new `weather.data` record with the fetched information.

        It handles potential network errors and API errors gracefully.

        Returns:
            bool: Always returns True.

        Raises:
            UserError: If the API call fails for a location, it raises an error
                       to inform the user.
        """
        for location in self:
            # Construct the API URL with the location's coordinates.
            url = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current_weather=true"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
                data = response.json()

                current_weather = data.get('current_weather')
                if current_weather:
                    # Create a new weather.data record with the API response.
                    self.env['weather.data'].create({
                        'location_id': location.id,
                        'time': current_weather.get('time'),
                        'temperature': current_weather.get('temperature'),
                        'windspeed': current_weather.get('windspeed'),
                        'winddirection': current_weather.get('winddirection'),
                        'weathercode': current_weather.get('weathercode'),
                    })
            except requests.exceptions.RequestException as e:
                # If the request fails, inform the user with a specific error message.
                raise UserError(f"Could not fetch weather data for {location.name}: {e}")
        return True
