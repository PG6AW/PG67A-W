a = input("Please input a string here: ")
print()
always_false = False
always_false_list = []
all_non_recursive_char = []
all_non_recursive_char_index = []
for i in a:
    boolean_value = True
    snapshot_of_a = list(a)
    snapshot_of_a.pop(a.index(i))
    for j in snapshot_of_a:
        if j == i:
            boolean_value = False
    if boolean_value != True:
        always_false_list.append(0)
    else:
        always_false_list.append(1)
    if boolean_value:
        all_non_recursive_char.append(i)
        all_non_recursive_char_index.append(a.index(i))
if len(all_non_recursive_char) != 0:
 print(f'The first non_recursive Character is: ("{all_non_recursive_char[0]}")' , f', And the address (order) of the first non_recursive character inside the string is: ("{all_non_recursive_char_index[0]+1}nd(st)") with the index (Starting_From_Zero) of ("{all_non_recursive_char_index[0]}")')
 print()
 print("All non_recursive characters including their order respectively in accordance with their index value: ")
 print()
 for c,d in zip(all_non_recursive_char,all_non_recursive_char_index):
  print(c , " : " , f"Order in ({a}): {d+1}" , end = (" | "))
if 1 not in always_false_list:
    always_false = True
if always_false == True:
    print("No non_recursive Character have been found in the given string!")
print()