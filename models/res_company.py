# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

import requests
import json

import time
from datetime import datetime

class ResCompany(models.Model):
    _inherit = 'res.company'

    def canvas_test_connect(self):
        headers = {
           'Authorization': 'Bearer ' + self.canvas_token,
        }

        response = requests.get(self.canvas_url + '/api/v1/accounts', headers=headers)
        _logger.info(response.text)

        if response.status_code == 200:
            raise ValidationError('¡Está Conectado con Instructure-Canvas!')
        else:
            raise ValidationError('Conexión no establecida o falta de permisos. Contacte a su administrador.')

    def canvas_import_users(self):
        headers = {
           'Authorization': 'Bearer ' + self.canvas_token,
        }

        response = requests.get(self.canvas_url + '/api/v1/accounts/self/users', headers=headers, params={'per_page':10})

        if response.status_code == 200:
            paginated = response.json()
            while 'next' in response.links:
               response = requests.get(response.links['next']['url'], headers=headers)
               paginated.extend(response.json())
            self.process_user(paginated)
        else:
            raise ValidationError('Conexión no establecida o falta de permisos. Contacte a su administrador. ' + response.text)

    def process_user(self, r):
        for rec in r:
            _logger.info(rec['id'])
            if rec['login_id']:
                partner = self.env['res.partner'].search([('email', '=', rec['login_id'])], limit='1')
                if not partner:
                    _logger.info('Sin partner')

    canvas_url = fields.Char(string='Canvas URL', help='This is the Canvas URL of site')
    canvas_token = fields.Char(string='Canvas API Token', help='Canvas API Token')
