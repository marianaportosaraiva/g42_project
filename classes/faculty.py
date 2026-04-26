from classes.gclass import Gclass

class Faculty(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_info', '_university_id']
    header = 'Faculties'
    des = ['Faculty ID', 'Faculty Info', 'University ID']

    def __init__(self, id, info, university_id):
        super().__init__()
        id = Faculty.get_id(id)
        self._id = id
        self._info = info
        self._university_id = university_id
        
        Faculty.obj[id] = self
        Faculty.lst.append(id)

    @property
    def id(self): return self._id
    @id.setter
    def id(self, id): self._id = id

    @property
    def info(self): return self._info
    @info.setter
    def info(self, info): self._info = info

    @property
    def university_id(self): return self._university_id
    @university_id.setter
    def university_id(self, university_id): self._university_id = university_id