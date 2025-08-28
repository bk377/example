# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WeatherReport(models.TransientModel):
    _name = 'weather.report'
    _description = 'Weather Report'

    location_id = fields.Many2one('weather.location', string='Location', required=True)
    avg_temp = fields.Float(string='Average Temperature', compute='_compute_stats')
    min_temp = fields.Float(string='Min Temperature', compute='_compute_stats')
    max_temp = fields.Float(string='Max Temperature', compute='_compute_stats')

    @api.depends('location_id.weather_data_ids.temperature')
    def _compute_stats(self):
        for report in self:
            weather_data = report.location_id.weather_data_ids
            if weather_data:
                temperatures = weather_data.mapped('temperature')
                if temperatures:
                    report.avg_temp = sum(temperatures) / len(temperatures)
                    report.min_temp = min(temperatures)
                    report.max_temp = max(temperatures)
                else:
                    report.avg_temp = 0
                    report.min_temp = 0
                    report.max_temp = 0
            else:
                report.avg_temp = 0
                report.min_temp = 0
                report.max_temp = 0

    def print_report(self):
        self.ensure_one()
        return self.env.ref('example.action_report_weather').report_action(self)
