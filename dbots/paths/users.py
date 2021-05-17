from dbots.models.user import User
from dbots.paths import Path

user_path = Path("GET", "/users/user_id", response_type=User, caching=3 * 60, url_params=["user_id"])