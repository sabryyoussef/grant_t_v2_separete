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
    
    @http.route(['/my/student'], type='http', auth='user', website=True)
    def portal_my_student_dashboard(self, **kw):
        """Student dashboard - shows student info and enrolled courses"""
        student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        values = {
            'page_name': 'student_dashboard',
            'student': student,
            'courses': student.course_session_ids,
            'progress': student.progress_percentage,
            'certificates': student.certificate_ids,
        }
        
        return request.render('grants_training_suite_v19.portal_student_dashboard', values)
    
    @http.route(['/my/courses'], type='http', auth='user', website=True)
    def portal_my_courses(self, **kw):
        """List of enrolled courses for student"""
        student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        values = {
            'page_name': 'my_courses',
            'student': student,
            'sessions': student.course_session_ids,
        }
        
        return request.render('grants_training_suite_v19.portal_my_courses', values)
    
    @http.route(['/my/courses/<int:session_id>'], type='http', auth='user', website=True)
    def portal_course_detail(self, session_id, **kw):
        """Course session detail page"""
        student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        session = request.env['gr.course.session'].sudo().browse(session_id)
        
        # Verify this session belongs to the student
        if session.student_id != student:
            return request.render('website.403')
        
        values = {
            'page_name': 'course_detail',
            'student': student,
            'session': session,
        }
        
        return request.render('grants_training_suite_v19.portal_course_detail', values)
    
    @http.route(['/my/certificates'], type='http', auth='user', website=True)
    def portal_my_certificates(self, **kw):
        """List of certificates for student"""
        student = self._get_student_for_portal_user()
        
        if not student:
            return request.render('grants_training_suite_v19.portal_no_student')
        
        values = {
            'page_name': 'my_certificates',
            'student': student,
            'certificates': student.certificate_ids,
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
