# -*- coding: utf-8 -*-

import actions.views

urls = [
    # '/api/(.*)',           actions.views.ApiAction,
    '/admin/(.*)',           actions.views.AdminAction,
    '/article/(.*)',         actions.views.FrontAction,
    '/',                   actions.views.FrontIndexAction,
]

