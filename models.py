
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
