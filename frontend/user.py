class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.authenticated = False
        self.token = None

    def is_active(self):
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False