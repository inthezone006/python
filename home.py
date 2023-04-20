import test

choice = 0
def theMain():
    print("Welcome! What would you like to try out? (press e to exit)")
    print("1: Module and Class Example #1")
    print("2: Module and Class Example #2")
    print("3: Another Module Example")
    choice = input("")

    if (choice == "1"):
        test.test1()
        theMain()

    elif (choice == "2"):
        test.test2()
        theMain()

    elif (choice == "3"):
        test.test3()
        theMain()
        
    elif (choice == "e"):
        pass

    else:
        print("Invalid option!")
        theMain()


theMain()
