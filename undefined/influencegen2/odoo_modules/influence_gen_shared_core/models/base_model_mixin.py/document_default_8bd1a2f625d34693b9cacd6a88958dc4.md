# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.http import request as odoo_request # To access current request if available
from typing import Optional, Dict, Any

from ..utils import logging_utils # Use relative import within the module

_logger = logging_utils.get_logger(__name__)

class InfluenceGenBaseMixin(models.AbstractModel):
    _name = 'influence.gen.base.mixin'
    _description = 'InfluenceGen Base Mixin for Common Fields and Methods'

    # Common Fields (Example)
    # These fields might be better placed directly on models that need them,
    # or if truly universal, consider their impact carefully.
    # For now, focusing on methods, especially logging.

    # correlation_id = fields.Char(
    #     string="Correlation ID",
    #     readonly=True,
    #     copy=False,
    #     help="Correlation ID for tracing requests related to this record, set on creation if available in context."
    # )

    # Methods
    def _get_current_correlation_id(self) -> Optional[str]:
        """
        Retrieves the correlation ID.
        Tries from self.env.context, then odoo.http.request, then generates a new one.
        """
        correlation_id = self.env.context.get('correlation_id')
        if not correlation_id and odoo_request:
            correlation_id = logging_utils.get_correlation_id(request_opt=odoo_request)
        if not correlation_id: # Generate if still not found
             correlation_id = logging_utils.get_correlation_id()
        return correlation_id

    def _log_activity_structured(
        self,
        message: str,
        level: str = "INFO",
        log_type_name: Optional[str] = None, # e.g. Odoo's 'mail.message.subtype' name like 'Note' or 'Activity'
        summary: Optional[str] = None, # For mail.activity summary
        note_html: Optional[str] = None, # For mail.message body or mail.activity note
        user_id_to_assign: Optional[int] = None, # For mail.activity assigned user
        date_deadline: Optional[fields.Date] = None, # For mail.activity deadline
        **kwargs # For extra_context in JSON log and potentially other mail.activity fields
    ):
        """
        Logs a structured message using logging_utils and optionally creates an Odoo mail.message or mail.activity.
        Automatically includes model name, record ID, and correlation ID in structured logs.
        """
        logger_instance = logging_utils.get_logger(self._name or 'influence.gen.model')
        correlation_id = self._get_current_correlation_id()

        extra_log_context = {
            'model': self._name,
            'res_id': self.id if self.id else None,
        }
        if kwargs:
            extra_log_context.update(kwargs)

        effective_message = message
        if note_html: # If note_html is provided, it's likely the main message content for mail.message/activity
            effective_message = note_html if isinstance(note_html, str) else "HTML content provided"


        if level.upper() == "INFO":
            logging_utils.log_info_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context)
        elif level.upper() == "ERROR":
            logging_utils.log_error_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context, exc_info=kwargs.get('exc_info', False))
        elif level.upper() == "WARNING":
            logging_utils.log_warning_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context)
        elif level.upper() == "DEBUG":
            logging_utils.log_debug_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context)
        elif level.upper() == "CRITICAL":
            logging_utils.log_critical_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context, exc_info=kwargs.get('exc_info', False))
        else:
            logging_utils.log_info_structured(logger_instance, f"({level}) {effective_message}", correlation_id=correlation_id, extra_context=extra_log_context)


        # Optional: Create Odoo Chatter message (mail.message) or Activity (mail.activity)
        # This part requires the 'mail' module dependency in __manifest__.py
        if log_type_name and self.id and hasattr(self, 'message_post'): # Check if model inherits from mail.thread
            if log_type_name.lower() != 'activity': # Avoid double processing if log_type_name is 'activity'
                try:
                    body_content = note_html or message
                    # Ensure subtype_xmlid is valid, e.g., 'mail.mt_note', 'mail.mt_comment'
                    subtype_xmlid = f"mail.mt_{log_type_name.lower().replace(' ', '_')}"
                    # Check if subtype exists before posting
                    subtype_exists = self.env['mail.message.subtype'].search_count([('name', '=', log_type_name)]) > 0 or \
                                     self.env['ir.model.data'].search_count([('module', '=', 'mail'), ('name', '=', f"mt_{log_type_name.lower().replace(' ', '_')}")]) > 0
                    
                    if not subtype_exists and log_type_name.lower() == 'note': # Default to note if specific one not found
                        subtype_xmlid = 'mail.mt_note'
                    elif not subtype_exists:
                         _logger.warning(f"Subtype '{log_type_name}' (xmlid: {subtype_xmlid}) not found for mail.message on {self._name}:{self.id}. Message not posted to chatter.") # NOSONAR
                         subtype_xmlid = None # Prevent posting if subtype is invalid and not 'note'

                    if subtype_xmlid:
                        self.message_post(body=body_content, subject=summary, subtype_xmlid=subtype_xmlid)
                        _logger.debug(f"Posted mail.message of type '{log_type_name}' for {self._name}:{self.id}") # NOSONAR
                except Exception as e:
                    _logger.error(f"Failed to post mail.message for {self._name}:{self.id}: {e}") # NOSONAR

        if log_type_name and log_type_name.lower() == 'activity' and self.id and hasattr(self, 'activity_schedule'):
            try:
                activity_summary = summary or message
                activity_type = self.env['mail.activity.type'].search([('name', '=', activity_summary)], limit=1)
                if not activity_type: # Create if not exists (or require pre-configuration)
                    # Try to find a default or a generic one first
                    default_activity_type = self.env['mail.activity.type'].search([('category', '=', 'default')], limit=1) # Odoo often has a 'default' category
                    if not default_activity_type:
                        default_activity_type = self.env['mail.activity.type'].create({
                            'name': summary or "Platform Activity",
                            'summary': summary or "General platform activity",
                            # 'category': 'default', # Optional: might need specific categories
                        })
                    activity_type = default_activity_type
                
                activity_values = {
                    'activity_type_id': activity_type.id,
                    'summary': activity_summary,
                    'note': note_html or message, # Odoo's activity_schedule uses 'note' for the body
                    'user_id': user_id_to_assign or self.env.user.id,
                }
                if date_deadline:
                    activity_values['date_deadline'] = date_deadline
                
                self.activity_schedule(**activity_values)
                _logger.debug(f"Scheduled mail.activity '{activity_summary}' for {self._name}:{self.id}") # NOSONAR
            except Exception as e:
                _logger.error(f"Failed to schedule mail.activity for {self._name}:{self.id}: {e}") # NOSONAR


    # @api.model_create_multi
    # def create(self, vals_list):
    #     """Override create to inject correlation_id and log."""
    #     records = super(InfluenceGenBaseMixin, self.with_context(
    #         logging_utils.inject_correlation_id_to_context(self.env.context)
    #     )).create(vals_list)
        
    #     for record in records:
    #         # Attempt to set correlation_id field if it exists on the concrete model
    #         if hasattr(record, 'correlation_id') and not record.correlation_id:
    #             current_corr_id = record._get_current_correlation_id()
    #             if current_corr_id:
    #                 try:
    #                     # Use a direct SQL update or a non-triggering write if necessary
    #                     # to avoid recursion if 'write' also logs.
    #                     # For simplicity, direct assignment might trigger write if not careful.
    #                     # This is a complex area; Odoo's ORM can be tricky with onchange/compute.
    #                     # Best to set in context and have field compute from context on create.
    #                     # Or, if the field is simple Char, a direct write during create is often fine.
    #                     # For now, assuming correlation_id is set through context or manually.
    #                     pass # record.correlation_id = current_corr_id
    #                 except Exception as e:
    #                     _logger.warning(f"Could not set correlation_id field on {record._name}:{record.id}: {e}")

    #         record._log_activity_structured(
    #             message=f"{record._description or record._name} created.",
    #             level="INFO",
    #             log_type_name="note" # Example: log as a chatter note
    #         )
    #     return records

    # def write(self, vals):
    #     """Override write to log."""
    #     res = super(InfluenceGenBaseMixin, self.with_context(
    #         logging_utils.inject_correlation_id_to_context(self.env.context)
    #     )).write(vals)
        
    #     for record in self:
    #         changed_fields = ", ".join(vals.keys())
    #         record._log_activity_structured(
    #             message=f"{record._description or record._name} updated. Fields changed: {changed_fields}.",
    #             level="INFO",
    #             log_type_name="note" # Example
    #         )
    #     return res
    
    # Note: Overriding create/write in a generic mixin for logging and correlation_id
    # needs careful consideration of performance and potential recursion if not handled correctly.
    # It might be better to call _log_activity_structured explicitly from the concrete models'
    # create/write methods where specific context is richer.
    # For correlation_id, passing it in context during service calls and then to ORM methods
    # is a common pattern, and models can then retrieve it from self.env.context.