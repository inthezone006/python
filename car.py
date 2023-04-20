class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def returnCar(self):
        return self.make + " " + self.model
    
class BMW(Car):
    def __init__(self, model):
        if not type(model) is str:
            raise TypeError("Only strings allowed!")
        else:
            self.make = "BMW"
            self.model = model

    def returnCar(self):
        return "BMW " + self.model
    
class Toyota(Car):
    def __init__(self, model):
        if not type(model) is str:
            raise TypeError("Only strings allowed!")
        else:
            self.make = "Toyota"
            self.model = model

    def returnCar(self):
        return "Toyota " + self.model