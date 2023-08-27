while 1 == 1:
    a = int(input())
    for i in str(a):
        print(f"{i}: ",end = (""))
        for j in range(0,int(i)):
            print(f"{i}",end = (""))
        print()
