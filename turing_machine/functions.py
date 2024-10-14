def cmdCheck(cmd):
    cmd = cmd.replace(" ", "")
    if (len(cmd) == 11
        and cmd[0] == '(' 
        and cmd[1] != '-' 
        and cmd[2] == ',' 
        and cmd[3] != '-'
        and cmd[4] == ','
        and cmd[5] != '-'
        and cmd[6] == ','
        and cmd[7] != '-'
        and cmd[8] == ','
        and cmd[9] in ['<', '-', '>']
        and cmd[10] == ')'):
        return True
    else:
        print("Invalid command structure")
        return False

def runMachine(string, cmdMx):
    machineState = 0
    machinePlace = 0
    cmdExausted = 0
    print(cmdMx)
    while cmdExausted < len(cmdMx):
        cmdExausted = 0
        for cmd in cmdMx:
            if machinePlace > len(string) - 1:
                break
            if cmd[1] == str(machineState) and cmd[3] == string[machinePlace]:
                machineState = str(cmd[5])
                string_list = list(string)
                string_list[machinePlace] = cmd[7]
                string = "".join(string_list)
                if cmd[9] == '<':
                    machinePlace -= 1
                elif cmd[9] == '-':
                    pass
                elif cmd[9] == '>':
                    machinePlace += 1
            else:
                cmdExausted += 1
                
    return string, machineState