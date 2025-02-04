from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import redirect

from rightsolutions.settings import EMAIL_HOST_USER
import mimetypes
from django.conf import settings
from square.client import Client


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



SQUARE_APPLICATION_ID = 'sandbox-sq0idb-gAwWVEStoZcBZYN3XryFJA'
SQUARE_ACCESS_TOKEN = 'EAAAl5TGbV7dKZU8Nfw5l-ZFluWZUdkxyKWGEWMjGfCSqCbgoG-QpfIvj9Y2bBwx'
SQUARE_LOCATION_ID = 'LX8TR77STPYKS'
SQUARE_ENVIRONMENT = 'sandbox'



client = Client(
    access_token=SQUARE_ACCESS_TOKEN,
    environment="sandbox",
)


def process_payment(pagename, amount, source_id, service_name):
    """
    Process payment using Square API.
    :param amount: The amount to charge (in dollars).
    :param currency: The currency code (e.g., 'USD').
    :param source_id: The payment nonce from Square.
    :return: Tuple (success: bool, response: dict or error message)
    """
    # Initialize Square client
    if not amount or not service_name:
         return redirect("/order-failed/")
    client = Client(
        access_token=SQUARE_ACCESS_TOKEN,
        environment=SQUARE_ENVIRONMENT
    )

    # Create payment request
    body = {
        "idempotency_key": f"order-{source_id}-{amount}",
        "order": {
            "location_id": SQUARE_LOCATION_ID,
            "line_items": [
                {
                    "name": str(service_name),
                    "pagename": str(pagename),
                    "quantity": "1",
                    "base_price_money": {"amount": int(float(amount) * 100), "currency": "USD"},
                }
            ],
        },
        "checkout_options": {
                            "redirect_url": "https://yourwebsite.com/thank-you/",
                        },

    }

    # Process payment
    result = client.checkout.create_payment_link(body)
    return result





# @csrf_exempt  # Allow POST requests without CSRF token (ensure security in production)
# def create_square_checkout(request):
#     if request.method == "POST":
#         amount = request.POST.get("amount")  # Get amount from form input
#         service_name = request.POST.get("service_name")  # Get service name
#
#         if not amount or not service_name:
#             return redirect("/order-failed/")  # Handle missing data case
#
#         body = {
#             "idempotency_key": f"order-{request.user.id}-{amount}",
#             "order": {
#                 "location_id": LOCATION_ID,
#                 "line_items": [
#                     {
#                         "name": service_name,
#                         "quantity": "1",
#                         "base_price_money": {"amount": int(float(amount) * 100), "currency": "USD"},
#                     }
#                 ],
#             },
#             "checkout_options": {
#                 "redirect_url": "https://yourwebsite.com/thank-you/",
#             },
#         }
#
#         # Generate Checkout Link
#         result = client.checkout.create_payment_link(body)
#
#         if result.is_success():
#             return redirect(result.body['payment_link']['url'])  # Redirect to Square Checkout
#         else:
#             return redirect("/payment-failed/")  # Handle errors
#
#     return redirect("/order/")  # Redirect if accessed without POST data