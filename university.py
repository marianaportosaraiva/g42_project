from classes.gclass import Gclass

class University(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_name', '_created_date']
    header = 'Universities'
    des = ['ID', 'Name', 'Created Date']

    def __init__(self, id, name, created_date):
        super().__init__()
        id = University.get_id(id)
        self._id = id
        self._name = name
        self._created_date = created_date
        
        University.obj[id] = self
        University.lst.append(id)

    @property
    def id(self): return self._id
    
    @id.setter
    def id(self, id): self._id = id

    @property
    def name(self): return self._name
    
    @name.setter
    def name(self, name): self._name = name

    @property
    def created_date(self): return self._created_date
    
    @created_date.setter
    def created_date(self, created_date): self._created_date = created_date