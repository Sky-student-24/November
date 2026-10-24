import requests
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestsSpecs:
    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=request.model_dump(),
            headers=RequestsSpecs.base_headers()
        )

        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestsSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to authenticate")

    @staticmethod
    def unauth_headers():
        return RequestsSpecs.base_headers()


