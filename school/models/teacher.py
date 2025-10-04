from odoo import api, fields, models, _

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'
    _order = 'name'

    name = fields.Char(required=True)
    address = fields.Text()
    phone = fields.Char(required=True)
    email = fields.Char()
    active = fields.Boolean(default=True)
    class_ids = fields.One2many('school.classroom', 'teacher_id', string='Classes')
    student_ids = fields.One2many('school.student', 'teacher_id', string='Students', readonly=True)
    student_count = fields.Integer(compute='_compute_student_count', store=True)
    note = fields.Html()

    _sql_constraints = [
        ('teacher_phone_unique', 'unique(phone)', 'Teacher phone number must be unique.'),
    ]

    @api.depends('student_ids', 'student_ids.active')
    def _compute_student_count(self):
        for teacher in self:
            students = teacher.student_ids.filtered('active')
            teacher.student_count = len(students)

    def action_activate_students(self):
        self.ensure_one()
        self.student_ids.filtered(lambda s: not s.active).write({'active': True})
        return True

    def action_deactivate_students(self):
        self.ensure_one()
        self.student_ids.filtered(lambda s: s.active).write({'active': False})
        return True

    def action_open_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Students'),
            'res_model': 'school.student',
            'view_mode': 'tree,form',
            'domain': [('teacher_id', '=', self.id)],
            'context': dict(self.env.context, default_teacher_id=self.id),
        }
