"""
@author: G42
(2025) objective: class Userlogin
"""
from werkzeug.security import generate_password_hash, check_password_hash
from classes.gclass import Gclass

class UserLogin(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # identifier attribute '_id' must be first
    att = ['_id', '_username', '_usergroup', '_password']
    header = 'Users'
    des = ['Id', 'User', 'User group', 'Password']
    logged_username = ''
    user_id         = 0

    def __init__(self, id, username, usergroup, password):
        super().__init__()
        id = int(float(id))
        id = UserLogin.get_id(id)
        self._id        = id
        self._username  = username
        self._usergroup = usergroup
        self._password  = password
        UserLogin.obj[id] = self
        UserLogin.lst.append(id)

    @property
    def id(self): return self._id
    @id.setter
    def id(self, v): self._id = v

    @property
    def username(self): return self._username
    @username.setter
    def username(self, v): self._username = v

    # alias: 'user' so gclass SQL column name matches
    @property
    def user(self): return self._username
    @user.setter
    def user(self, v): self._username = v

    @property
    def usergroup(self): return self._usergroup
    @usergroup.setter
    def usergroup(self, v): self._usergroup = v

    # password getter returns empty for security
    @property
    def password(self):
        return ''
    @password.setter
    def password(self, v):
        self._password = v

    def __str__(self):
        return f'Id:{self._id}, User:{self._username}, Usergroup:{self._usergroup}'

    @classmethod
    def get_user_id(cls, user):
        user_id = 0
        lsobj = cls.find(user, 'username')
        if len(lsobj) == 1:
            obj = lsobj[0]
            user_id = obj.id
        return user_id

    @classmethod
    def chk_password(cls, user, password):
        cls.logged_username = ''
        user_id = cls.get_user_id(user)
        if user_id != 0:
            obj = cls.obj[user_id]
            valid = check_password_hash(obj._password, password)
            if valid:
                cls.user_id         = obj.id
                cls.logged_username = obj.username
                message = 'Valid'
            else:
                message = 'Wrong password'
        else:
            message = 'No existent user'
        return message

    @classmethod
    def set_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def find(cls, value, attr):
        """Return list of objects whose attr equals value."""
        return [obj for obj in cls.obj.values() if getattr(obj, attr) == value]
