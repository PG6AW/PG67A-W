while 1 == 1:
  nothing = True
  while nothing == True:
      a = input("Enter your Average: ")
      b = ['1','2','3','4','5','6','7','8','9','0','.','-']
  
      for i in a:
          if i not in b:
              nothing = True
              break
          else:
              nothing = False
      if nothing == True or a == '.':
          print("Please input a Grade!" , end = (" "))
          nothin = True
  
  if a != '.' and nothing == False:
      a = float(a)
      if a < 10:
          print(" --------> Very Bad:((")
      elif a < 12:
          print(" --------> Bad:(")
      elif a < 15:
          print(" --------> Not Bad.")
      elif a < 17:
          print(" --------> Good!")
      elif a < 20:
          print(" --------> Very Good!!")
      elif a == 20:
          print(" --------> Excellent!!!")
      else:
          print("** Invalid Input **")
