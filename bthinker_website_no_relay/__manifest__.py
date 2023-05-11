# -*- coding: utf-8 -*-
# Autor: B-Thinker
{
	'name': "Website No-Relay SMTP",
    
	'summary': """
		Módulo Odoo para envio de e-mail por
        servidores SMTP que não aceitam relay.
	""",

	'description': """
		Este módulo permite que o website envie emails
        utilizando um endereço de e-mail do próprio domínio
        SMTP usado para o recebimento de e-mails.
        
        Este módulo cria um template de e-mail para ser usado pelo
        formulário de contato do website. No template, definimos os
        parâmetros de envio de e-mail como SMTP server e destinatário.
	""",

	'author': "B-Thinker",
	'website': "http://www.bthinker.com.br",
	'category': 'Mail Utility',
	'version': '1.0',
	'license': 'LGPL-3',
    'support': 'contato@bthinker.com.br',	
    'images': ['static/description/logo.png'],
	'depends': ['base', 'mail', 'contacts', 'snailmail', 'website'],
	
	'data': [		
		'data/website_mail_template.xml',		
	],
	
	'installable': True,
	'application': True,
	'auto_install': False
}