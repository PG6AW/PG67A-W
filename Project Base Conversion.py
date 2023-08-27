#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py
#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py
#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py
#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py

result = input("Enter the number in any base: ")
saved = result
base1 = input("Specify the current base for your number: ")
saved2 = base1
result1 = []
nothing_out = False
if int(saved2) < 2:
    nothing_out = True
number_dict = {'0':0,'1':1,
'2':2,'3':3,'4':4,'5':5,
'6':6,'7':7,'8':8,'9':9,
'A':10,'B':11,'C':12,
'D':13,'E':14,'F':15,
'G':16,'H':17,'I':18,
'J':19,'K':20,'L':21,
'M':22,'N':23,'O':24,
'P':25,'Q':26,'R':27,
'S':28,'T':29,'U':30,
'V':31,'W':32,'X':33,
'Y':34,'Z':35,'a':10,
'b':11,'c':12,'d':13,
'e':14,'f':15,'g':16,
'h':17,'i':18,'j':19,
'k':20,'l':21,'m':22,
'n':23,'o':24,'p':25,
'q':26,'r':27,'s':28,
't':29,'u':30,'v':31,
'w':32,'x':33,'y':34,
'z':35}
issues = False
nums_list = []
num_list = ['0','1','2','3','4','5','6','7','8','9']
for num in saved:
    if num not in num_list:
        nums_list.append(number_dict[num])
if len(nums_list) != 0:
 max_num = max(nums_list)
 if max_num >= int(saved2) :
  issues = True    
if int(saved2) > 36:
    issues = True
  
for j in result:
    result1.append(number_dict[j])
b = len(result1) - 1
stage1 = 0
for i in result1:
    if nothing_out == False:
     stage = int(i)*((int(base1)**b))
     stage1 += stage
     b = b - 1
#GATEKEEPER    
if nothing_out == True:
    stage1 = 1
n = int(stage1)
base = int(input("Enter the base for the result form in which you'd like the number to be transformed into: "))
saved3 = base
if int(saved3) > 36:
    issues = True
if int(saved3) < 2:
    nothing_out = True   
if nothing_out == True:
    remainder = 0
    n = 0  
last = []
while n>=base and nothing_out == False:
    remainder = n % base
    n = n // base
    dict_remainder = {10:"A",11:"B",
    12:"C",13:"D",14:"E",
    15:"F",16:"G",17:"H",
    18:"I",19:"J", 20:"K",
    21:"L", 22:"M", 23:"N",
    24:"O", 25:"P", 26:"Q",
    27:"R", 28:"S", 29:"T",
    30:"U", 31:"V", 32:"W",
    33:"X", 34:"Y", 35:"Z"}
    if remainder < 10:
        last.append(str(remainder))
    elif remainder >= 10:
        last.append(str(dict_remainder[remainder]))
if n < 10:          
    last.append(str(n))
elif remainder >= 10 or n >= 10:
    last.append(str(dict_remainder[n]))
final = []
final = last[::-1]
result = "".join(final)
if issues == True:
    print()
    print("Miscalculation occured since you entered a NUMBER with DIGITS EQUIVALENT or ABOVE the given BASE or perhaps, whether the BASE for the ORIGIN NUMBER or the BASE for the CONVERTING STAGE point is above 36!!! However the invalid output would be as follows: ")
if base <= 10 and nothing_out == False:
    print()
    print(f"The final result for {saved} in base {saved2} transforming to the base of {saved3} is:",int(result))
elif nothing_out == False:
    print()
    print(f"The final result for {saved} in base {saved2} transforming to the base of {saved3} is:",str(result))
if nothing_out == True:
    print("Invalid Base given!")

#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py
#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py
#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py
#For Updated Version of the Code visit: https://github.com/PG6AW/PG67AW/blob/master/Project%20Base%20Conversion_Updated.py
