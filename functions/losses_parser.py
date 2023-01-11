import configparser


def main(losses_file):
    '''
    :param losses_file:
    :return a list of losses parsed from the input file :
    '''
    parser = configparser.ConfigParser(empty_lines_in_values=False)
    parser.read(losses_file)
    stored_vals = parser._sections
    losses = {}
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
    for key in stored_vals["LOSSES"].keys():
        losses[key] = {}
    for key,value in stored_vals["LOSSES"].items():
        losses[key] = value

    if not bool(losses):
        Warning("Losses File was not imported correctly, using default values")
        return losses_default
    else:
        return losses


losses_file = "../inputs/losses.ini"

if __name__ == '__main__':
    main(losses_file)