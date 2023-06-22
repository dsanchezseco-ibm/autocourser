from re import A
import sys
import os
import autosolver

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def main() -> int:

    print("Welcome to the autocourser v1.0!")
    print()
    print("Before anything else, give me your JWT token (without 'Bearer')")
    JWT = input("> ")

    exit = False
    while not exit:
        clearConsole()
        print("what do you want to do today?:")
        print()
        print("1. Do an already solved quiz")
        print("2. Resolve a NEW quiz")
        print("3. exit")
        print()
        choice = input("> ")

        if choice == "1":
            print("Give me the QUIZ_ID to see if I already know that one")
            print("(start the quiz manually and give me the params from the url)")
            print("has the format 'QUIZ-XXXXXXXXXXXXX")
            QUIZ_ID = input("> ")
            clearConsole()
            directories = os.listdir( "QAs/" )
            autosolver.solver(QUIZ_ID, JWT, QUIZ_ID+".txt" in directories)
        elif choice == "2":
            print("I need the QUIZ_ID (start the quiz manually and give me the params from the url)")
            print("has the format 'QUIZ-XXXXXXXXXXXXX")
            QUIZ_ID = input("> ")
            clearConsole()
            autosolver.solver(QUIZ_ID, JWT, False)
        elif choice == "3": 
            clearConsole()
            print("You owe me a beer! Bye!")
            exit = True

    return 0


if __name__ == '__main__':
    sys.exit(main())
