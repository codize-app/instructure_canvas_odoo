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
        raise ValidationError('Testing Canvas')

    def canvas_import_users(self):
        raise ValidationError('Importar Usuarios')

    canvas_url = fields.Char(string='Canvas URL', help='This is the Canvas URL of site')
    canvas_token = fields.Char(string='Canvas API Token', help='Canvas API Token')