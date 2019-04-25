# -*- coding: utf-8 -*-
# Copyright 2016-2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import time
import paramiko
from openerp import tools
from openerp.modules.registry import RegistryManager
from openerp.tests.common import TransactionCase, at_install, post_install
from openerp.addons.document_sftp.models.document_sftp import _db2thread
from ..hooks import post_init_hook


@at_install(False)
@post_install(True)
class TestDocumentSftp(TransactionCase):
    def test_document_sftp(self):
        # be sure to set a hostkey
        self.assertTrue(
            'PRIVATE KEY' in
            self.env['ir.config_parameter'].get_param('document_sftp.hostkey')
        )
        # give it some time
        time.sleep(5)
        # use this to bind to our server
        bind = self.env['ir.config_parameter'].get_param('document_sftp.bind')
        host, port = bind.split(':')
        transport = paramiko.Transport((host, int(port)))
        demo_key = paramiko.rsakey.RSAKey(
            file_obj=tools.file_open('document_sftp/demo/demo.key'))
        transport.connect(username='demo', pkey=demo_key)

        sftp = paramiko.SFTPClient.from_transport(transport)
        self.assertTrue('By model' in sftp.listdir('.'))
        self.assertTrue('res.company' in sftp.listdir('/By model'))
        sftp.close()

    def tearDown(self):
        super(TestDocumentSftp, self).tearDown()
        thread = _db2thread[self.env.cr.dbname][0]
        _db2thread[self.env.cr.dbname][1].set()
        thread.join()
