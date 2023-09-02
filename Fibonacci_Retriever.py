#Code to print all fibonacci numbers within a specified upperbound:


while 1 == 1:
    a = input("Enter the number to get all fibonacci numbers up to its upperbound point: ")
    Try_again = True
    while Try_again == True:
        try:
            a = int(a)
        except ValueError:
            print("Try again and enter a number!")
            a = input("Enter the number to get all fibonacci numbers up to its upperbound point: ")
        else:
            Try_again = False
    b = []
    b.append(0)
    b.append(1)
    c = 0
    while c <= a:
        c = b[len(b)-2]+b[len(b)-1]
        b.append(c)
    b.pop()
    print()
    print(f"Here are all fibonacci numbers up to {a}:",b)
    print()
