# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class GrantsTrainingMain(http.Controller):
    """Main controller for grants training suite"""
    
    @http.route(['/grants'], type='http', auth='public', website=True)
    def index(self, **kw):
        """Landing page for grants training"""
        return request.render('grants_training_suite_v19.portal_home')
