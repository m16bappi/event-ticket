import os
import requests
from typing import Any, Dict
from events.models import Ticket


class SSLCommerzPayment:
    def __init__(self):
        self.session_url = f"{self.base_url}/gwprocess/v4/api.php"
        self.validation_url = f"{self.base_url}/validator/api/validationserverAPI.php"
        self.store_id = os.getenv("SSLCOMMERZ_STORE_ID")
        self.store_passwd = os.getenv("SSLCOMMERZ_PASSWD")
        self.default_params = {
            "store_id": self.store_id,
            "store_passwd": self.store_passwd,
        }

    @property
    def base_url(self):
        is_live = os.getenv("SSLCOMMERZ_LIVE") == "true"
        env = "securepay" if is_live else "sandbox"
        return f"https://{env}.sslcommerz.com"

    def init(self, ticket: Ticket) -> Dict[str, Any]:
        """
        Initialize a payment session.
        """
        payload = {
            **self.default_params,
            "total_amount": ticket.event.ticket_price,
            "currency": "BDT",
            "tran_id": ticket.order.id,
            "success_url": "",
            "fail_url": "",
            "cancel_url": "",
            "ipn_url": "",
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

    @staticmethod
    def parse_body(request) -> Dict[str, Any]:
        """
        Parse incoming request body for payment response.
        """
        content_type = request.headers.get("Content-Type")

        if content_type == "application/json":
            return request.json

        if content_type == "application/x-www-form-urlencoded":
            return {k: v for k, v in request.form.items()}

        raise ValueError("Unsupported content type")
