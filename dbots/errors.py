from requests import Response
from typing import Union


class DBotsApiError(Exception):
    def __init__(self, response: Response):
        self.response = response
        if "message" in response.json():
            self.message = response.json()["message"]
        elif response.headers.get("Content-Type") == "application/json":
            self.message = response.json()
        else:
            self.message = response.content
        super().__init__(
            f"The Api has answered with a exception: {response.status_code} - {self.message}."
        )


class BadRequest(DBotsApiError):
    pass


class Unauthorized(DBotsApiError):
    pass


class Forbidden(DBotsApiError):
    pass


class NotFound(DBotsApiError):
    pass


class MethodNotAllowed(DBotsApiError):
    pass


class AuthenticationNeeded(Exception):
    def __init__(self):
        super().__init__(
            "This operation needs authentication. Please add your api token to client."
        )


class TooManyRequests(DBotsApiError):
    def __init__(self, response: Response):
        self.retry_after: int = int(response.headers.get("retry-after"))
        super().__init__(response)


_errors = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    429: TooManyRequests,
}


def handle_response(response: Response) -> Union[dict, bytes]:
    if response.status_code >= 400:
        if response.status_code in _errors:
            raise _errors[response.status_code](response)
        else:
            raise DBotsApiError(response)
    elif response.headers.get("Content-Type") == "application/json":
        return response.json()
    else:
        return response.content
