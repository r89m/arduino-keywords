# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os

import fnmatch
import glob

import CppHeaderParser

KEYWORDS_FILENAME = u"keywords.txt"
KEYWORD_SEP = u"\t"
KEYWORD_FORMAT_CLASS = u"{{class_name}}{separator}KEYWORD1".format(separator=KEYWORD_SEP)
KEYWORD_FORMAT_METHOD = u"{{method}}{separator}KEYWORD2".format(separator=KEYWORD_SEP)
KEYWORD_FORMAT_CONSTANT = u"{{constant}}{separator}LITERAL1".format(separator=KEYWORD_SEP)


class ClassKeywords:

    def __init__(self, name, filename=None):
        self.name = name
        self.filename = filename
        self._methods = []

    def add_method(self, method_name):
        self._methods.append(method_name)

    def get_methods(self):
        return sorted(set(self._methods))


def parse_library(library_path, max_depth=1):

    header_files = find_header_files(library_path, max_depth)

    classes = []

    for header in header_files:
        classes.extend(parse_header(header))

    return classes


def find_header_files(library_path, max_depth=1):

    header_files = []

    # Max depth script borrowed from John Scmiddt (http://stackoverflow.com/a/17056922)
    for d in range(1, max_depth + 1):
        maxGlob = "/".join("*" * d)
        topGlob = os.path.join(library_path, maxGlob)
        allFiles = glob.glob(topGlob)
        for file in allFiles:
            if fnmatch.fnmatch(os.path.basename(file), '*.h'):
                header_files.append(file)

    return header_files


def parse_header(header_path):
    try:
        cpp_header = CppHeaderParser.CppHeader(header_path)

        classes = []

        for class_name, header_class in cpp_header.classes.items():
            keyword_class = ClassKeywords(class_name, header_path)
            for method in header_class["methods"]["public"]:
                # Ignore constructors and destructors
                if not (method["constructor"] or method["destructor"]):
                    keyword_class.add_method(method["name"])

            classes.append(keyword_class)

        return classes

    except CppHeaderParser.CppParseError as e:
        print(e)
        return []


def get_keywords_fullpath(keywords_path):

    if(os.path.isdir(keywords_path)):
        keywords_path = os.path.join(keywords_path, KEYWORDS_FILENAME)
    else:
        keywords_path = keywords_path

    return os.path.abspath(keywords_path)


def output_keywords(classes, keywords_file, additional_constants=None):

    for output_class in classes:
        keywords_file.write(KEYWORD_FORMAT_CLASS.format(class_name=output_class.name))
        keywords_file.write("\n")
        for method in output_class.get_methods():
            keywords_file.write(KEYWORD_FORMAT_METHOD.format(method=method))
            keywords_file.write("\n")

    if additional_constants is not None:
        for constant in additional_constants:
            keywords_file.write(KEYWORD_FORMAT_CONSTANT.format(constant=constant))
            keywords_file.write("\n")



