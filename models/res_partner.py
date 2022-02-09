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
        company = self.env.user.company_id
        if self.email:
            headers = {
                'Authorization': 'Bearer ' + company.canvas_token,
            }

            files = {
                'user[name]': (None, self.name),
                'pseudonym[unique_id]': (None, self.email),
                'pseudonym[sis_user_id]': (None, self.email)
            }
            response = requests.post(company.canvas_url + '/api/v1/accounts/1/users', files=files, headers=headers)
            _logger.info(response.text)
            _logger.info(response)
            if response.status_code == 200:
                _logger.info(response.text)
                self.canvas_id = response.json()['id']
            else:
                raise ValidationError('Error ' + str(response.text))
        else:
            raise ValidationError('El Usuario debe tener un Mail')

    def link_course(self):
        company = self.env.user.company_id
        if self.canvas_id != 0 and self.canvas_role != False:
            headers = {
                'Authorization': 'Bearer ' + company.canvas_token,
            }
            files = {
                'enrollment[user_id]': (None, str(self.canvas_id)),
                'enrollment[type]': (None, self.canvas_role),
                'enrollment[notify]': (None, True)
            }

            if self.canvas_course_ids:
                for c in self.canvas_course_ids:
                    if c.course.canvas_id:
                        response = requests.post(company.canvas_url + '/api/v1/courses/' + str(c.course.canvas_id) + '/enrollments', files=files, headers=headers)
                        if response.status_code != 200:
                            raise ValidationError('Error ' + str(response.text))

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
