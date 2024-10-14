import functions

cmdMx = []
string = input("Enter the string: \n")

print("Enter the commands in quintuplets, enter only - to start the machine: ")

while True:
    cmd = input()
    if cmd == "-":
        break
    else:
        if functions.cmdCheck(cmd):
            cmd = cmd.replace(" ", "")
            cmdMx.append(cmd)

print(functions.runMachine(string, cmdMx))