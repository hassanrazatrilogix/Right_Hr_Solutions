from django.core.mail import EmailMessage
from django.conf import settings
from rightsolutions.settings import EMAIL_HOST_USER
import mimetypes


def sendEmail(too=['m.haneef1966@gmail.com'], sub='Test', temp=None, replyTo=None, attchs=None, custom=None, sendr=None, request=None):
    try:
        # Default sender is from settings or fallback
        # if sendr:
        #     sender = sendr  # If sendr is provided, use it
        # else:
            # user_name = request.user.get_full_name() or request.user.username  # Get user's full name or username
            # client_name = request.session.get('selectedClient', [None, None])[1]  # Access selected client from session
            # sender = f"{user_name} @ {client_name} | Trilogix <{EMAIL_HOST_USER}>"

        msg = EmailMessage(
            subject=sub,
            body=temp,
            from_email=EMAIL_HOST_USER,
            to=too,
            reply_to=[replyTo] if replyTo else None
        )

        # Handle attachments (both file-based and custom data)
        if attchs:
            for x in attchs:
                mimetype = x.content_type or mimetypes.guess_type(x.filename)[0]
                msg.attach(x.filename, x.read(), mimetype)

        if custom:
            for x in custom:
                mimetype = x.get("content_type", "application/octet-stream")
                msg.attach(x.get("filename"), x.get("data"), mimetype)

        # Send the email and return status
        msg.send()
        print("Email Status: Sent")
        return [True, 'Sent']

    except Exception as ex:
        print(f"Email Status: Failed with error: {ex}")
        return [False, str(ex)]
