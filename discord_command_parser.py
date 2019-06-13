from typing import List

def parse_command_args(message: str, command_name: str, len_of_command: int, num_args: int) -> List[str]:
    command_args = message.strip().split(" ")[len_of_command:]
    ca_length = len(command_args)
    if ca_length > num_args:
        raise Exception("ERROR: Too many arguments given to '{0}' command. Given '{1}'. Expected {2}.".format(command_name, ca_length, num_args))
    elif ca_length < num_args:
        raise Exception("ERROR: Too few arguments given to '{0}' command. Given '{1}'. Expected {2}.".format(command_name, ca_length, num_args))
    return command_args


def parse_add_me(message: str) -> str:
    command_args = parse_command_args(message, "!add me", 2, 0)
    

def parse_add_points(message: str) -> int:
    command_args = parse_command_args(message, "!add points", 2, 1)
    try:
        points = int(command_args[0])
        if points < 0:
            raise ValueError
    except ValueError as e:
        raise Exception("ERROR: Did not receive a positive integer for '!add points' command.")
    
    return points

# try:
#     print(parse_add_points("!add points 100"))
#     parse_add_me("!add me")
# except Exception as e:
#     print(e)
