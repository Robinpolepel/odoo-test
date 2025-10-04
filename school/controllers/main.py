import json
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

class SchoolAPIController(http.Controller):

    def _authenticate_api_key(self):
        api_key = None
        auth_header = request.httprequest.headers.get('Authorization')
        if auth_header:
            scheme, _, token = auth_header.partition(' ')
            if scheme.lower() in {'bearer', 'apikey', 'api-key'}:
                api_key = token.strip()
        if not api_key:
            api_key = request.httprequest.headers.get('X-Api-Key')
        if not api_key:
            return None
        user_id = request.env['res.users.apikeys'].sudo()._check_credentials(scope='rpc', key=api_key)
        if not user_id:
            return None
        return request.env['res.users'].sudo().browse(user_id)

    def _unauthorized_response(self):
        return request.make_json_response({'error': 'Unauthorized'}, status=401)

    @http.route('/school/api/teachers', type='http', auth='public', methods=['GET'], csrf=False)
    def list_teachers(self, **kwargs):
        user = self._authenticate_api_key()
        if not user:
            return self._unauthorized_response()
        env = request.env(user=user)
        teachers = env['school.teacher'].search([])
        items = []
        for teacher in teachers:
            teacher_data = {
                'id': teacher.id,
                'name': teacher.name,
                'phone': teacher.phone,
                'address': teacher.address,
                'email': teacher.email,
                'student_count': teacher.student_count,
                'students': [
                    {
                        'id': student.id,
                        'name': student.name,
                        'class': student.class_id.name,
                        'active': student.active,
                    }
                    for student in teacher.student_ids
                ],
            }
            items.append(teacher_data)
        payload = {
            'count': len(items),
            'teachers': items,
        }
        return request.make_json_response(payload)

    @http.route('/school/api/students', type='json', auth='public', methods=['POST'], csrf=False)
    def create_student(self, **payload):
        user = self._authenticate_api_key()
        if not user:
            return self._unauthorized_response()
        env = request.env(user=user)
        payload = json.loads(request.httprequest.data)
        name = payload.get('name')
        class_id = payload.get('class_id')
        teacher_id = payload.get('teacher_id')
        if not name:
            return request.make_json_response({'error': 'Field "name" is required.'}, status=400)
        if not class_id and not teacher_id:
            return request.make_json_response({'error': 'Provide either "class_id" or "teacher_id".'}, status=400)

        student_vals = {'name': name}
        if payload.get('enrollment_date'):
            student_vals['enrollment_date'] = payload['enrollment_date']
        if payload.get('email'):
            student_vals['email'] = payload['email']
        if payload.get('phone'):
            student_vals['phone'] = payload['phone']
        if payload.get('tuition_fee') is not None:
            student_vals['tuition_fee'] = payload['tuition_fee']
        if payload.get('currency_id'):
            student_vals['currency_id'] = payload['currency_id']

        classroom = None
        teacher = None
        if class_id:
            classroom = env['school.classroom'].browse(int(class_id))
            if not classroom.exists():
                return request.make_json_response({'error': 'Class not found.'}, status=404)
            student_vals['class_id'] = classroom.id
        if teacher_id:
            teacher = env['school.teacher'].browse(int(teacher_id))
            if not teacher.exists():
                return request.make_json_response({'error': 'Teacher not found.'}, status=404)
            student_vals['teacher_id'] = teacher.id
        if classroom and teacher and classroom.teacher_id != teacher:
            return request.make_json_response({'error': 'Teacher does not teach the given class.'}, status=400)

        try:
            student = env['school.student'].create(student_vals)
        except ValidationError as exc:
            return request.make_json_response({'error': exc.name}, status=400)

        return request.make_json_response({
            'id': student.id,
            'name': student.name,
            'class_id': student.class_id.id if student.class_id else False,
            'teacher_id': student.teacher_id.id if student.teacher_id else False,
        }, status=201)
