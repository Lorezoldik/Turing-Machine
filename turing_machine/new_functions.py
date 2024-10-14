import time


def unbundleCluster(cluster):
    """
    Unbundles a cluster string into a string and a list of commands

    A cluster string is a string in the format string,,,cmd1)(cmd2...
    This function splits the string into a string and a list of commands
    and validates each command. If a command is invalid, it is not included
    in the list of commands.

    Args:
        cluster (str): The cluster string to unbundle

    Returns:
        tuple: A tuple containing the string and the list of valid commands
    """

    cmdMx = []
    cluster = cluster.replace(" ", "")
    cluster = cluster.split(",,,")
    string = cluster[0]
    # Create a new list to hold valid commands
    valid_cmdMx = []
    cmdMx = str(cluster[1:])[2:-2].split(")(")
    print(cmdMx)
    for cmd in cmdMx:
        if not cmd.startswith("("):
            cmd = "(" + cmd
        if not cmd.endswith(")"):
            cmd = cmd + ")"
        if cmdCheck(cmd):
            valid_cmdMx.append(cmd)  # Only add valid commands to the new list
    
    return string, valid_cmdMx


def bundleCluster(string, cmdMx):
    """
    Bundles a string and a list of commands into a single string in the format string,,,cmd1)(cmd2...
    
    Args:
        string (str): The string to bundle
        cmdMx (list): A list of commands in quintuplet format
    
    Returns:
        str: The bundled string
    """
    
    return string + ",,," + ")(".join(cmdMx)

def parseInterval(part):
    """
    Converts a string representation of an interval into a list of strings representing the contents of that interval.

    If the string contains "..", it is interpreted as a range and the start and end values are split and processed accordingly.
    If the start and end values are both numeric, the range is interpreted as a numeric range and includes all the numbers from start to end (inclusive).
    If the start and end values are both alphabetical, the range is interpreted as an alphabetical range and includes all the characters from start to end (inclusive).

    If the string does not contain "..", it is interpreted as a list of individual values and is converted directly to a list of strings.

    Args:
        part (str): The string representation of the interval to be parsed

    Returns:
        list: A list of strings representing the contents of the given interval
    """
    # Handle ranges
    if ".." in part:
        start, end = part.split("..")
        
        # Check if it's a numeric or alphabetical range
        if start.isdigit() and end.isdigit():
            # Numeric range
            if int(start) <= int(end):
                return list(map(str, range(int(start), int(end) + 1)))
            else:
                return list(map(str, range(int(start), int(end) - 1, -1)))
        elif start.isalpha() and end.isalpha():
            # Alphabetical range
            if ord(start) <= ord(end):
                return [chr(c) for c in range(ord(start), ord(end) + 1)]
            else:
                return [chr(c) for c in range(ord(start), ord(end) - 1, -1)]
        else:
            raise ValueError("Inconsistent interval type")
    else:
        return list(part)

def cmdCheck(cmd): 
    """
    Checks if a given command is valid and in the correct format.

    The command must be a string of exactly 5 comma-separated arguments, surrounded by parentheses.
    The first argument must be a valid interval (either numeric or alphabetical),
    the second argument must be a valid interval, the third argument must be a valid interval,
    the fourth argument must be a valid interval, and the fifth argument must be one of '<', '-', or '>'.
    The intervals must all have the same length.

    If the command is valid, this function returns True, otherwise it prints an error message and returns False.
    """
    cmd = cmd.replace(" ", "")
    
    if not (cmd.startswith('(') and cmd.endswith(')')):
        print(f"Command must start with '(' and end with ')', problematic command: {cmd}")
        return False
    
    cmd = cmd[1:-1]  # Remove surrounding parentheses
    parts = cmd.split(',')
    
    if len(parts) != 5:
        print(f"Command must contain exactly 5 comma-separated arguments, problematic command: {cmd}")
        return False
    
    try:
        # Parse each part and validate indexing
        readState = parseInterval(parts[0])
        readSymbol = parseInterval(parts[1])
        writeState = parseInterval(parts[2])
        writeSymbol = parseInterval(parts[3])
        moveDirection = parts[4]
        
        # DEBUG: Print parsed intervals to check correctness
        #print(f"Read Symbol Interval: {readSymbol}")
        #print(f"Write Symbol Interval: {writeSymbol}")
        
        # Check that moveDirection is valid
        if moveDirection not in ['<', '-', '>']:
            print(f"Invalid move direction, problematic command: {cmd}")
            return False
        
        # Ensure intervals match in length
        if len(readSymbol) != len(writeSymbol):
            print(f"Read and write symbol intervals must match in length, problematic command: {cmd}")
            return False
        
        return True
    
    except Exception as e:
        print(f"Error in parsing intervals: {e}, problematic command: {cmd}")
        return False

def runMachine(string, cmdMx):
    """
    Runs the Turing Machine on the given string and commands.

    Args:
        string (str): The string to run the machine on.
        cmdMx (list): A list of commands in quintuplet format.

    Returns:
        tuple: A tuple containing the final string and the final state of the machine.
    """
    machineState = 0
    machinePlace = 0
    exhausted_cmds = 0
    delay = 0
    steps = 0  # Step counter for debugging
    string = string.replace(" ", "-")
    steps_check = input("Do you want to see the steps? (y/n) ")
    if steps_check.lower() == "y":
        try:
            delay = float(input("Enter the delay for each step in seconds: "))
            if delay < 0:
                raise ValueError
        except ValueError:
            print("Delay must be a positive number, using default delay of 0.2 seconds")
            delay = 0.2
        
    while exhausted_cmds < len(cmdMx):
        exhausted_cmds = 0

        for cmd in cmdMx:
            # Check if the machine head is at the last position and needs more space
            if machinePlace >= len(string):
                string += "-"  # Append a space at the end if machinePlace exceeds string length
            if machinePlace < 0:
                string = "-" + string  # Prepend a space at the beginning if machinePlace is less than 0
            
            cmd = cmd.replace(" ", "")
            cmd = cmd[1:-1]  # Remove surrounding parentheses
            parts = cmd.split(',')

            current_char = string[machinePlace]
            readState, readSymbol = parseInterval(parts[0]), parseInterval(parts[1])
            writeState, writeSymbol = parseInterval(parts[2]), parseInterval(parts[3])
            moveDirection = parts[4]

            if str(machineState) in readState and current_char in readSymbol:
                # DEBUG: Print the command being evaluated
                #print(f"State={machineState}, Position={machinePlace}, String={string}, Evaluating Command: {cmd}, Read State: {readState}, Read Symbol: {readSymbol}")
                if steps_check.lower() == "y":
                    print(f"State={machineState}, String={string}, Evaluating Command: {cmd}")
                time.sleep(int(delay))
                stateIndex = readState.index(str(machineState))
                symbolIndex = readSymbol.index(current_char)
                machineState = writeState[stateIndex]

                string_list = list(string)
                string_list[machinePlace] = writeSymbol[symbolIndex]
                string = "".join(string_list)

                if moveDirection == '<':
                    machinePlace -= 1
                elif moveDirection == '-':
                    pass
                elif moveDirection == '>':
                    machinePlace += 1
                break
                
            else:
                exhausted_cmds += 1

        steps += 1

        #if steps > 1000:  # Halting condition to prevent infinite loops
            #print("Halting to prevent infinite loop")
            #break
        string = string.replace("-", " ")
    return string, machineState