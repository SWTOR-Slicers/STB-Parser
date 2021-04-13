# -*- coding: utf-8 -*-

import os


def parse_extraction_file_name(file_path, work_dir, save_dir):
    # Take the current file being processed and create a separate
    # text file for saving the strings

    # Create file name
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Compose part of new name based on the location of the original
    dir_extension = os.path.dirname(file_path).replace(work_dir, '').replace(chr(92), '-')

    # Compose new file name and path
    extraction_path = save_dir + 'decoded_' + dir_extension + '-' + file_name +'.txt'
    return extraction_path


def parse_stb(stb_file, decoded_file):

    # Grab file content
    file_buffer = stb_file.read()

    # Initialize seeker cursor
    seek_track = 0

    # Grab the number of strings  in the file, skip header 10 00 00
    string_num = int.from_bytes(file_buffer[seek_track + 3: seek_track + 7],
         "little", signed=False)

    # Initialize cursor to the next byte location after string number
    seek_track = 7

    # Initialize string counter
    string_track = 0

    while string_track != string_num:
        # Get string ID, might be useful for cross-referencing
        string_id = int.from_bytes(file_buffer[seek_track:seek_track + 8],
            "little", signed=False)
        seek_track = seek_track + 8

        # Grab first text type byte - main/secondary/alternate toggle
        type_one = file_buffer[seek_track]
        seek_track = seek_track + 1

        # Grab second text type byte - possible localization toggle
        type_two = file_buffer[seek_track]
        seek_track = seek_track + 1

        # Grab text speed float - currently useless
        text_speed = file_buffer[seek_track: seek_track + 4]
        seek_track = seek_track + 4

        # Get string length
        string_offset = int.from_bytes(file_buffer[seek_track: seek_track
            + 4], "little", signed=False)
        seek_track = seek_track + 4

        # Get string location in the file
        string_location = int.from_bytes(file_buffer[seek_track: seek_track
            + 4], "little", signed=False)
        seek_track = seek_track + 4

        # Get string repetition length - unknown use
        string_repeat = int.from_bytes(file_buffer[seek_track: seek_track
            + 4], "little", signed=False)
        seek_track = seek_track + 4

        # Get text string data and decode it
        text_string = file_buffer[string_location: string_location +
            string_offset]
        try:
            decoded_file.write(text_string.decode('ANSI') + '\n')
        except:
            continue
        string_track = string_track + 1


def main():

    working_dir = r'' # Define directory from where the STB files are read
    save_dir = r' ' # Define directory to save files

    # Iterate over file list, check for STB files and run extraction
    for root, dirs, file_list in os.walk(working_dir, topdown = False):
        for filename in file_list:
            if filename.endswith('.stb'):
                reader_path = os.path.join(root, filename)
                reader = open(reader_path, 'rb')
                writer = open(parse_extraction_file_name(reader_path, working_dir, save_dir), 'ta+')
                try:
                    parse_stb(reader, writer)
                finally:
                    reader.close()
                    writer.close()
            else:
                continue


if __name__ == "__main__":
    main()