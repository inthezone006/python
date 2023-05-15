import platform as pf
import people
import car
import requests

#Module and Class Example #1
def test1():
    print(people.Person("John", "Smith").printInfo())
    print(people.Student("Boring", "Bobby", 2022).printInfo())
    print(people.Teacher("Lame", "Larry", 10).printInfo())
    print()

#Module and Class Example #2
def test2():
    print(car.Car("Lamborghini", "Aventador").returnCar())
    print(car.BMW("M550I").returnCar())
    print(car.Toyota("86").returnCar())
    print()

#Another Module Example
def test3():
    print("Platform Architecture:", pf.machine())
    print()
