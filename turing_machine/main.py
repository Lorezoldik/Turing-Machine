"""
Main file for the Turing Machine simulator.

This file contains the main loop of the simulator, which guides the user through
either guided mode or cluster mode. In guided mode, the user is prompted to enter
a string and a series of quintuple commands. In cluster mode, the user is prompted
to enter a cluster (a string and a list of commands).

The main loop is as follows:

1. Prompt the user for guided mode (g) or cluster mode (c).
2. If guided mode, prompt the user for a string and a series of quintuple commands.
   If cluster mode, prompt the user for a cluster.
3. Unbundle the cluster if necessary.
4. Run the machine on the commands and print the result.
"""


import new_functions


def main():
    """
    The main function for the Turing Machine simulator.
    """
    cmdMx = []

    mode = input("Guided mode (g) or cluster mode (c): \n")
    # Validate the mode
    while mode != 'g' and mode != 'c':
        mode = input("Invalid mode, enter g or c: \n")
    if mode == 'g':
        # Prompt the user for a string
        string = input("Enter the string: \n")
        print("Enter the commands in quintuplets, only - to start, only + to generate cluster: ")

        # Read commands until - is entered
        while True:
            cmd = input()
            if cmd == "-":
                break
            if cmd == "+":
                print(new_functions.bundleCluster(string, cmdMx))
            else:
                # Validate the command and add it to the list
                if new_functions.cmdCheck(cmd):
                    cmd = cmd.replace(" ", "")
                    cmdMx.append(cmd)

        # Run the machine and print the result
        print(new_functions.runMachine(string, cmdMx))

    if mode == 'c':
        # Prompt the user for a cluster
        cluster = input('Enter the cluster: \n')
        # Unbundle the cluster and run the machine
        string, cmdMx = new_functions.unbundleCluster(cluster)
        print(new_functions.runMachine(string, cmdMx))


if __name__ == "__main__":
    main()

