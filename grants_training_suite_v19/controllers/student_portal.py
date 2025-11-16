# -*- coding: utf-8 -*-

import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

_logger = logging.getLogger(__name__)


class StudentPortal(CustomerPortal):
    """Student Portal Controller"""
    
    def _prepare_home_portal_values(self, counters):
        """Add student-related counters to portal home"""
        values = super()._prepare_home_portal_values(counters)
        
        if 'course_count' in counters:
            student = self._get_student_for_portal_user()
            if student:
                values['course_count'] = len(student.course_session_ids)
        
        return values
    
    def _get_student_for_portal_user(self):
        """Get student record for current portal user"""
        if not request.env.user or request.env.user._is_public():
            return False
        
        # Find student by email matching portal user email
        student = request.env['gr.student'].sudo().search([
            ('email', '=', request.env.user.email)
        ], limit=1)
        
        return student
    
    def _create_demo_student(self):
        """Create a demo student for testing"""
        student = request.env['gr.student'].sudo().create({
            'name': 'Demo Student',
            'name_english': 'John Demo Student',
            'name_arabic': 'طالب تجريبي',
            'email': 'demo.student@example.com',
            'phone': '+1234567890',
            'birth_date': '1995-05-15',
            'gender': 'male',
            'nationality': 'American',
            'native_language': 'English',
            'english_level': 'intermediate',
            'state': 'approved',
        })
        _logger.info('Created demo student: %s', student.name)
        return student
    
    def _create_demo_courses(self, student):
        """Create demo courses for student"""
        courses = request.env['gr.course.session'].sudo()
        
        # Create 3 demo course sessions
        course_data = [
            {'name': 'English Language Basics', 'status': 'completed', 'progress': 100},
            {'name': 'Advanced Communication Skills', 'status': 'in_progress', 'progress': 75},
            {'name': 'Business English', 'status': 'enrolled', 'progress': 30},
        ]
        
        for data in course_data:
            course = request.env['gr.course.session'].sudo().create({
                'name': data['name'],
                'student_id': student.id,
                'status': data['status'],
                'start_date': '2024-01-15',
                'end_date': '2024-12-15',
            })
            courses |= course
        
        _logger.info('Created %d demo courses for student %s', len(courses), student.name)
        return courses
    
    def _create_demo_certificates(self, student):
        """Create demo certificates for student"""
        certificates = request.env['gr.certificate'].sudo()
        
        # Create 2 demo certificates
        cert_data = [
            {
                'certificate_title': 'English Language Proficiency Certificate',
                'certificate_type': 'completion',
                'state': 'issued',
                'course_name': 'English Language Basics',
            },
            {
                'certificate_title': 'Advanced Communication Certificate',
                'certificate_type': 'achievement',
                'state': 'verified',
                'course_name': 'Advanced Communication Skills',
            },
        ]
        
        for data in cert_data:
            cert = request.env['gr.certificate'].sudo().create({
                'student_id': student.id,
                'certificate_title': data['certificate_title'],
                'certificate_type': data['certificate_type'],
                'state': data['state'],
                'course_name': data['course_name'],
                'issue_date': '2024-06-15',
                'valid_from': '2024-06-15',
                'valid_until': '2026-06-15',
                'certificate_description': f'Certificate of {data["certificate_type"]} for {data["course_name"]}',
            })
            certificates |= cert
        
        _logger.info('Created %d demo certificates for student %s', len(certificates), student.name)
        return certificates
    
    @http.route(['/my/student'], type='http', auth='public', website=True)
    def portal_my_student_dashboard(self, **kw):
        """Student dashboard - shows student info and enrolled courses - Public for testing"""
        if not request.env.user or request.env.user._is_public():
            # For public access, show demo student
            student = request.env['gr.student'].sudo().search([], limit=1)
            if not student:
                # Create demo student if none exists
                student = self._create_demo_student()
        else:
            student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        # Get demo courses and certificates if none exist
        courses = student.course_session_ids
        if not courses:
            courses = self._create_demo_courses(student)
        
        certificates = student.certificate_ids
        if not certificates:
            certificates = self._create_demo_certificates(student)
        
        values = {
            'page_name': 'student_dashboard',
            'student': student,
            'courses': courses,
            'progress': student.progress_percentage if hasattr(student, 'progress_percentage') else 75.0,
            'certificates': certificates,
        }
        
        return request.render('grants_training_suite_v19.portal_student_dashboard', values)
    
    @http.route(['/my/courses'], type='http', auth='public', website=True)
    def portal_my_courses(self, **kw):
        """List of enrolled courses for student - Public for testing"""
        if not request.env.user or request.env.user._is_public():
            student = request.env['gr.student'].sudo().search([], limit=1)
            if not student:
                student = self._create_demo_student()
        else:
            student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        sessions = student.course_session_ids
        if not sessions:
            sessions = self._create_demo_courses(student)
        
        values = {
            'page_name': 'my_courses',
            'student': student,
            'sessions': sessions,
        }
        
        return request.render('grants_training_suite_v19.portal_my_courses', values)
    
    @http.route(['/my/courses/<int:session_id>'], type='http', auth='public', website=True)
    def portal_course_detail(self, session_id, **kw):
        """Course session detail page - Public for testing"""
        if not request.env.user or request.env.user._is_public():
            student = request.env['gr.student'].sudo().search([], limit=1)
        else:
            student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        session = request.env['gr.course.session'].sudo().browse(session_id)
        
        # Skip verification for public access (testing)
        if not request.env.user._is_public() and session.student_id != student:
            return request.render('website.403')
        
        values = {
            'page_name': 'course_detail',
            'student': student,
            'session': session,
        }
        
        return request.render('grants_training_suite_v19.portal_course_detail', values)
    
    @http.route(['/my/certificates'], type='http', auth='public', website=True)
    def portal_my_certificates(self, **kw):
        """List of certificates for student - Public for testing"""
        if not request.env.user or request.env.user._is_public():
            student = request.env['gr.student'].sudo().search([], limit=1)
            if not student:
                student = self._create_demo_student()
        else:
            student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        certificates = student.certificate_ids
        if not certificates:
            certificates = self._create_demo_certificates(student)
        
        values = {
            'page_name': 'my_certificates',
            'student': student,
            'certificates': certificates,
        }
        
        return request.render('grants_training_suite_v19.portal_my_certificates', values)
    
    @http.route(['/grants/register'], type='http', auth='public', website=True, sitemap=False)
    def student_registration(self, **kw):
        """Student registration page"""
        values = {}
        
        # Get course options for registration
        active_integrations = request.env['gr.course.integration'].sudo().search([
            ('status', '=', 'active')
        ])
        
        values['courses'] = active_integrations
        
        return request.render('grants_training_suite_v19.portal_student_registration', values)
    
    @http.route(['/grants/register/submit'], type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def student_registration_submit(self, **post):
        """Handle student registration form submission"""
        try:
            # Validate required fields
            required_fields = ['name_english', 'name_arabic', 'email', 'phone', 'birth_date', 
                             'gender', 'nationality', 'english_level']
            
            for field in required_fields:
                if not post.get(field):
                    return request.render('grants_training_suite_v19.portal_registration_error', {
                        'error': _('Please fill all required fields.')
                    })
            
            # Check if email already exists
            existing_student = request.env['gr.student'].sudo().search([
                ('email', '=', post.get('email'))
            ], limit=1)
            
            if existing_student:
                return request.render('grants_training_suite_v19.portal_registration_error', {
                    'error': _('A student with this email already exists.')
                })
            
            # Create student record
            student_vals = {
                'name': post.get('name_english'),
                'name_english': post.get('name_english'),
                'name_arabic': post.get('name_arabic'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'birth_date': post.get('birth_date'),
                'gender': post.get('gender'),
                'nationality': post.get('nationality'),
                'native_language': post.get('native_language', 'Arabic'),
                'english_level': post.get('english_level'),
                'has_certificate': post.get('has_certificate') == 'yes',
                'certificate_type': post.get('certificate_type', ''),
                'state': 'draft',
            }
            
            # Add preferred course if selected
            if post.get('preferred_course'):
                student_vals['preferred_course_integration_id'] = int(post.get('preferred_course'))
            
            student = request.env['gr.student'].sudo().create(student_vals)
            
            # Create portal user for the student
            portal_group = request.env.ref('base.group_portal')
            user_vals = {
                'name': student.name_english,
                'login': student.email,
                'email': student.email,
                'groups_id': [(6, 0, [portal_group.id])],
                'active': True,
            }
            
            user = request.env['res.users'].sudo().create(user_vals)
            
            # Send welcome email
            template = request.env.ref('grants_training_suite_v19.email_template_student_welcome', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(student.id, force_send=True)
            
            _logger.info('New student registered: %s (%s)', student.name, student.email)
            
            return request.render('grants_training_suite_v19.portal_registration_success', {
                'student': student,
            })
            
        except Exception as e:
            _logger.error('Student registration error: %s', str(e))
            return request.render('grants_training_suite_v19.portal_registration_error', {
                'error': _('Registration failed. Please try again or contact support.')
            })
    
    @http.route(['/grants/login'], type='http', auth='public', website=True, sitemap=False)
    def student_login(self, redirect=None, **kw):
        """Student login page (redirects to Odoo's login)"""
        # Use Odoo's built-in login mechanism
        return request.redirect('/web/login?redirect=/my/student')
    
    @http.route(['/grants/courses/catalog'], type='http', auth='public', website=True)
    def course_catalog(self, **kw):
        """Public course catalog page"""
        active_integrations = request.env['gr.course.integration'].sudo().search([
            ('status', '=', 'active')
        ])
        
        values = {
            'page_name': 'course_catalog',
            'courses': active_integrations,
        }
        
        return request.render('grants_training_suite_v19.portal_course_catalog', values)
    
    @http.route(['/grants/courses/<int:course_id>'], type='http', auth='public', website=True)
    def course_detail_public(self, course_id, **kw):
        """Public course detail page"""
        course = request.env['gr.course.integration'].sudo().browse(course_id)
        
        if not course.exists():
            return request.render('website.404')
        
        values = {
            'page_name': 'course_detail_public',
            'course': course,
        }
        
        return request.render('grants_training_suite_v19.portal_course_detail_public', values)
