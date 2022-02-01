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
        _logger.info('Actualizando Usuario en Canvas')
        company = self.env.user.company_id
        headers = {
            'Authorization': 'Bearer ' + company.canvas_token,
        }

        files = {
            'user[name]': (None, self.name),
            'user[email]': (None, self.email),
        }

        response = requests.put(company.canvas_url + '/api/v1/users/' + str(self.canvas_id) + '.json', headers=headers, files=files)

    def create_in_canvas(self):
        raise ValidationError('Función no permitida')

    def link_course(self):
        if self.canvas_id != 0 and self.canvas_role != False:
            files = {
                'enrollment[user_id]': (None, str(self.canvas_id)),
                'enrollment[type]': (None, self.canvas_role),
            }

            if self.canvas_course_ids:
                for c in self.canvas_course_ids:
                    response = requests.post(company.canvas_url + '/api/v1/courses/' + str(c.canvas_id) + '/enrollments', files=files)

    canvas_id = fields.Integer('Canvas ID')
    canvas_role = fields.Selection([('StudentEnrollment', 'Estudiante'),('TeacherEnrollment', 'Docente'),('TaEnrollment', 'TA'),('DesignerEnrollment', 'Diseñador'),('ObserverEnrollment','Observador')], 'Canvas Rol')
    canvas_course_ids = fields.One2many(
        comodel_name='res.partner.course.line',
        inverse_name='res_partner_id',
    )


class CourseLinesPartner(models.Model):
    _name="res.partner.course.line"

    res_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Referencia Partner ID",
    )
    course = fields.Many2one(
        comodel_name="product.product",
        string="Cursos",
        required=True
    )
    is_canvas_course = fields.Boolean(string="Es Curso Canvas", related='course.is_canvas_course')
