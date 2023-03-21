import glob,os


'''
search and identify filepaths for the required files to run the whole project.
If any are missing they should throw exceptions or warnings here
'''

# identify filepaths for FPM file, txt file and ini file
# build in exceptions or warnings for each one if they are missing, partially, just checking if they are all there for now
def main(directory):

    files = {"windfarmer": None, "losses": f"./inputs/losses.ini", "startup": f"./inputs/startup.ini", "windog": None}

    # find input directory folder and add fpm file to file list

    for file in os.listdir(f"{directory}/inputs"):
        if file.endswith(".fpm"):
            files["windfarmer"] = f"./inputs/{file}"
        elif file.endswith(".txt"):
            files["windog"] = f"./inputs/{file}"

    if len(files.keys()) < 4:
        raise Warning("There is an input file missing from the inputs folder")
    return files


if __name__ == "__main__":
    main()