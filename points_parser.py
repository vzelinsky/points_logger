

def s_parse_add_points(message):
    command_args = message.strip().split(" ")[2:]
    ca_length = len(command_args)
    if ca_length > 1:
        raise Exception("ERROR: Too many arguments given to '!add points' command. Given '{0}'. Expected 1.".format(ca_length))
    elif ca_length < 1:
        raise Exception("ERROR: Too few arguments given to '!add points' command. Given '{0}'. Expected 1.".format(ca_length))
    
    try:
        points = int(command_args[0])
        if points < 0:
            raise ValueError
    except ValueError as e:
        raise Exception("ERROR: Did not receive a positive integer for '!add points' command.")
    
    return points

# try:
#     s_parse_add_points("!add points 100")
# except Exception as e:
#     print(e)
