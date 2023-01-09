import glob,os

'''
search and identify filepaths for the required files to run the whole project.
If any are missing they should throw exceptions or warnings here
'''

# identify filepaths for FPM file, txt file and ini file
# build in exceptions or warnings for each one if they are missing, partially, just checking if they are all there for now
def main():

    files = {}

    # find input directory folder and add fpm file to file list
    for file in os.listdir("./inputs"):
        if file.endswith(".fpm"):
            files["Windfarmer"] = f"./inputs/{file}"
        elif file.endswith(".ini"):
            files["Losses"] = f"./inputs/{file}"
        elif file.endswith(".txt"):
            files["Windog"] = f"./inputs/{file}"

    if len(files.keys()) < 3:
        raise Warning("There is an input file missing from the inputs folder")
    return files


if __name__ == "__main__":
    main()