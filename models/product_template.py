# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

import requests
import json

import time
from datetime import datetime

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def update_to_canvas(self):
        _logger.info('Actualizando Curso en Canvas')
        company = self.env.user.company_id
        headers = {
            'Authorization': 'Bearer ' + company.canvas_token,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'course[name]=' + self.name

        response = requests.put(company.canvas_url + '/api/v1/courses/' + str(self.canvas_id), headers=headers, data=data)

    is_canvas_course = fields.Boolean('Es un Curso Canvas')
    canvas_id = fields.Integer('Canvas ID')
