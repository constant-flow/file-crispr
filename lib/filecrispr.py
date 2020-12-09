#!/usr/bin/python3

from shutil import copyfile
import os
import math
import pathlib

fallbackValue = "(content not found)"
temporary_filename = "___temp_crispr_file___"
crispr_marker = "___crispr"


def modeToFileWrite(mode):
    file_write_mode = "a"
    if mode == 0:
        file_write_mode = "w"
    return file_write_mode


def file_read_line(filepath,
                   lineNumber,
                   first_line_id_is_zero=False,
                   fallback=fallbackValue):
    """Reads the content of a line from a file.\n
    If not existent it returns the provided fallback value"""
    count = 0
    if first_line_id_is_zero:
        count: -1
    with open(filepath) as fp:
        Lines = fp.readlines()
        for line in Lines:
            count += 1
            if count == lineNumber:
                return line.replace("\n", "")
    return fallback


def file_get_extension(filepath,
                       with_extension_dot=False,
                       only_last_extension=False):
    """returns the extension of a file by a provided filepath\n
    with_extension_dot (default: False): True, will include the dot e.g. '.txt'\n
    only_last_extension (default: False): True, returns only the last extension e.g. 'gz' instead of 'tar.gz'
    """

    if only_last_extension:
        return pathlib.Path(filepath).suffix[(0 if with_extension_dot else 1):]
    else:
        return "".join(
            pathlib.Path(filepath).suffixes)[(0 if with_extension_dot else 1):]


def file_write_string(filepath, string_to_write, mode=1):
    """
    Writes a string to a file\n
    mode: if 1 (default) content will be appended, if 0 content will be overwritten
    """
    file_write_mode = modeToFileWrite(mode)
    file_output = open(filepath, file_write_mode)
    file_output.write(string_to_write)
    file_output.close()


def file_find_string_pos(filepath, search_string, start=0):
    """Returns the position of a string in a file.\n
    If not found it returns -1"""
    with open(filepath, 'rb') as f:
        file_size = os.path.getsize(filepath)
        buffer_size = 4096
        buffer = None
        if start > 0:
            f.seek(start)
        overlap = len(search_string) - 1
        while True:
            if (f.tell() >= overlap and f.tell() < file_size):
                f.seek(f.tell() - overlap)
            buffer = f.read(buffer_size)
            if buffer:
                pos = buffer.find(search_string.encode())
                if pos >= 0:
                    return f.tell() - (len(buffer) - pos)
            else:
                return -1


def get_line_comment_symbol_for_filetype(extension_without_dot,
                                         fallback_comment_symbol,
                                         trailing_symbol=" "):
    extensions = {
        "js": "//",
        "jsx": "//",
        "sw": "//",
        "java": "//",
        "h": "//",
        "c": "//",
        "hpp": "//",
        "cpp": "//",
        "md": "#",
        "r": "#",
        "php": "#",
        "ps": "#",
        "py": "#",
        "rb": "#",
        "sql": "--",
        "scpt": "--",
        "scptd": "--",
        "applescript": "--",
        "lua": "--",
        "tex": "%",
        "m": "%",
        "basic": "REM",
    }

    return extensions.get(extension_without_dot,
                          fallback_comment_symbol) + trailing_symbol


def file_replace_line(filepath,
                      line_nr_to_replace,
                      new_line_content,
                      first_line_id_is_zero=False,
                      temporary_filename=temporary_filename):
    """
    Replaces the content of one line (specified by number), with a new content (new_line_content)
    """

    # file_remove(temporary_filename)
    file_output = open(temporary_filename, "w")

    # line indexing
    current_line = 0
    if not first_line_id_is_zero:
        current_line = 1

    line_start_found = False
    copy_chars = True

    with open(filepath) as file_input:
        while True:
            read_char = file_input.read(1)
            if not read_char:
                break

            if not line_start_found and current_line == line_nr_to_replace:
                line_start_found = True
                copy_chars = False
                file_output.write(new_line_content)
                file_output.write("\n")

            if line_start_found and current_line == line_nr_to_replace + 1:
                copy_chars = True

            if read_char == '\n':
                current_line = current_line + 1

            if copy_chars:
                file_output.write(read_char)

    file_output.close()

    file_remove(filepath)
    file_copy(temporary_filename, filepath)
    file_remove(temporary_filename)


def file_line_comment_symbol(filepath, line_comment_string=0):
    # automatic comment symbol based on extention
    if line_comment_string == 0:
        extension = file_get_extension(filepath)
        return get_line_comment_symbol_for_filetype(extension, "//?")
    else:  # manually specified char/string to start a comment
        return line_comment_string


def file_comment_line(filepath,
                      line_to_comment_out,
                      line_comment_string=0,
                      first_line_id_is_zero=False,
                      temporary_filename=temporary_filename):
    """Comments on line out in a provided file\n
    line_to_comment_out: specifies the line number to comment\n
    line_comment_string: how to comment out, 0 is default will base it on the file type. Else provide the prefix that will comment the line out\n
    first_line_id_is_zero: default is False. If true first line is indexed by line_to_comment_out=0.
    """

    comment_symbol = file_line_comment_symbol(filepath, line_comment_string)
    content_commented_line = comment_symbol + file_read_line(
        filepath, line_to_comment_out, first_line_id_is_zero)

    file_replace_line(filepath, line_to_comment_out, content_commented_line,
                      first_line_id_is_zero, temporary_filename)


def file_uncomment_line(filepath,
                        line_to_uncomment,
                        line_comment_string=0,
                        first_line_id_is_zero=False,
                        temporary_filename=temporary_filename):
    """Uncomments a line in in a provided file\n
    line_to_uncomment: specifies the line number to uncomment\n
    line_comment_string: how to uncomment, 0 is default will base it on the file type. Else provide the prefix that comments the line currently\n
    first_line_id_is_zero: default is False. If true first line is indexed by line_to_comment_out=0.
    """

    comment_symbol = file_line_comment_symbol(filepath, line_comment_string)
    content_of_line = file_read_line(filepath, line_to_uncomment,
                                     first_line_id_is_zero)
    if content_of_line == "": return

    new_content_of_line = content_of_line.replace(comment_symbol, "")
    # trim of spaces in the beginning of the line
    while new_content_of_line[0] == " ":
        new_content_of_line = new_content_of_line[1:]

    file_replace_line(filepath, line_to_uncomment, new_content_of_line,
                      first_line_id_is_zero, temporary_filename)


def file_transfer_bytes_n_to_m(filepath_source, filepath_target, n, m, mode=1):
    """Transfers all bytes/chars from n (inclusive) to m (exclusive) from file source to target\n
    mode: if 1 (default) content will be appended, if 0 content will be overwritten"""

    file_write_mode = modeToFileWrite(mode)
    file_output = open(filepath_target, file_write_mode)

    counter = 0
    with open(filepath_source) as file_input:
        while True:
            read_char = file_input.read(1)
            if not read_char:
                break

            if counter >= n and counter < m:
                file_output.write(read_char)
            counter = counter + 1

    file_output.close()


def file_erase_string(filepath,
                      string_to_erase,
                      times_to_erase=1,
                      temporary_filename=temporary_filename):
    """
    erases a string from a file\n
    times_to_erase: how often should the string be removed (=1 remove once (default), >0 defines the number of occurences to remove, <0 remove all occurences)\n
    temporary_filename: filename to temporarily save the output\n
    """
    file_replace_string(filepath, string_to_erase, "", times_to_erase,
                        temporary_filename)


def get_numbered_marker(id):
    """returns a numbered crispr marker"""
    return crispr_marker + str(id)


def crispr_mark(filepath,
                string_to_mark,
                times_to_mark=1,
                temporary_filename=temporary_filename):
    """
    marks a string in a file with unique crispr markers at each occurence of the string_to_mark\n
    times_to_mark: how often should the string be marked (=1 mark first (default), >0 defines the number of occurences to mark, <0 mark all occurences)\n
    temporary_filename: filename to temporarily save the output\n
    """

    marked_counter = 0

    if times_to_mark == 0:
        return marked_counter

    while True:
        crispr_marker_numbered = get_numbered_marker(marked_counter)
        marked = file_replace_string_once(filepath, string_to_mark,
                                          crispr_marker_numbered,
                                          temporary_filename)
        if not marked:
            break
        marked_counter = marked_counter + 1
        times_to_mark = times_to_mark - 1
        if times_to_mark == 0:
            break

    return marked_counter


def file_prepend_string_to_string(filepath,
                                  string_to_find,
                                  string_to_prepend,
                                  times_to_repeat=1,
                                  temporary_filename=temporary_filename):
    """
    searches a file for a string and prepends a provided string\n
    times_to_repeat: how often should the string be be prepended (=1 once (default), >0 defines the number of prepend actions, <0 prepends at every occurence)\n
    """

    return file_pre_and_append_string_to_string(filepath, string_to_find,
                                                string_to_prepend, "",
                                                times_to_repeat,
                                                temporary_filename)


def file_append_string_to_string(filepath,
                                 string_to_find,
                                 string_to_append,
                                 times_to_repeat=1,
                                 temporary_filename=temporary_filename):
    """
    searches a file for a string and appends a provided string\n
    times_to_repeat: how often should the string be be appended (=1 once (default), >0 defines the number of append actions, <0 appends at every occurence)\n
    """

    return file_pre_and_append_string_to_string(filepath, string_to_find, "",
                                                string_to_append,
                                                times_to_repeat,
                                                temporary_filename)


def file_pre_and_append_string_to_string(
        filepath,
        string_to_find,
        string_to_prepend,
        string_to_append,
        times_to_repeat=1,
        temporary_filename=temporary_filename):
    """
    searches a file for a string and appends a provided string\n
    times_to_repeat: how often should the string be be appended (=1 once (default), >0 defines the number of append actions, <0 appends at every occurence)\n
    """

    marked_count = crispr_mark(filepath, string_to_find, times_to_repeat)

    for i in range(marked_count):
        file_replace_string_once(
            filepath, get_numbered_marker(i),
            string_to_prepend + string_to_find + string_to_append,
            temporary_filename)


def file_replace_string(filepath,
                        string_to_replace,
                        string_to_place,
                        times_to_replace=1,
                        temporary_filename=temporary_filename):
    """
    replaces a string in a file\n
    times_to_replace: how often should the string be removed (=1 remove once (default), >0 defines the number of occurences to remove, <0 remove all occurences)\n
    temporary_filename: filename to temporarily save the output\n
    returns the ampunt of replacements/occurences
    """

    marked_count = crispr_mark(filepath, string_to_replace, times_to_replace)

    for i in range(marked_count):
        file_replace_string_once(filepath, get_numbered_marker(i),
                                 string_to_place, temporary_filename)

    return marked_count


def file_replace_string_once(filepath,
                             string_to_replace,
                             string_to_place,
                             temporary_filename=temporary_filename):
    """
    searches a file and replaces the first occurence of `string_to_replace` with `string_to_place\n`
    returns 1 if the string was found else 0
    """

    replaced_counter = 0
    position_in_string = file_find_string_pos(filepath, string_to_replace)

    if position_in_string == -1:
        return replaced_counter

    file_transfer_bytes_n_to_m(filepath, temporary_filename, 0,
                               position_in_string)
    if len(string_to_place) > 0:
        file_write_string(temporary_filename, string_to_place)

    file_transfer_bytes_n_to_m(filepath, temporary_filename,
                               position_in_string + len(string_to_replace),
                               math.inf)

    file_copy(temporary_filename, filepath)
    file_remove(temporary_filename)

    replaced_counter = 1

    return replaced_counter


###############################################
# File operations
###############################################


# Copies a file from src to dest path
def file_copy(file_path_source, file_path_destination):
    """Copies a file from `file_path_source` to `file_path_destination`"""
    copyfile(file_path_source, file_path_destination)


def file_remove(file_to_remove):
    """Removes a file at path `file_to_remove`"""
    os.remove(file_to_remove)
