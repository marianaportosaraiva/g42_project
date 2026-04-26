from classes.gclass import Gclass

class Partnership(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_university_id', '_program_id', '_course_start_date', '_students_number']
    header = 'Partnerships'
    des = ['ID', 'University ID', 'Program ID', 'Course Start Date', 'Number of Students']

    def __init__(self, id, university_id, program_id, course_start_date, students_number=None):
        super().__init__()
        id = Partnership.get_id(id) 
        self._id = id
        self._university_id = university_id
        self._program_id = program_id
        self._course_start_date = course_start_date
        self._students_number = int(students_number)
        
        Partnership.obj[id] = self
        Partnership.lst.append(id)

    @property
    def id(self): 
        return self._id
    @id.setter
    def id(self, id): 
        self._id = id

    @property
    def university_id(self): 
        return self._university_id
    @university_id.setter
    def university_id(self, university_id): 
        self._university_id = university_id

    @property
    def program_id(self): 
        return self._program_id
    @program_id.setter
    def program_id(self, program_id): 
        self._program_id = program_id

    @property
    def course_start_date(self): 
        return self._course_start_date
    @course_start_date.setter
    def course_start_date(self, course_start_date): 
        self._course_start_date = course_start_date

    @property
    def students_number(self): 
        return self._students_number
    @students_number.setter
    def students_number(self, students_number): 
        self._students_number = int(students_number)