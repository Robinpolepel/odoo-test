# -*- coding: utf-8 -*-
{
    'name': 'School Management',
    'summary': 'Manage teachers, students, classes, and billing',
    'version': '16.0.1.0.0',
    'author': 'Your Company',
    'website': 'https://www.example.com',
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'report/teacher_report_templates.xml',
        'report/teacher_report.xml',
        'views/teacher_views.xml',
        'views/class_views.xml',
        'views/student_views.xml',
        'views/invoice_views.xml',
        'views/menuitems.xml',
    ],
    'application': True,
    'installable': True,
}
