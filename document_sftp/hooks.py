# -*- coding: utf-8 -*-
# Copyright 2016-2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import socket
from openerp import SUPERUSER_ID, api

def post_init_hook(cr, pool):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if socket.getfqdn().endswith('odoo-community.org'):  # pragma: no cover
        # we need a different default listening address on runbot
        env['ir.config_parameter'].set_param(
            'document_sftp.bind', '%s:0' % socket.getfqdn(),
        )
