# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

import requests
import json

import time
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def update_to_canvas(self):
        raise ValidationError('Función no permitida')

    def create_in_canvas(self):
        raise ValidationError('Función no permitida')

    canvas_id = fields.Integer('Canvas ID')
    canvas_role = fields.Selection([('StudentEnrollment', 'Estudiante'),('TeacherEnrollment', 'Docente'),('TaEnrollment', 'TA'),('DesignerEnrollment', 'Diseñador'),('ObserverEnrollment','Observador')], 'Canvas Rol')
