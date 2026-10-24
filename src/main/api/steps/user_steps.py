from src.main.api.models.create_user_request import CreateUserCreditRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.requests_specs import RequestsSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.specs.response_specs import ResponseSpecs


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def deposit_crash(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)
        return response


    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
            response = ValidateCrudRequester(
                RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER,
                ResponseSpecs.request_ok()
            ).post(transfer_request)
            return response

    def transfer_crash(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
            response = ValidateCrudRequester(
                RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER,
                ResponseSpecs.unpoces_content()
            ).post(transfer_request)
            return response

    def credit(self, create_user_request: CreateUserCreditRequest, credit_request: CreditRequest):
            response = ValidateCrudRequester(
                RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREDIT,
                ResponseSpecs.request_created()
            ).post(credit_request)
            return response

    def credit_crash(self, create_user_request: CreateUserCreditRequest, credit_request: CreditRequest):
            response = ValidateCrudRequester(
                RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREDIT,
                ResponseSpecs.forbidden()
            ).post(credit_request)
            return response

    def create_account_credit(self, create_user_request: CreateUserCreditRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def repay(self, create_user_request: CreateUserCreditRequest, repay_request: RepayRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.REPAY,
            ResponseSpecs.request_ok()
        ).post(repay_request)
        return response

    def repay_crash(self, create_user_request: CreateUserCreditRequest, repay_request: RepayRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.REPAY,
            ResponseSpecs.not_found()
        ).post(repay_request)
        return response


