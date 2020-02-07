def compress_file_to(source_filename, target_filename):
    file = open(source_filename)
    text_list = file.read().split('\n')
    file.close()
    remove_lines = []
    # check every line
    for line_index in range(len(text_list)):
        line = text_list[line_index]
        first_non_space = -1
        #   find the first character in the line that is not a space or tab
        for char in line:
            if not(char == ' ' or char == '\t'):
                first_non_space = line.index(char)
                break
        if first_non_space == -1:
            #   if the line is empty or consists out of only spaces/tabs
            remove_lines.insert(0, line_index)
        else:
            text_list[line_index] = line[first_non_space:]
    #   remove all the empty lines
    for line_index in remove_lines:
        text_list.pop(line_index)
    #   write to the new file
    with open(target_filename, 'w') as f:
        for item in text_list:
            f.write("%s\n" % item)


if __name__ == "__main__":
    compress_file_to("uncompressed.txt", "compressed.txt")
