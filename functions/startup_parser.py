import configparser
import os

def main(working_dir, startup_params_file):
    '''
    :param startup_params:
    :return parameters on which to run the program, includes farm size, used in limiting production,
    8760 status to use the tmy and turbine model for losses calculations :
    '''

    parser = configparser.ConfigParser()
    os.chdir("..")
    parser.read(os.path.join(working_dir, "inputs", "startup_params.ini"))
    stored_vals = parser._sections

    startup_params = {}

    for key in stored_vals["PARAMS"].keys():
        startup_params[key] = {}
    for key,value in stored_vals["PARAMS"].items():
        startup_params[key]= value

    startup_params["run_8760"] = bool(startup_params["run_8760"])
    startup_params["farm_size"] = float(startup_params["farm_size"])
    startup_params["high_temp"] = float(startup_params["high_temp"])
    startup_params["low_temp"] = float(startup_params["low_temp"])


    return startup_params

if __name__ == '__main__':
    main()