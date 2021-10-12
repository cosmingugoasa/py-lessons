from colorama import init
from colorama import Fore 

def printMenu():
    init()
    print(Fore.YELLOW + """\

                               Dax - 2021

     _____       _                                          __   ___  
    |  __ \     | |                                        /_ | |__ \ 
    | |__) |   _| |     ___  ___ ___  ___  _ __  ___  __   _| |    ) |
    |  ___/ | | | |    / _ \/ __/ __|/ _ \| '_ \/ __| \ \ / / |   / / 
    | |   | |_| | |___|  __/\__ \__ \ (_) | | | \__ \  \ V /| |_ / /_ 
    |_|    \__, |______\___||___/___/\___/|_| |_|___/   \_/ |_(_)____|
            __/ |                                                     
           |___/                                                       

                        'cuz regualar GUIs are boring        
    """)

    print(Fore.GREEN + """\
        Inserisci il numero corrispondente all'opzione che vuoi usare:""" + Fore.RESET + """
        - [""" + Fore.GREEN + """1"""+ Fore.RESET + """] Link.
        - [""" + Fore.GREEN + """2""" +Fore.RESET + """] TXT file con più link.
        - [""" + Fore.GREEN + """3""" +Fore.RESET + """] Registrazione audio.
    """)
