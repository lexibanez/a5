# Lex Ibanez
# laibanez@uci.edu
# 70063614

"""
This module provides functions to list the contents of
a directory based on certain options. It includes functionality
to list files with a specific extension and to search for a specific file.
"""

from pathlib import Path
from Profile import Profile, Post, DsuProfileError
from ds_client import send
from OpenWeather import OpenWeather
from LastFM import LastFM


def get_last_option(options):
    """
    This function returns the last option from the provided list of options.
    If the length of the options list is 3, it returns the third option.
    If the length of the options list is 4, it returns the fourth option.
    """
    if len(options) == 3:
        return options[2]
    elif len(options) == 4:
        return options[3]


def list_directory(directory, options):
    """
    This function takes a directory and a list of options,
    and lists the contents of the directory. It separates the
    contents into files and directories, and returns these as
    two separate lists.
    """
    contents = list(directory.iterdir())
    # sort contents for files
    files = [x for x in contents if x.is_file()]
    # sort contents for directories
    directories = [x for x in contents if x.is_dir()]

    if '-e' in options:
        suffix = get_last_option(options)

        for file in files:
            if file.suffix == '.' + suffix:
                print(file)
        for directory in directories:
            if '-r' in options:
                list_directory(directory, options)

    elif '-s' in options:
        search_file = get_last_option(options)

        # checks if the search file has a path
        if Path(directory / search_file).is_file():
            print(Path(directory / search_file))
        for directory in directories:
            if '-r' in options:
                list_directory(directory, options)

    elif '-f' in options:
        for file in files:
            print(file)
        for directory in directories:
            if '-r' in options:
                list_directory(directory, options)

    else:
        for file in files:
            print(file)
        for directory in directories:
            print(directory)
            if '-r' in options:
                list_directory(directory, options)


def create_file(directory, options):
    """
    This function creates a new file in the specified directory.
    The '-n' option followed by a string can be used to
    specify the name of the new file. If the specified directory
    does not exist, it raises an exception.
    """
    if not directory.is_dir():
        print("not a directory")
        raise Exception("not a directory")

    if "-n" in options:
        index = options.index('-n')
        if index + 1 < len(options):
            file_name = options[index + 1]
            new_path = directory / f'{file_name}.dsu'
            new_path.touch()
        else:
            print("missing file name")
            raise Exception("missing file name")
    else:
        print("missing -n option")
        raise Exception("missing -n option")

    return new_path


def delete_file(directory):
    """
    This function deletes a file in the specified directory.
    It checks if the path is a file and if the file has a '.dsu'
    extension. If both conditions are met, it deletes the file
    and prints a confirmation message. If any of the conditions
    are not met, it prints an error message.
    """
    if directory.is_file():
        if directory.suffix == '.dsu':
            file_name = directory
            directory.unlink()
            print(f'{file_name} DELETED')
        else:
            print("ERROR")
    else:
        print("ERROR")


def read_file(directory):
    """
    This function reads a file in the specified directory.
    It checks if the path is a file and if the file has a
    '.dsu' extension. If both conditions are met, it reads
    the file and prints its content. If the file is empty,
    it prints a message indicating that the file is empty.
    If any of the conditions are not met, it prints an error
    message.
    """
    if directory.is_file():
        if directory.suffix == '.dsu':
            with open(directory, 'r') as file:
                content = file.read()
                if not content:
                    print("empty file")
                else:
                    print(content.strip())
        else:
            print("not a dsu file")
    else:
        print("not a file")


def open_dsu_file(directory):
    """
    This function opens a '.dsu' file in the specified directory.
    It checks if the path is a file and if the file has a
    '.dsu' extension. If both conditions are met, it attempts
    to load the file into a Profile object. If the file does not
    follow the Profile format, it raises an exception.
    If any of the conditions are not met, it raises an
    appropriate exception.
    """
    if directory.is_file():
        if directory.suffix == '.dsu':
            try:
                # instantiate a new profile object
                journal = Profile()
                # load the profile from the file system into the object
                journal.load_profile(directory)
                return journal
            except DsuProfileError:
                print("File does not follow Profile format.")
                raise Exception
        else:
            raise Exception("not a .dsu file")
    else:
        raise Exception("could not open the file")


def edit_dsu_file(journal: Profile, dsu_path: str, command=None, args=None):
    """
    This function edits a '.dsu' file based on the provided command
    and arguments. The arguments can be used to specify the username,
    password, bio, posts, and other profile details.
    """
    if command.lower() == 'q':
        return

    elif command.lower() == 'e':
        if '-usr' in args:
            username = get_argument_value(args, '-usr')
            journal.username = username
            journal.save_profile(dsu_path)
        if '-pwd' in args:
            pwd = get_argument_value(args, '-pwd')
            journal.password = pwd
            journal.save_profile(dsu_path)
        if '-bio' in args:
            bio = get_argument_value(args, '-bio')
            journal.bio = bio
            journal.save_profile(dsu_path)
        if '-addpost' in args:
            post_content = get_argument_value(args, '-addpost')
            word_list = post_content.split()
            if '@weather' in word_list:
                weather = OpenWeather('92697', 'US')
                weather.set_apikey("9c81c43b728ea74cde192277e6a7c141")
                try:
                    weather.load_data()
                    post_content = weather.transclude(post_content)
                except Exception as e:
                    print(f"An error occured while"
                          f"loading the weather data: {e}")

            if '@lastfm' in word_list:
                lastfm = LastFM("Frank+Ocean")
                lastfm.set_apikey('5408974569119b2838a20277a9290976')
                try:
                    lastfm.load_data()
                    post_content = lastfm.transclude(post_content)
                except Exception as e:
                    print(f"An error occured while"
                          f"loading the lastfm data: {e}")

            post = Post(post_content)
            journal.add_post(post)
            journal.save_profile(dsu_path)
        if '-delpost' in args:
            index = args[args.index('-delpost') + 1]
            journal.del_post(index)
            journal.save_profile(dsu_path)
        if '-publish' in args:
            if journal.dsuserver is None:
                IP = input("Enter the server ip: ")
                journal.dsuserver = IP
                journal.save_profile(dsu_path)
            for arg in args:
                if arg.isdigit():
                    index = int(arg)
                    break
            post = journal.get_posts()[index]["entry"]
            send(journal.dsuserver, 3021, journal.username,
                 journal.password, post, journal.bio)
        if '-publishbio' in args:
            new_bio = get_argument_value(args, '-publishbio')
            if journal.dsuserver is None:
                IP = input("Enter the server ip: ")
                journal.dsuserver = IP
                journal.save_profile(dsu_path)
            send(journal.dsuserver, 3021, journal.username,
                 journal.password, None, new_bio)

        return

    elif command.lower() == 'p':
        if '-usr' in args:
            print(f'Your username is {journal.username}\n')
        if '-pwd' in args:
            print(f'Your password is {journal.password}\n')
        if '-bio' in args:
            print(f'Your bio is {journal.bio}\n')
        if '-posts' in args:
            get_all_posts(journal)
        if '-post' in args:
            try:
                id = get_argument_value(args, '-post')
                print(journal.get_posts()[int(id)]["entry"])
            except IndexError:
                print("Index out of bounds. Please try again.")
        if '-all' in args:
            print(f'The saved dsuserver is {journal.dsuserver}')
            print(f'Your username is {journal.username}')
            print(f'Your password is {journal.password}')
            print(f'Your bio is {journal.bio}')
            print('Your posts are:')
            get_all_posts(journal)
        return


# get the value of the argument after the "-xxx" command including spaces
def get_argument_value(args, command):
    """
    This function retrieves the value of a specified command
    from a list of arguments. It finds the index of the command
    in the list, then finds the index of the next command. The value of
    the specified command is the arguments between these two indices.
    If the command is not found in the list, the function returns None.
    """
    if command in args:
        start_index = args.index(command) + 1
        end_index = next((i for i,
                          arg in enumerate(args[start_index:],
                                           start=start_index)
                          if arg.startswith('-')), len(args))
        value = ' '.join(args[start_index:end_index])
        # get the value of the argument after the
        # "-xxx" command including spaces
        return value.strip('\'"')
    else:
        return None


def get_all_posts(journal):
    """
    This function retrieves all posts from a journal object.
    It prints each post's index, content, and timestamp.
    """
    posts = journal.get_posts()
    i = 0
    for post in posts:
        print(f'{i}: {post["entry"]}\nTimestamp: {post["timestamp"]}')
        i += 1


def check_spaces(input):
    """
    This function checks if the input is only spaces or is empty.
    If the input is only spaces or is empty, it prints an error
    message and returns False. Otherwise, it returns True.
    """
    if input.isspace():
        print('Input cannot be only spaces')
        return False
    if input == '':
        print('Input cannot be empty')
        return False
    return True


def check_input(input):
    """
    This function checks if the input is valid.
    It checks if the input is empty, contains spaces, or is only spaces.
    If any of these conditions are met, it prints an error message and
    returns False. Otherwise, it returns True.
    """
    if input == '':
        print('Input cannot be empty')
        return False
    if ' ' in input:
        print('Input cannot contain spaces')
        return False
    if input.isspace():
        print('Input cannot be only spaces')
        return False
    return True
