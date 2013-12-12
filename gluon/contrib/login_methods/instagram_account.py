#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of web2py Web Framework (Copyrighted, 2007-2009).
Developed by Massimo Di Pierro <mdipierro@cs.depaul.edu>.
License: GPL v2

Thanks to Hans Donner <hans.donner@pobox.com> for GaeGoogleAccount.
"""

from gluon.http import HTTP
try:
    from instagram import client
except ImportError:
    raise HTTP(400, "instagram module not found")


class InstagramAccount(object):
    """
    Login will be done via Google's Appengine login object, instead of web2py's
    login form.

    Include in your model (eg db.py)::

        from gluon.contrib.login_methods.linkedin_account import LinkedInAccount
        auth.settings.login_form=LinkedInAccount(request,KEY,SECRET,RETURN_URL)

    """

    def __init__(self, request, client_id=None, client_secret=None, access_token=None, redirect_uri=None, scope=["likes","comments"]):
        self.request = request
        self.scope = scope
        self.api = client.InstagramAPI(client_id, client_secret, access_token, redirect_uri)

    def login_url(self, next="/"):        
        return self.api.get_authorize_url(scope=self.scope)

    def logout_url(self, next="/"):
        return ''

    def get_user(self):
        result = self.request.vars.code and self.api.exchange_code_for_access_token(self.request.vars.code)
        if result:
            name = result[1]['full_name'].split(' ')
            return dict(first_name=name[0], 
                        last_name=' '.join(name[1:]),
                        username=result[1]['username'])

