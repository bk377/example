# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestWeatherReport(TransactionCase):

    def setUp(self):
        super(TestWeatherReport, self).setUp()
        self.WeatherLocation = self.env['weather.location']
        self.WeatherData = self.env['weather.data']
        self.WeatherReport = self.env['weather.report']

        self.test_location = self.WeatherLocation.create({
            'name': 'Test Report City',
            'latitude': 50.0,
            'longitude': 10.0,
        })

        self.WeatherData.create([{
            'location_id': self.test_location.id,
            'time': '2023-01-01T10:00',
            'temperature': 12.0,
            'windspeed': 5.0,
            'winddirection': 180.0,
            'weathercode': 2,
        }, {
            'location_id': self.test_location.id,
            'time': '2023-01-01T11:00',
            'temperature': 10.0,
            'windspeed': 6.0,
            'winddirection': 190.0,
            'weathercode': 3,
        }, {
            'location_id': self.test_location.id,
            'time': '2023-01-01T12:00',
            'temperature': 14.0,
            'windspeed': 4.0,
            'winddirection': 170.0,
            'weathercode': 1,
        }])

    def test_report_calculations(self):
        report_wizard = self.WeatherReport.create({
            'location_id': self.test_location.id,
        })
        self.assertEqual(report_wizard.min_temp, 10.0)
        self.assertEqual(report_wizard.max_temp, 14.0)
        self.assertEqual(report_wizard.avg_temp, 12.0)

    def test_print_report_action(self):
        report_wizard = self.WeatherReport.create({
            'location_id': self.test_location.id,
        })
        action = report_wizard.print_report()
        self.assertIn('report_type', action)
        self.assertEqual(action['report_type'], 'ir.actions.report')
