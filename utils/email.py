import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_email(subject, body, context, recipient_list, is_body_template=True):
    if settings.EMAIL_NOTIFY:
        try:
            if is_body_template:
                body = render_to_string(body, context).strip()

            msg = EmailMessage(
                settings.ACCOUNT_EMAIL_SUBJECT_PREFIX + subject.title(),
                body,
                settings.DEFAULT_FROM_EMAIL,
                bcc=recipient_list,
            )
            msg.content_subtype = "html"
            msg.send()
            logger.info(f"Email sent to: {recipient_list}")
        except Exception as e:
            logger.exception(f"Failed to send email: {e}")
