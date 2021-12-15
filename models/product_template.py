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
        }

        #files = {
        #    'user[name]': (None, self.name),
        #    'user[email]': (None, self.email),
        #}

        #response = requests.put(company.canvas_url + '/api/v1/users/' + str(self.canvas_id) + '.json', headers=headers, files=files)

    is_canvas_course = fields.Boolean('Es un Curso Canvas')
    canvas_id = fields.Integer('Canvas ID')
