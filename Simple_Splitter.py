#simple code that omits a character or a whole word from a string and returns it:

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


    def word_omitter_single(string,word):
        start = 0
        end = 0
        while end < len(string):
            if string[end:end+len(word)] == word or len(string) - 1 == end :
                print(string[start:end],end = "")
                start = end + len(word) + 1
            end += 1
        print(string[len(string)-1])


    def char_omitter_single(string,char):
        start = 0
        end = 0
        for i in string:
            if i == char or len(string) - 1 == end :
                print(string[start:end],end = "")
                start = end + len(char)
            end += 1
        print(string[len(string)-1])

    
    if ask == "c" or ask == "C":
        a = input("Input the string here: ")
        b = input("Input one character as the splitter: ")
        char_omitter_single(a,b)


    elif ask == "w" or ask == "W":
        a = input("Input the string here: ")
        b = input("Input one word as the splitter: ")
        word_omitter_single(a,b)
