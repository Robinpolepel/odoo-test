from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class SchoolInvoice(models.Model):
    _name = 'school.invoice'
    _description = 'Student Invoice'
    _order = 'billing_period desc, student_id'

    name = fields.Char(required=True)
    student_id = fields.Many2one('school.student', string='Student', required=True)
    teacher_id = fields.Many2one('school.teacher', string='Teacher', related='student_id.teacher_id', store=True, readonly=True)
    class_id = fields.Many2one('school.classroom', string='Class', related='student_id.class_id', store=True, readonly=True)
    amount = fields.Monetary(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    billing_period = fields.Date(string='Billing Period', required=True, default=lambda self: self._default_billing_period())
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
    ], default='draft')
    note = fields.Text()

    _sql_constraints = [
        (
            'unique_student_period',
            'unique(student_id, billing_period)',
            'A billing record already exists for this student and period.',
        ),
    ]

    @api.model
    def _default_billing_period(self):
        today = fields.Date.context_today(self)
        if isinstance(today, date):
            return today.replace(day=1)
        parsed = fields.Date.from_string(today)
        return parsed.replace(day=1)

    @api.model
    def create(self, vals):
        vals = dict(vals)
        student = None
        if vals.get('student_id'):
            student = self.env['school.student'].browse(vals['student_id'])
        period_date = self._normalize_period(vals.get('billing_period'))
        if period_date:
            vals['billing_period'] = period_date
        if not vals.get('name') and student and period_date:
            vals['name'] = '%s - %s' % (student.name, period_date.strftime('%B %Y'))
        if student and not vals.get('currency_id'):
            vals['currency_id'] = student.currency_id.id
        if period_date and not vals.get('due_date'):
            vals['due_date'] = period_date + relativedelta(days=14)
        if not vals.get('amount') and student:
            vals['amount'] = student.tuition_fee or 0.0
            if not vals.get('currency_id') and student.currency_id:
                vals['currency_id'] = student.currency_id.id
        return super().create(vals)

    def write(self, vals):
        vals = dict(vals)
        if 'billing_period' in vals:
            period_date = self._normalize_period(vals.get('billing_period'))
            vals['billing_period'] = period_date
            if period_date and 'due_date' not in vals:
                vals['due_date'] = period_date + relativedelta(days=14)
        return super().write(vals)

    @api.model
    def _normalize_period(self, period_value):
        if not period_value:
            return self._default_billing_period()
        if isinstance(period_value, str):
            period_date = fields.Date.from_string(period_value)
        else:
            period_date = period_value
        if isinstance(period_date, date):
            return period_date.replace(day=1)
        return period_date

    @api.model
    def cron_generate_monthly_invoices(self):
        period_date = self._default_billing_period()
        students = self.env['school.student'].search([('active', '=', True)])
        for student in students:
            existing = self.search([
                ('student_id', '=', student.id),
                ('billing_period', '=', period_date),
            ], limit=1)
            if existing:
                continue
            amount = student.tuition_fee or 0.0
            self.create({
                'student_id': student.id,
                'billing_period': period_date,
                'amount': amount,
                'currency_id': student.currency_id.id,
            })
        return True
