class Person:
    def __init__(self, fname, lname):
        self.firstName = fname
        self.lastName = lname

    def printInfo(self):
        return "Person " + self.firstName + " " + self.lastName

class Student(Person):
    def __init__(self, fname, lname, y):
        Person.__init__(self, fname, lname)
        self.year = y

    def printInfo(self):
        return "Student" + " " + self.firstName + " " + self.lastName + ": Class of " + str(self.year)
    
class Teacher(Person):
    def __init__(self, fname, lname, g):
        Person.__init__(self, fname, lname)
        self.grade = g
    
    def printInfo(self):
        return "Teacher " + self.firstName + " " + self.lastName + ": Teaches Grade" + " " + str(self.grade)