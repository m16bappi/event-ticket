from decouple import config
from dataclasses import dataclass


@dataclass(init=False, frozen=True)
class ENV:
    SSLCOMMERZ_STORE_ID = config("SSLCOMMERZ_STORE_ID")
    SSLCOMMERZ_STORE_PASSWORD = config("SSLCOMMERZ_STORE_PASSWORD")
    SSLCOMMERZ_IS_SANDBOX = config("SSLCOMMERZ_IS_SANDBOX", cast=bool)
