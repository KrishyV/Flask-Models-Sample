
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Relationship for users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    refresh_token = db.Column(db.String(256))
    secret_qns =db.Column(db.String(256))
    secret_ans =db.Column(db.String(256))

    # Setting up relationship to PasswordHistory
    password_history = db.relationship('PasswordHistory', backref='user', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Hashes password
    def setPassword(self, password):
    	self.password_hash = generate_password_hash(password)

    # Checks if passwords match. Called when user attempts logging in
    def checkPassword(self, password):
    	return check_password_hash(self.password_hash, password)

    # Hashes secret answer
    def setSecretAnswer(self, secret_ans_unhash):
        self.secret_ans = generate_password_hash(secret_ans_unhash)

    # Checks if secret answer match. Called when user enters secret answer.
    def checkSecretAnswer(self, secret_ans_unhash):
        return check_password_hash(self.secret_ans, secret_ans_unhash)
    # Initialise the instance
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Password history. Keeps last four passwords, password cannot be the same
# as the previous password.
class PasswordHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_one = db.Column(db.String(256), default='0')
    password_two = db.Column(db.String(256), default='0')
    password_three = db.Column(db.String(256), default='0')
    password_four = db.Column(db.String(256), default='0')

    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # It goes thorugh all four columns of passwords, and checks if
    # they match the password that is passed through the function.
    # If they match, the functions True.
    def checkPastPassword(self, password):
        if check_password_hash(self.password_one, password) or \
           check_password_hash(self.password_two, password) or \
           check_password_hash(self.password_three, password) or \
           check_password_hash(self.password_four, password):
           print('I have checked the past four passwords!!')
           return True

    # This function simulates popping of an array by
    # systematically saving the password of the preceding
    # past password columns into its own column.
    # For example, password_four now gets password_three's password,
    # password_three gets password_two's password, so on and so forth
    # until password_one gets the password that's behind the current
    # password by one cycle.
    def setNewPassword(self, password):
        self.password_four = self.password_three
        self.password_three = self.password_two
        self.password_two = self.password_one
        self.password_one = password

    def __init__(self, **kwargs):
        super(PasswordHistory, self).__init__(**kwargs)
## End of User related tables
class Categories(db.Model):
    __tablename__ = 'categories' # Table names are specified this way
    __table_args__ = (
        UniqueConstraint('parent', 'child', name='unique_category'),
    ) 
    # Refer to https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/table_config.html for a better understanding
    
    parent = db.Column(db.String, nullable=False)
    child = db.Column(db.String, nullable=False)
    pid = db.Column(db.Integer, primary_key=True)
    concat = column_property(parent + " - " + child) # Useful if you wish to view a concatenated column in your application

    def __repr__(self):
        return f"Categories('{self.parent}', '{self.child}', '{self.pid}'), '{self.concat}'"
        
  # concat is a column property and thus there is no need for us to initialise it
  # since you can't commit to an empty table.
  
    def __init__(self, parent, child, pid):
        self.parent = parent
        self.child = child
        self.pid = pid
        
 # The code below is particularly useful if you have many columns to initialise.
 
 #   def __init__(self, **kwargs):
 #      super(Categories, self).__init__(**kwargs)
    
class Color(db.Model):
    __tablename__ = 'color'
    color_design = db.Column(db.String, unique=True, nullable=False)
    id = db.Column(db.String(4), db.CheckConstraint('length(id) = 4'), unique=True, nullable=False)
    type = db.Column(db.Integer, db.CheckConstraint('length(type) = 1' and 'type < 4'), unique=False, nullable=False)
    pid = db.Column(db.Integer, primary_key=True, nullable=False)

    # Some of the way you can implement constraints. For column type, I specified the integer can only
    # be of 'length 1' and below 4 so essentially 0-3.
    
    def __repr__(self): # In case you are wondering, this is necessary for you to be able to display them.
        return f"Color('{self.color_design}', '{self.id}', '{self.pid}', '{self.type}')"

    def __init__(self, color_design, id, pid, type):
        self.color_design = color_design
        self.id = id
        self.pid = pid
        self.type = type
