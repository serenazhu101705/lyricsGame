import random, string, os, module; from lyricsModule import *

while True:
    directory = '../lyrics game/lyrics/'
    highscores = '../lyrics game/high scores/'

    def numbers(List, choice):
        l = "a"
        vowels = ['a','e','i','o','u']
        if choice[0] in vowels:
            l = "an"
        print("\nChoose %s %s:\n" % (l, choice))
        if len(List) != 1:
            List.append("Random %s" % choice)
        for i, el in enumerate(List, 1):
            print("%d. %s" % (i, el))
        print("\n")
        l = module.numbers(1,len(List))
        if l == len(List) and len(List) != 1:
            l = random.randint(1, len(List) - 1)
        return List[l - 1]
    
    genre = numbers(["Country","Pop","Rap"], "genre of music")
    directory = directory + str.lower(genre) + '/'
    
    names = os.listdir(directory)
    for i in names:
        if i not in os.listdir(highscores):
            with open(highscores + i, 'w') as f:
                f.write('0')

    fileslist = [directory + i for i in names]

    t = []
    artists = []
    for i in fileslist:
        lines = module.read(i, 'r')
        title, artist = lines[0].replace("\n",''), lines[1].replace("\n",'')
        t.append(title)
        artists.append(artist) 

    titles = []; artists = sorted(artists)
    artist = numbers(list(dict.fromkeys(artists)), "artist")


    for i in t:
        if artist in i:
            titles.append(i)

    titles.sort()
    title = numbers(titles, "song")

    for i in fileslist:
        lines = module.read(i, 'r')
        if lines[0].replace("\n",'') == title:
            filename = i
            highscore_file = i.replace(directory, highscores)


    a = ''
    with open(filename) as fp:
        for i , line in enumerate(fp):
            if i > 3:
                a = a + line
    alist = list(set(a.split()))

    levels = ["Beginner(7 random words)", "Intermediate (15 random words)","Advanced (30 random words)","Expert (Every word (Are you crazy?????))"]
    level_choice = numbers(levels, "level")
    print(level_choice,"\n\n")

    #missingwords_list
    blank = "_"
    missingwords_list = []
    removes, adds = set(), set()
    
    levels.remove("Expert (Every word (Are you crazy?????))")
    for i in '7', '15', '30':
        if i in level_choice:
            level = int(i)
                
    if level_choice in levels:
        while len(missingwords_list) != level:
            removes, adds = set(), set()
            while len(missingwords_list) != level:
                if len(missingwords_list) > level:
                    missingwords_list.pop(random.randint(0,len(missingwords_list)))
                else:
                    missingwords_list.append(random.choice(alist))

            #remove duplicated words
            for i in missingwords_list:
                for el in missingwords_list:
                    if i in el and i!=el:
                        removes.add(i) 

            module.remove(missingwords_list,'a','')
            missingwords_list = create(missingwords_list)

        #Replace missingwords_list string w/ ___    
        for i in missingwords_list:
            a = a.replace(i, blank*len(i))


    #Expert
    else:
        level = len(alist)
        for i in list(string.ascii_lowercase):
            a = a.replace(i,blank)

        for i in list(string.ascii_uppercase):
            a = a.replace(i,blank)

        for i in list(string.digits):
            a = a.replace(i, blank)

        missingwords_list = [i for i in alist if i != '']
        missingwords_list = create(missingwords_list)


    missingwords_list = list(map(str.lower,missingwords_list))
    print(a, """\nFill in the missing lyrics
for %s.
You have %d words left.\n""" % (title, level))
    clue, wrong = 0, 0
    trieslist, answers_list = [], set()
    for i in range(len(missingwords_list)):
        if "'" in missingwords_list[i]:
            missingwords_list[i] = missingwords_list[i].replace("'","")
            
    
    #answer loop
    while True:
        #input and remaining blanks list
        answer = input().lower()
        answer = module.Replace([i for i in list(string.punctuation) if i != '-'], answer)
        remainingblanks_list = [str(i) for i in missingwords_list if i not in answers_list]

        goods = ['clue','i give up', 'password']
        #trieslist
        if answer not in goods:
            trieslist.append(answer)

        #clues  
        if answer == "clue":
            if clue < 3:
                print("Here is a clue: One of the words is: " + "'" + random.choice(remainingblanks_list) + "'")
                clue = clue + 1
                print("You have",3 - clue,"clues left.")

            else:        
                print("I'm sorry, you are only allowed 3 clues per game.")


        #right
        if answer in answers_list:
            print("You have already done this word. You have " + str(len(remainingblanks_list)) + " words left.") 


        if answer in missingwords_list and answer not in answers_list:
            answers_list.add(answer)
            print("YES GOOD JOB! YOU REALLY KNOW YOUR " + str.upper(artist) + "! YOU HAVE " + str(len(remainingblanks_list) - 1) + str(" WORDS LEFT!"))
        
        #wrong
        if answer not in missingwords_list and answer not in goods:
            print("Sorry, that is not one of the blanks. Try again. You have " + str(len(remainingblanks_list)) + str(" words left!"))
            wrong = wrong + 1

        if clue < 4 and answer not in goods and answer not in missingwords_list:
            print("Need a hint? Type in 'clue' below and I will tell you one of the words.")

        if wrong >= 8 and (answer not in missingwords_list) and answer not in goods:
            print("Give up? Type in 'I give up' below.")    


        #hack
        if answer == "password":
            password = input()
            if password == "serenaisawesome":
                print("Welcome, Boss Master Serena.\nHere is what you have requested.")
                for i in range(0,len(remainingblanks_list)):
                    print(u'\u2022' + str.capitalize(remainingblanks_list[int(i)]))



            if password != 'serenaisawesome' and password != "im done":
                print("Sorry, that is not one of the blanks. Try again. You have " + str((len(missingwords_list) - len(answers_list))) + str(" words left!"))


        #finished
        if answer == 'i give up' or len(answers_list) == len(missingwords_list) or (answer == "password" and password == "im done"):
            lines = module.read(highscore_file, 'r')
            for i in range(len(lines)):
                if level_choice in lines[i]:
                    highscore = float(module.strreplace(lines[i], level_choice + ": ", '\n'))   
                    line = i
            right = len(answers_list); tries = len(answers_list) + wrong

            if answer=="i give up":
                if len(remainingblanks_list) < 30:
                    print("Here is a list of remaining the blanks:\n")
                    for i in remainingblanks_list:
                        print(u'\u2022', str.capitalize(i))

            overall_score = (right/(len(missingwords_list) + wrong)) * 100
            overall_score = round(overall_score, 1)
            rights = len(missingwords_list)

            if len(answers_list) == len(missingwords_list) or (answer == "password" and password == "im done"):
                print("\nGood Job! You filled in all the blanks!\n")
            if len(missingwords_list) < 30:
                for i in missingwords_list:
                    print(u'\u2022',str.capitalize(i))
            if tries != 0:
                otries = tries + clue
                overall_score = round((right/otries) * 100, 1)
                rights = tries

            print("""\nYou got %s answers correct and you had %d tries.
You got %d words wrong.
You typed in %d duplicate words.
That means you got %d / %d right.
You used %d clues.
The high score for this level is %s.""" % (right, len(trieslist), wrong, len(trieslist) - (wrong + len(answers_list)), right, rights, clue, float(highscore)))
            if tries != 0:
                print("\nYour overall score is " + str(overall_score) + ", which is including your used clues.")
            if overall_score > highscore:
                print("Congratulations! You've set the new high score for this level!")
                lines[line] = "%s: %s\n" % (level_choice, overall_score)
                with open(highscore_file, 'w') as f:
                    f.write(''.join(lines))
            
                

            if overall_score == highscore:
                print("Good job, you tied the high score for this song!")
            break

    #play again?
    print("\nDo you want to play this again?")
    play = module.yesorno()
    if play == "no":
        print("\nOk, thanks for playing!")
        print("Feedback? Type Yes or No below")
        feedback = module.yesorno()

        if feedback == "yes":
            print("\nType your feedback below")
            feedback = input()
            with open('../lyrics game/feedback', 'a') as file:
                file.write("\n\n\u2022 %s" % feedback)

            print("\nThanks for your feedback! Song recommendations and troubleshooting reports are always appreciated!")
        break
