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