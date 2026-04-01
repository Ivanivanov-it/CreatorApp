
from django.core.mail.backends.base import BaseEmailBackend
from azure.communication.email import EmailClient
import os


class AzureCommunicationEmailBackend(BaseEmailBackend):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        connection_string  = os.environ.get('AZURE_COMMUNICATION_CONNECTION_STRING')
        self.client        = EmailClient.from_connection_string(connection_string)
        self.from_email    = os.environ.get('DEFAULT_FROM_EMAIL')

    def send_messages(self, email_messages):
        sent = 0

        for message in email_messages:
            try:
                email_content = {
                    "subject":   message.subject,
                    "plainText": message.body,
                }


                if hasattr(message, 'alternatives'):
                    for content, mimetype in message.alternatives:
                        if mimetype == 'text/html':
                            email_content["html"] = content

                mail = {
                    "senderAddress": self.from_email,
                    "recipients": {
                        "to": [{"address": addr} for addr in message.to]
                    },
                    "content": email_content,
                }

                poller = self.client.begin_send(mail)
                poller.result()
                sent += 1

            except Exception as e:
                if not self.fail_silently:
                    raise e

        return sent