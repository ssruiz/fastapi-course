import json
import uuid

import requests

from decouple import config
from fastapi import HTTPException


class WiseService:
    def __init__(self):
        self.main_url = config("WISE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = f"{config('WISE_URL')}/v2/profiles"
        resp = requests.get(url, headers=self.headers)
        resp = self.process_response(resp)

        return [el["id"] for el in resp if el["type"] == "PERSONAL"][0]

    def create_quote(self, amount):
        url = f"{config('WISE_URL')}/v3/profiles/{self.profile_id}/quotes/"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": 100,
        }

        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        return self.process_response(resp)

    def create_recipient_account(self, full_name, iban):
        url = f"{config('WISE_URL')}/v1/accounts"
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "legalType": "PRIVATE",
            "details": {
                "iban": iban,
            }
        }

        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        return self.process_response(resp)

    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())
        url = f"{config('WISE_URL')}/v1/transfers"
        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        return self.process_response(resp)

    def fund_transfer(self, transfer_id):
        url = f"{config('WISE_URL')}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"

        data = {
            "type": "BALANCE"
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        return self.process_response(resp)

    def cancel_transfer(self, transfer_id):
        url = f"{config('WISE_URL')}/v1/transfers/{transfer_id}/cancel"

        resp = requests.put(url, headers=self.headers)
        return self.process_response(resp)

    @staticmethod
    def process_response(resp):
        if resp.status_code in [200, 201]:
            resp = resp.json()
            return resp

        raise HTTPException(500, "Payment provider is not available")
