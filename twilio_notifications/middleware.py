
### To send message, create Twilio REST client ###
def load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)

### Error handling with Django middleware. API calls from here ###
class TwilioNotificationsMiddleware(object):
    def __init__(self):
        self.administrators = load_admins_file()
        self.client = MessageClient()

### Custom alert message to send out via text message ###
    def process_exception(self, request, exception):
        exception_message = str(exception)
        message_to_send = MESSAGE % exception_message

### Trigger motifications for admin list ###
        for admin in self.administrators:
            self.client.send_message(message_to_send, admin['phone_number'])

        logger.info('Administrators notified')

        return None