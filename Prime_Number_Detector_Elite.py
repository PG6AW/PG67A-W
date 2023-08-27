import math
while 1 == 1:
    n1 = input("Please enter a number as the lowermost bound of calculation range: ")
    n2 = input("Please enter a number as the uppermost bound of calculation range: ")
    ambiguity = True
    while ambiguity:
        try:
            n1 = int(n1)
            n2 = int(n2)
            ambiguity = False
        except ValueError:
            ambiguity = True
            print("Please Enter a Correct Number without ambiguous characters!")
            n1 = input("Again, Enter a number as the lowermost bound of calculation range: ")
            n2 = input("Again, Enter a number as the uppermost bound of calcualtion range: ")
    overkill = input("Would you like to get even more out of this? For instance knowing if a specific number is prime or not? (Enter Y for yes and N for no): ")
    statement_manager = ["N","Y"]
    ambiguity = True
    while ambiguity:
        if overkill not in statement_manager:
            overkill = input("(Please enter Y for 'yes' and N for 'no'): ")
        elif overkill in statement_manager:
            ambiguity = False
    if n1 > n2:
        n1,n2 = n2,n1

    def if_is_prime(num):
        if num < 2:
            return False
        elif num == 2:
            return True
        for i in range(2,int(math.pow(num,.5))+1):
            if num % i == 0:
                return False
        return True

    list1 = []
    def showprime(num1,num2):
        for number in range(num1,num2 + 1):
            if if_is_prime(number):
                list1.append(int(number))
        if len(list1) > 0:
            print("Here's a list of all prime integers within the bound interval as follows: ",list1)
        if len(list1) == 0:
            print("NO PRIME NUMBER WITHIN THE GIVEN RANGE!")

    showprime(n1,n2)

    if overkill == "Y":
        overkill = True
    elif overkill == "N":
        overkill = False

    if overkill == True:
        print("You asked to check if a number is prime or not!")
        n3 = input("Enter the number to know if it's prime or not: ")
        ambiguity = True
        while ambiguity:
            try:
                n3 = int(n3)
                ambiguity = False
            except ValueError:
                ambiguity = True
                print("Please enter an integer and try again!")
                n3 = input("Enter the number to know if it's prime or not: ")
        if if_is_prime(n3):
            print(f"('{n3}') is Prime!")
        else:
            print(f"('{n3}') Ain't Prime!")
