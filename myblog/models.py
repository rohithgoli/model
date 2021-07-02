from myblog import ndb, client, login_manager


@login_manager.user_loader
def load_user(email):
    with client.context():
        qry = Admin.query().filter(Admin.email == email).get()
        if qry == None:
            qry = Mentor.query().filter(Mentor.email == email).get()
            if qry == None:
                qry = Intern.query().filter(Intern.email == email).get()
        return qry


class Admin(ndb.Model):
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def get_user_type(self):
        return 'Admin'


class Intern(ndb.Model):
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    mentors = ndb.KeyProperty(kind="Mentor", repeated=True)

    def __repr__(self):
        return f"Intern('{self.username}', '{self.email}')"

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def get_user_type(self):
        return 'Intern'


class Mentor(ndb.Model):
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    interns = ndb.KeyProperty(kind="Intern", repeated=True)

    def __repr__(self):
        return f"Mentor('{self.username}', '{self.email}')"

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def get_user_type(self):
        return 'Mentor'


class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    posted_at = ndb.DateTimeProperty(auto_now=True)
    posted_by = ndb.KeyProperty(kind="Intern")

    def __repr__(self):
        return f"Post('{self.title}', '{self.posted_by}')"


class Task(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    posted_at = ndb.DateTimeProperty(auto_now=True)
    assigned_by = ndb.KeyProperty(kind="Mentor")
    assigned_to = ndb.KeyProperty(kind="Intern")

    def __repr__(self):
        return f"Task('{self.title}', '{self.assigned_by}', '{self.assigned_to}')"
