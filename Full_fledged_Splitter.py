#simple code that omits a character or a whole word from a string and returns it or otherwise does the same thing with a multiple ones:

while 1 == 1:
    ask = input('Please input ("w") if you wish to split by a Word or ("c") if you wish to split by Character: ')
    answer_box = ["w","W","C","c"]
    invalid_checker = True
    while invalid_checker == True:
        if ask not in answer_box:
            print('Invalid input! Please type ("w") for "Word" OR ("c") for "Character"!')
            ask = input("Try again: ")
        else:
            invalid_checker = False


    def word_omitter_multi(string,word):

        import io
        import sys
        # Create a stream object to capture the output
        output = io.StringIO()
        # Redirect the standard output to the stream
        sys.stdout = output

        for j in word:
            start = 0
            end = 0
            while end < len(string):
                if string[end:end+len(j)] == j or len(string) - 1 == end :
                    print(string[start:end],end = "")
                    start = end + len(j) + 1
                end += 1
            print(string[len(string)-1])   

            # Reset the standard output
            sys.stdout = sys.__stdout__
            # Save the captured output to a variable
            string = output.getvalue()

    def word_omitter_single(string,word):
        start = 0
        end = 0
        while end < len(string):
            if string[end:end+len(word)] == word or len(string) - 1 == end :
                print(string[start:end],end = "")
                start = end + len(word) + 1
            end += 1
        print(string[len(string)-1])


    def char_omitter_multi(string,char):

        import io
        import sys
        # Create a stream object to capture the output
        output = io.StringIO()
        # Redirect the standard output to the stream
        sys.stdout = output

        for j in char:
            start = 0
            end = 0
            for i in string:
                if i == j or len(string) - 1 == end :
                    print(string[start:end],end = "")
                    start = end + len(j)
                end += 1
            print(string[len(string)-1])

            # Reset the standard output
            sys.stdout = sys.__stdout__
            # Save the captured output to a variable
            char = output.getvalue()

    def char_omitter_single(string,char):
        start = 0
        end = 0
        for i in string:
            if i == char or len(string) - 1 == end :
                print(string[start:end],end = "")
                start = end + len(char)
            end += 1
        print(string[len(string)-1])

    if ask == "c":
        det = "Character(s)"
    elif ask == "w":
        det = "Word(s)"
    ask2 = input(f"Multiple {det} or Solo one? input ('m') for Multiple and ('s') for Solo: ")
    approved_list = ["m","s","M","S"]
    check_approved = True
    while check_approved == True:
        if ask2 in approved_list:
            check_approved = False
        else:
            print("Please Try again!") 
            ask2 = input(f"Multiple {det} or Solo one? input ('m') for Multiple and ('s') for Solo: ")   

    if ask2 == "s" or ask2 == "S":
        solo = True
    elif ask2 == "m" or ask2 == "M":
        solo = False

    if ask == "c":
        if solo == True:
            a = input("Input the string here: ")
            b = input("Input one character as the splitter: ")
            char_omitter_single(a,b)
        elif solo == False:
            a = input("Input the string here: ")
            b = input("Input all characters as splitters: ").split()
            char_omitter_multi(a,b)

    elif ask == "w":
        if solo == True:
            a = input("Input the string here: ")
            b = input("Input one word as the splitter: ")
            word_omitter_single(a,b)
        elif solo == False:
            a = input("Input the string here: ")
            b = input("Input all words as splitters: ").split()
            word_omitter_multi(a,b)
