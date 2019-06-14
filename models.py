
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
