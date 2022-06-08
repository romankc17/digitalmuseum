from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_otp_vai_email(data):
        # Send email
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to']],
        )
        email.send()
        