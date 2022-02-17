import uuid

# Formatting the user info data that is sent to API in request
class UserInfoModel:
    user_id: None
    username: None
    password: None
    role: None

    @staticmethod
    def parse(dict):
        user_model = UserInfoModel()
        user_model.user_id = dict.get("user_id")
        user_model.username = dict.get("username")
        user_model.password = dict.get("password")
        user_model.role = dict.get("role")

        if user_model.user_id is None:
            user_model.user_id = str(uuid.uuid4())

        if user_model.username is None:
            raise Exception("Username should not be empty!")

        if user_model.password is None:
            raise Exception("Password should not be empty!")

        if user_model.role is None:
            user_model.role = "USER"

        return user_model