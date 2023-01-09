import configparser

losses_default = {
    "1a": 5,
    "1b": 0.99,
    "1c": 0.99,
    "2a": 0.99,
    "2b": 0.99,
    "2c": 0.99,
    "3a": 0.99,
    "3b": 0.99,
    "3c": 0.99,
}

def unpack(losses_file, losses_default):
    '''
    :param losses_file:
    :return a list of losses parsed from the input file :
    '''
    parser = configparser.ConfigParser(empty_lines_in_values=False)
    parser.read(losses_file)
    stored_vals = parser._sections
    losses = {}
    for key in stored_vals["LOSSES"].keys():
        losses[key] = {}
    for key,value in stored_vals["LOSSES"].items():
        # losses[key]['loss'] = key
        losses[key] = value

    if not bool(losses):
        raise Warning("Losses File was not imported correctly, using default values")
        return losses_default
    else:
        return losses


losses = unpack("inputs/losses.ini", losses_default)
print(losses)