#Code to simply count the number of characters or words in a given string:


list_string = input("Input words or chars separated by a space or Input a whole sentence instead : ").split()
count_list = []
unique_list_string = [] #Dont use list(set()) since it always returns things in an unordered* manner . use the following trick instead:
for i in list_string:
    if i not in unique_list_string:
        unique_list_string.append(i)
for i in unique_list_string:
    count = 0
    for j in list_string:
        if j == i:
            count += 1
    count_list.append(count)
for a,b in zip(unique_list_string,count_list):
    print(f'Word or Char: ("{a}")',",",f'Count: ("{b}")')
