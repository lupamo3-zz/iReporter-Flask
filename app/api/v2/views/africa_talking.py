import africastalking


class SMS:
    def __init__(self):
        # set your app credentials
        self.username = os.getenv('API_USERNAME')
        self.api_key = os.getenv('API_KEY')

        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS

    def send_sms_syn(self):
        recipients = ["+254714144041", "+254787556483", "+254717245777"]

        message = "I know who I am!"

        try:
            response = self.sms.send(message, recipients)
            print(response)
        except Exception as e:
            print('Encountered an error while sending: %s' % str(e))


if __name__ == '__main__':
    SMS().send_sms_sync()
