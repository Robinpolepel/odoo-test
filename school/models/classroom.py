from odoo import models, fields

class SchoolClassroom(models.Model):
    _name = 'school.classroom'
    _description = 'Classroom'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char()
    teacher_id = fields.Many2one('school.teacher', string='Teacher', required=True)
    student_ids = fields.One2many('school.student', 'class_id', string='Students')
    schedule = fields.Char()
    capacity = fields.Integer()

    def write(self, vals):
        res = super().write(vals)
        if 'teacher_id' in vals:
            for classroom in self:
                if classroom.student_ids:
                    classroom.student_ids.write({'teacher_id': classroom.teacher_id.id})
        return res
