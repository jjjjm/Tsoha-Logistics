from application import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(144), nullable = False, unique = True)
    password = db.Column(db.String(144), nullable = False)
    admin = db.Column(db.Boolean, nullable = False)

    def __init__(self,username,password,admin = False):
        self.username = username
        self.password = password
        self.admin = admin
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def roles(self):
        print("self.admin")
        print(self.admin)
        if self.admin == True:
            return ["ADMIN","USER"]
        else:
            return ["USER"]
