import ast
import difflib
import os
import re

import astunparse


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list and x != "":
            unique_list.append(x)

    return unique_list


def find_and_replace_in_file(file_path, search_pattern, replacement):
    # Open the file in read mode
    with open(file_path, "r") as file:
        # Read the entire contents of the file
        contents = file.read()

    # Compile the regular expression pattern
    pattern = re.compile(search_pattern)

    # Use the re.sub() function to find and replace all occurrences of the pattern in the file contents
    modified_contents = re.sub(pattern, replacement, contents)

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write the modified contents back to the file
        file.write(modified_contents)


def fix_unicode_escapes(source):
    # Find all \UXXXXXXXX escape sequences
    regex = r"\\U[0-9A-Fa-f]{8}"
    matches = re.finditer(regex, source)

    # Replace each escape sequence with a question mark
    for match in matches:
        source = source[:match.start()] + "?" + source[match.end():]

    return source


def organize_functions(filename, start_line, end_line):
    # Read the source code from the file
    with open(filename, 'r') as f:
        source = f.read()

    # Fix any invalid Unicode escape sequences
    source = fix_unicode_escapes(source)

    # Parse the source code into an AST
    tree = ast.parse(source)

    # Find all function definitions in the AST
    function_defs = [node for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]

    # Sort the function definitions alphabetically by name
    function_defs.sort(key=lambda x: x.name)

    # Create a new AST with the sorted function definitions
    new_tree = ast.Module(body=function_defs)

    # Convert the new AST back into source code
    new_source = astunparse.unparse(new_tree)

    # Split the original source code into lines
    lines = source.split("\n")

    # Replace the lines containing the asynchronous functions with the sorted source code
    lines[start_line - 1:end_line] = new_source.split("\n")

    # Join the lines back into a single string
    new_source = "\n".join(lines)

    # Write the modified source code back to the original file
    with open(filename, 'w') as f:
        f.write(new_source)


def write_dict_to_files(dictionary, directory):
    # create the directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    for key, value in dictionary.items():
        # create a new file with the key as the file name
        with open(os.path.join(directory, key + ".txt"), "w") as f:
            # write the value to the file
            f.write(value)


def find_most_similar_string(string_list, input_string):
    # Create a SequenceMatcher object to compare the input string to each string in the list
    matcher = difflib.SequenceMatcher()
    matcher.set_seq1(input_string)

    # Initialize variables to keep track of the most similar string and its similarity ratio
    most_similar_string = None
    highest_similarity_ratio = 0

    # Iterate through the list of strings
    for string in string_list:
        # Set the second sequence to compare to the input string
        matcher.set_seq2(string)

        # Calculate the similarity ratio
        similarity_ratio = matcher.ratio()
        # If the similarity ratio is higher than the current highest, update the most similar string and highest similarity ratio
        if similarity_ratio > highest_similarity_ratio:
            highest_similarity_ratio = similarity_ratio
            most_similar_string = string

    # print(highest_similarity_ratio)
    # Return the most similar string
    return most_similar_string


replace_words = ["Scenario:", "Effect:", "Trigger:", "Condition:", "Details:", "Lore - ",
                 "Bonus:", "Description:", "Example:", "On Success:", "On Failure:"]


def segment_list(text):
    paragraphs = text.split(", ")  # Splits the text by paragraphs
    messages = []  # Array of individual messages that the bot will send to make up the task
    txt_block = ""
    for block in paragraphs:
        if len(txt_block + block) >= 1999:
            messages.append(txt_block)
            txt_block = ""
        txt_block += block + ", "
    messages.append(txt_block)
    return messages


def segment_text(text, flag=None):
    paragraphs = text.split("\n")  # Splits the text by paragraphs
    if "Request" not in paragraphs[0] and flag == "Legend":
        first_temp = paragraphs[1]
        paragraphs[1] = "__**" + first_temp + "**__"
    for i in range(len(paragraphs)):
        if "Boss Ability" in paragraphs[i] or "Trainer Ability" in paragraphs[i]:
            temp = paragraphs[i]
            second_temp = paragraphs[i + 1]
            paragraphs[i] = "**" + temp + "**"
            paragraphs[i + 1] = "*" + second_temp + "*"
        for word in replace_words:
            scen_temp = paragraphs[i].replace(word, "**" + word + "**")
            paragraphs[i] = scen_temp

    messages = []  # Array of individual messages that the bot will send to make up the task
    txt_block = ""
    for block in paragraphs:
        if len(txt_block + block) > 2000:
            messages.append(txt_block)
            txt_block = ""
        txt_block += block + "\n"
    messages.append(txt_block)
    return messages


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = []
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            temp = ''
            for elem in elements:
                temp += read_paragraph_element(elem)
            if "Prerequisite:" in temp and not temp.startswith("P"):
                temp_t = temp.split("Prerequisite:")
                text.append(temp_t[0][:-1])
                temp = "\nPrerequisite:" + temp_t[1]
            text.append(temp)
    return text


def make_text(words):
    """Return textstring output of get_text("words").
    Word items are sorted for reading sequence left to right,
    top to bottom.
    """
    line_dict = {}  # key: vertical coordinate, value: list of words
    words.sort(key=lambda w: w[0])  # sort by horizontal coordinate
    for w in words:  # fill the line dictionary
        y1 = round(w[3], 1)  # bottom of a word: don't be too picky!
        word = w[4]  # the text of the word
        line = line_dict.get(y1, [])  # read current line content
        line.append(word)  # append new word
        line_dict[y1] = line  # write back to dict
    lines = list(line_dict.items())
    lines.sort()  # sort vertically
    return " ".join([" ".join(line[1]) for line in lines])


def search_cell_value(data, name):
    # Compile the regex pattern
    regex = re.compile('(?i)^' + name + "$")

    # Get the sheet data
    sheet_data = data["Encounter Slots"]

    # Create a list to store the matching keys
    matching_keys = []

    # Iterate over the columns in the sheet
    for key, nested_dict in sheet_data.items():
        # Iterate over the cells in the column
        for row_num, (val, comment, treasure_tag) in nested_dict.items():
            # If the cell value matches the regex pattern, add the key to the list
            if regex.match(val):
                matching_keys.append(key)

    # If there are no matching keys, find the most similar value
    if not matching_keys:
        # Get a list of all the values in the sheet
        all_values = [val for nested_dict in sheet_data.values() for row_num, (val, comment) in nested_dict.items()]

        # Find the most similar value
        most_similar_value = find_most_similar_string(all_values, name)

        return ["NO MATCH FOUND", most_similar_value]
    return matching_keys


def create_item_list(items_string):
    items = []
    lines = items_string.split('\n')
    for line in lines:
        # Use a regular expression to remove the number from the beginning of the line
        item = re.sub(r'^\d+\s+', '', line)
        items.append(item)
    return items


def find_largest_smaller_number(numbers, x):
    largest_smaller_number = None
    # Iterate over the numbers in the list
    for number in numbers:
        # Check if the number is smaller than x and (either largest_smaller_number is not set or the number is greater than largest_smaller_number)
        if number < x and (largest_smaller_number is None or number > largest_smaller_number):
            largest_smaller_number = number
    return largest_smaller_number


def exclusion(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
