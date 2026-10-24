import requests
from requests import Response
from src.main.api.requests.requester import Requester
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse


class CreditRequester(Requester):
    def post(self, credit_request: CreditRequest) -> CreditResponse | Response:
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return CreditResponse(**response.json())