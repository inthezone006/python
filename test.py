class Person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def printName(self):
        return self.fname, self.lname

x = Person("John", "Smith")
print(x.printName()[0], x.printName()[1])