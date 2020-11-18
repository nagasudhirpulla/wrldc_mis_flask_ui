from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_, name, email, roles):
        self.id = id_
        self.name = name
        self.email = email
        self.roles = roles

    def has_role(self, role):
        return role in self.roles