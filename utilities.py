import ast
import difflib
import os
import re

import astunparse


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

    # Return the most similar string
    return most_similar_string


replace_words = ["Scenario:", "Effect:", "Trigger:", "Condition:", "Details:", "Lore - ",
                 "Bonus:", "Description:", "Example:", "On Success:", "On Failure:"]


def segment_list(text):
    paragraphs = text.split(", ")  # Splits the text by paragraphs
    messages = []  # Array of individual messages that the bot will send to make up the task
    txt_block = ""
    for block in paragraphs:
        if len(txt_block + block) > 2000:
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
