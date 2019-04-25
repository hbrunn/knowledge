# -*- coding: utf-8 -*-
# Copyright 2016-2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from paramiko import AUTH_SUCCESSFUL, AUTH_FAILED,\
    OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED, OPEN_SUCCEEDED,\
    RSAKey, ServerInterface
from paramiko.py3compat import decodebytes
from openerp.exceptions import AccessDenied


class DocumentSFTPServer(ServerInterface):
    def __init__(self, env):
        import pdb
        pdb.set_trace()
        self.env = env
        super(DocumentSFTPServer, self).__init__()

    def check_auth_password(self, username, password):
        import pdb
        pdb.set_trace()
        try:
            user = self.env['res.users'].search([('login', '=', username)])
            if not user:
                return AUTH_FAILED
            user.sudo(user.id).check_credentials(password)
            self.env = self.env(user=user.id)
            return AUTH_SUCCESSFUL
        except AccessDenied:
            pass
        return AUTH_FAILED

    def check_auth_publickey(self, username, key):
        import pdb
        pdb.set_trace()
        user = self.env['res.users'].search([('login', '=', username)])
        if not user:
            return AUTH_FAILED
        for line in (user.authorized_keys or '').split('\n'):
            if not line or line.startswith('#'):
                continue
            key_type, key_data = line.split(' ', 2)[:2]
            if key_type != 'ssh-rsa':
                self.logger.info(
                    'Ignoring key of unknown type for line %s', line)
                continue
            if RSAKey(data=decodebytes(key_data)) == key:
                self.env = self.env(user=user.id)
                return AUTH_SUCCESSFUL
        return AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password,publickey'

    def check_channel_request(self, kind, chanid):
        if kind in ('session',):
            return OPEN_SUCCEEDED
        return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
