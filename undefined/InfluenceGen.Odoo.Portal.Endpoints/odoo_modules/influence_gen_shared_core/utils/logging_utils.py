# -*- coding: utf-8 -*-
import logging
import json
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

import odoo # For accessing odoo.http.request if available
from ..const import influence_gen_constants

_logger = logging.getLogger(__name__) # Logger for this utility module itself

def get_logger(name: str) -> logging.Logger:
    """Returns a logger instance for the given name."""
    return logging.getLogger(name)

def get_correlation_id(request_opt: Optional[Any] = None) -> str:
    """
    Retrieves or generates a correlation ID.
    Tries to get it from Odoo request headers or context, otherwise generates a new UUID.
    """
    correlation_id: Optional[str] = None
    # Try from odoo.http.request if available (e.g., in a controller context)
    if hasattr(odoo, 'http') and odoo.http.request and hasattr(odoo.http.request, 'httprequest'):
        correlation_id = odoo.http.request.httprequest.headers.get(
            influence_gen_constants.DEFAULT_CORRELATION_ID_HEADER
        )
    # Try from passed request_opt (e.g., Odoo's self.env.context in a model method, or request context dict)
    if not correlation_id and request_opt:
        if hasattr(request_opt, 'context') and isinstance(request_opt.context, dict):
            correlation_id = request_opt.context.get('correlation_id')
        elif isinstance(request_opt, dict): # if request_opt is already a context dict
            correlation_id = request_opt.get('correlation_id')
        # Fallback for other potential request-like objects if needed in future
        elif hasattr(request_opt, 'META') and isinstance(request_opt.META, dict): # Django-like request
             correlation_id = request_opt.META.get(f'HTTP_{influence_gen_constants.DEFAULT_CORRELATION_ID_HEADER.upper().replace("-", "_")}')
        elif hasattr(request_opt, 'headers') and isinstance(request_opt.headers, dict): # Flask/ FastAPI-like request
             correlation_id = request_opt.headers.get(influence_gen_constants.DEFAULT_CORRELATION_ID_HEADER)


    if not correlation_id:
        correlation_id = str(uuid.uuid4())
    return correlation_id

def inject_correlation_id_to_context(context: Optional[Dict[str, Any]], correlation_id: Optional[str] = None) -> Dict[str, Any]:
    """Injects correlation_id into context if not present."""
    if context is None:
        context = {}
    if 'correlation_id' not in context:
        context['correlation_id'] = correlation_id or get_correlation_id(
            request_opt=odoo.http.request if hasattr(odoo, 'http') and odoo.http.request else None
        )
    return context

def _format_log_message_json(
    message: str,
    level: str,
    logger_name: str,
    user_id: Optional[int] = None,
    request_id_val: Optional[str] = None, # Renamed to avoid conflict with odoo.http.request
    correlation_id_val: Optional[str] = None, # Renamed
    extra_context: Optional[Dict[str, Any]] = None
) -> str:
    """Constructs a JSON log message with UTC timestamp and contextual IDs."""
    log_entry: Dict[str, Any] = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'level': level,
        'logger': logger_name,
        'message': message,
    }
    # Attempt to get current Odoo user if not provided
    uid_to_log = user_id
    if uid_to_log is None and hasattr(odoo, 'SUPERUSER_ID'): # Check if odoo global is available
        try:
            # This might fail if not in an Odoo environment with an active env
            if odoo.env: # Check if odoo.env is available and initialized
                 uid_to_log = odoo.env.uid
        except AttributeError: # odoo.env might not exist or uid not set
            pass # Keep uid_to_log as None
        except Exception: # NOSONAR - Catch any other exception
            pass # Keep uid_to_log as None

    if uid_to_log is not None:
        log_entry['user_id'] = uid_to_log

    # Use provided correlation_id_val or try to get it
    final_correlation_id = correlation_id_val or get_correlation_id(
        request_opt=odoo.http.request if hasattr(odoo, 'http') and odoo.http.request else None
    )
    if final_correlation_id:
        log_entry['correlation_id'] = final_correlation_id

    if request_id_val: # If a specific request_id is passed
        log_entry['request_id'] = request_id_val
    elif hasattr(odoo, 'http') and odoo.http.request and hasattr(odoo.http.request, 'session') and odoo.http.request.session.sid:
        # Use Odoo session ID as a form of request identifier if no specific one is provided
        log_entry['session_id'] = odoo.http.request.session.sid
    elif hasattr(odoo, 'http') and odoo.http.request and hasattr(odoo.http.request, 'httprequest'):
        # Try to get X-Request-ID from headers if specified
        x_request_id = odoo.http.request.httprequest.headers.get(influence_gen_constants.REQUEST_ID_HEADER)
        if x_request_id:
            log_entry['request_id'] = x_request_id


    if extra_context:
        log_entry.update(extra_context)

    return json.dumps(log_entry, default=str) # Use default=str to handle non-serializable types like datetime

def _log_structured(
    logger_instance: logging.Logger,
    level_name: str, # e.g., "INFO", "ERROR"
    logging_level_int: int, # e.g., logging.INFO, logging.ERROR
    message: str,
    user_id: Optional[int] = None,
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    exc_info_flag: bool = False,
    extra_context: Optional[Dict[str, Any]] = None
):
    """Helper function to log structured messages."""
    if logger_instance.isEnabledFor(logging_level_int):
        json_message = _format_log_message_json(
            message, level_name, logger_instance.name, user_id, request_id, correlation_id, extra_context
        )
        logger_instance.log(logging_level_int, json_message, exc_info=exc_info_flag)

def log_info_structured(
    logger_instance: logging.Logger,
    message: str,
    user_id: Optional[int] = None,
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    extra_context: Optional[Dict[str, Any]] = None
):
    """Logs an INFO level message in a structured JSON format."""
    _log_structured(logger_instance, influence_gen_constants.LOG_SEVERITY_INFO, logging.INFO, message,
                    user_id, request_id, correlation_id, False, extra_context)

def log_error_structured(
    logger_instance: logging.Logger,
    message: str,
    exc_info: bool = False, # Pass True to include exception info
    user_id: Optional[int] = None,
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    extra_context: Optional[Dict[str, Any]] = None
):
    """Logs an ERROR level message in a structured JSON format."""
    _log_structured(logger_instance, influence_gen_constants.LOG_SEVERITY_ERROR, logging.ERROR, message,
                    user_id, request_id, correlation_id, exc_info, extra_context)

def log_warning_structured(
    logger_instance: logging.Logger,
    message: str,
    user_id: Optional[int] = None,
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    extra_context: Optional[Dict[str, Any]] = None
):
    """Logs a WARNING level message in a structured JSON format."""
    _log_structured(logger_instance, influence_gen_constants.LOG_SEVERITY_WARNING, logging.WARNING, message,
                    user_id, request_id, correlation_id, False, extra_context)

def log_debug_structured(
    logger_instance: logging.Logger,
    message: str,
    user_id: Optional[int] = None,
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    extra_context: Optional[Dict[str, Any]] = None
):
    """Logs a DEBUG level message in a structured JSON format."""
    _log_structured(logger_instance, influence_gen_constants.LOG_SEVERITY_DEBUG, logging.DEBUG, message,
                    user_id, request_id, correlation_id, False, extra_context)

def log_critical_structured(
    logger_instance: logging.Logger,
    message: str,
    exc_info: bool = False, # Pass True to include exception info
    user_id: Optional[int] = None,
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    extra_context: Optional[Dict[str, Any]] = None
):
    """Logs a CRITICAL level message in a structured JSON format."""
    _log_structured(logger_instance, influence_gen_constants.LOG_SEVERITY_CRITICAL, logging.CRITICAL, message,
                    user_id, request_id, correlation_id, exc_info, extra_context)