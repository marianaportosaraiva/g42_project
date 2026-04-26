from classes.gclass import Gclass

class Program(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_title', '_category']
    header = 'Programs'
    des = ['Program ID', 'Title', 'Category']

    def __init__(self, id, title, category):
        super().__init__()
        id = int(float(id))
        id = Program.get_id(id)
        self._id = id
        self._title = title
        self._category = category
        
        Program.obj[id] = self
        Program.lst.append(id)

    @property
    def id(self): 
        return self._id
    @id.setter
    def id(self, id): 
        self._id = id

    @property
    def title(self): 
        return self._title
    @title.setter
    def title(self, title): 
        self._title = title

    @property
    def category(self): 
        return self._category
    @category.setter
    def category(self, category): 
        self._category = category