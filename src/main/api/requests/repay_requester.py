import requests
from requests import Response
from src.main.api.requests.requester import Requester
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse


class RepayRequester(Requester):
    def post(self, repay_request: RepayRequest) -> RepayResponse | Response:
        url = f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            json=repay_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return RepayResponse(**response.json())

