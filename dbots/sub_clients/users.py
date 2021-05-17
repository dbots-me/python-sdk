from typing import Union

from dbots import HTTPClient
from dbots.models.user import User
from dbots.paths.users import user_path


class UsersSubClient(HTTPClient):
    def get_user(self, user_id: Union[int, str]) -> User:
        return self.request(user_path, user_id=user_id)
