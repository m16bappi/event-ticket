import requests
from typing import Any, Dict

from config.env import ENV
from events.models import Ticket


class SSLCommerzPayment:
    def __init__(self):
        self.session_url = f"{self.base_url}/gwprocess/v4/api.php"
        self.validation_url = f"{self.base_url}/validator/api/validationserverAPI.php"
        self.store_id = ENV.SSLCOMMERZ_STORE_ID
        self.store_passwd = ENV.SSLCOMMERZ_STORE_PASSWORD
        self.default_params = {
            "store_id": self.store_id,
            "store_passwd": self.store_passwd,
        }

    @property
    def base_url(self):
        is_sandbox = ENV.SSLCOMMERZ_IS_SANDBOX
        env = "sandbox" if is_sandbox else "securepay"
        return f"https://{env}.sslcommerz.com"

    def init(self, ticket: Ticket) -> Dict[str, Any]:
        """
        Initialize a payment session.
        """
        trans_id = ticket.order.id
        payload = {
            **self.default_params,
            "total_amount": ticket.event.ticket_price,
            "currency": "BDT",
            "tran_id": trans_id,
            "success_url": ENV.SSLCOMMERZ_SUCCESS_CALLBACK,
            "fail_url": ENV.SSLCOMMERZ_FAILED_CALLBACK,
            "cancel_url": ENV.SSLCOMMERZ_FAILED_CALLBACK,
            "ipn_url": ENV.SSLCOMMERZ_IPN_CALLBACK.format(id=trans_id),
            "cus_name": ticket.name,
            "cus_email": ticket.email,
            "cus_phone": ticket,
            "cus_add1": "",
            "cus_city": "Dhaka",
            "cus_country": "Bangladesh",
            "shipping_method": "NO",
            "num_of_item": 1,
            "product_name": "Web and Data Summit",
            "product_category": "Contents",
            "product_profile": "general",
        }
        response = requests.post(self.session_url, data=payload)

        if response.status_code == 200:
            return response.json()

        response.raise_for_status()

    def validate(self, val_id: str) -> Dict[str, Any]:
        """
        Validate a payment by val_id.
        """
        params = {
            **self.default_params,
            "val_id": val_id,
            "format": "json",
            "v": "1",
        }
        response = requests.get(self.validation_url, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(f"Payment validation failed, status: {response.status_code}")
