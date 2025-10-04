from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _order = 'name'

    name = fields.Char(required=True)
    teacher_id = fields.Many2one('school.teacher', string='Teacher')
    class_id = fields.Many2one('school.classroom', string='Class')
    enrollment_date = fields.Date(default=fields.Date.context_today)
    active = fields.Boolean(default=True)
    email = fields.Char()
    phone = fields.Char()
    tuition_fee = fields.Monetary(string='Tuition Fee', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    notes = fields.Text()

    @api.onchange('class_id')
    def _onchange_class_id(self):
        for student in self:
            student.teacher_id = student.class_id.teacher_id if student.class_id else False

    @api.model_create_multi
    def create(self, vals_list):
        classroom_model = self.env['school.classroom']
        for vals in vals_list:
            class_id = vals.get('class_id')
            teacher_id = vals.get('teacher_id')
            if class_id and not teacher_id:
                classroom = classroom_model.browse(class_id)
                if classroom and classroom.teacher_id:
                    vals['teacher_id'] = classroom.teacher_id.id
        students = super().create(vals_list)
        return students

    def write(self, vals):
        res = super().write(vals)
        if 'class_id' in vals and 'teacher_id' not in vals:
            for student in self:
                if student.class_id and student.class_id.teacher_id:
                    student.teacher_id = student.class_id.teacher_id
        return res

    @api.constrains('class_id', 'teacher_id')
    def _check_teacher_matches_class(self):
        for student in self:
            if student.class_id and student.teacher_id and student.class_id.teacher_id != student.teacher_id:
                raise ValidationError(_('The selected teacher must teach the selected class.'))
