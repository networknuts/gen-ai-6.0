def ask_information():
    name = input("What is your name? ")
    return name

def print_information(name):
    print(f"Your name is {name}")

name = ask_information()
print_information(name)