# -*- coding: utf-8 -*-
"""
Tests for the weather feature models and API calls.
"""

from unittest.mock import patch

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestWeather(TransactionCase):
    """Test suite for the Weather feature."""

    def setUp(self):
        """Set up test data."""
        super(TestWeather, self).setUp()
        self.WeatherLocation = self.env['weather.location']
        self.WeatherData = self.env['weather.data']

        self.test_location = self.WeatherLocation.create({
            'name': 'Test City',
            'latitude': 52.52,
            'longitude': 13.41,
        })

    def test_location_creation(self):
        """Test that a weather.location can be created."""
        self.assertEqual(self.test_location.name, 'Test City')
        self.assertEqual(self.test_location.latitude, 52.52)
        self.assertEqual(self.test_location.longitude, 13.41)

    @patch('odoo.addons.example.models.weather_location.requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Test successful fetching of weather data."""
        # Mock the API response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'current_weather': {
                'time': '2023-01-01T12:00',
                'temperature': 10.0,
                'windspeed': 5.5,
                'winddirection': 180.0,
                'weathercode': 3,
            }
        }

        # Call the method to be tested
        self.test_location.get_weather_data()

        # Check that the mock was called
        mock_get.assert_called_once_with(
            "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
        )

        # Check that a weather.data record was created
        weather_data = self.WeatherData.search([('location_id', '=', self.test_location.id)])
        self.assertEqual(len(weather_data), 1)
        self.assertEqual(weather_data.temperature, 10.0)
        self.assertEqual(weather_data.weathercode, 3)

    @patch('odoo.addons.example.models.weather_location.requests.get')
    def test_get_weather_data_failure(self, mock_get):
        """Test failed fetching of weather data."""
        # Mock a failed API response (e.g., a network error)
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Network Error")

        # Call the method and assert that it raises a UserError
        with self.assertRaises(UserError):
            self.test_location.get_weather_data()

        # Check that no weather.data record was created
        weather_data_count = self.WeatherData.search_count([('location_id', '=', self.test_location.id)])
        self.assertEqual(weather_data_count, 0)
