import textract


def parse_file(path_to_file, encoding_for_return="utf-8"):
    """
    Method parses the file and returns the contents as a string with the specified encoding.
    :param path_to_file: path to file for parse by textract
    :param encoding_for_return: encoding of the returned string (textract.process return 'bytes')
    :return: string
    """
    text = textract.process(path_to_file)
    return text.decode(encoding_for_return)


if __name__ == "__main__":
    ...