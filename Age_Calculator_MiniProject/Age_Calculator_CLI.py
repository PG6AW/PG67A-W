#Age_Calculator
#CLI

import datetime
def calculator(solar_birth):
    year = ""
    timedate = datetime.datetime.now()
    timedate = str(timedate)
    year = timedate[0] + timedate[1] + timedate[2] + timedate[3]
    solar_to_greg = solar_birth + 621
    greg_birth = solar_to_greg
    age = int(year) - int(greg_birth)
    return age
def calculate(greg_birth):
    year = ""
    timedate = datetime.datetime.now()
    timedate = str(timedate)
    year = timedate[0] + timedate[1] + timedate[2] + timedate[3]
    age = int(year) - int(greg_birth)
    return age
ask_it = True
while ask_it == True:
 ask = input("Gregorian or Solar?\nInput 's' for solar or 'g' for gregorian: ")
 if ask == "g" or ask == "G" or ask == "gregorian" or ask == "Gregorian" or ask == "Greg" or ask == "greg" or ask == "Gr" or ask == "gr" or ask == "grg" or ask == "Grg" or ask == "GREGORIAN":
  ask = "g"
  ask_it = False
 elif ask == "s" or ask == "S" or ask == "Solar" or ask == "solar" or ask == "Sol" or ask == "sol" or ask == "sl" or ask == "Sl" or ask == "SOLAR" or ask == "slr" or ask == "SLR":
  ask = "s"
  ask_it = False
 else:
  print("Invalid Input!")    
if ask == "s":    
 inp_birth = int(input("Input patient's solar birth year: "))
 print(f"Patient's age is: {calculator(inp_birth)}")
elif ask == "g":
    inp_birth = int(input("Input patient's gregorian birth year: "))
    print(f"Patient's age is: {calculate(inp_birth)}")