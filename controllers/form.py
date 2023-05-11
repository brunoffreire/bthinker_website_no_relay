

import base64
import json

from psycopg2 import IntegrityError
from werkzeug.exceptions import BadRequest

from odoo import http, SUPERUSER_ID, _
from odoo.http import request
from odoo.tools import plaintext2html
from odoo.exceptions import ValidationError, UserError
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.website.controllers.form import WebsiteForm

class WebsiteForm(http.Controller):	

	def insert_record(self, request, model, values, custom, meta=None):

		mail_values = self._draft_mail_from_template()		
		model_name = model.sudo().model
		if model_name == 'mail.mail':
			mail_values.update({'reply_to': values.get('email_from')})
			mail_values.update({'subject': values.get('subject')})
			mail_values.update({'body_html': values.get('body_html')})
		
		record = request.env[model_name].with_user(SUPERUSER_ID).with_context(mail_create_nosubscribe=True).create(mail_values)
		
		if custom or meta:
			_custom_label = "%s\n___________\n\n" % _("Other Information:")  # Title for custom fields
			if model_name == 'mail.mail':
				_custom_label = "%s\n___________\n\n" % _("This message has been posted on your website!")
			default_field = model.website_form_default_field_id
			default_field_data = values.get(default_field.name, '')
			custom_content = (default_field_data + "\n\n" if default_field_data else '') \
				+ (_custom_label + custom + "\n\n" if custom else '') \
				+ (self._meta_label + meta if meta else '')

			# If there is a default field configured for this model, use it.
			# If there isn't, put the custom data in a message instead
			if default_field.name:
				if default_field.ttype == 'html' or model_name == 'mail.mail':
					custom_content = nl2br(custom_content)
				record.update({default_field.name: custom_content})
			else:
				values = {
					'body': nl2br(custom_content),
					'model': model_name,
					'message_type': 'comment',
					'res_id': record.id,
				}
				request.env['mail.message'].with_user(SUPERUSER_ID).create(values)

		return record.id
	
	def _draft_mail_from_template(self):
		
		# Localiza o template pelo External ID único
		template_ids = self.env.ref('bthinker_website_no_relay.website_contact_mail_template').ids
		if not template_ids:
			return None
		
		return template_ids[0].generate_email(template_ids[0].id)