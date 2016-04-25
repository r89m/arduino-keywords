import os
from os.path import join

import unittest
from unittest.mock import call, patch, mock_open

from arduinokeywords import parse_header, parse_library, output_keywords, find_header_files, get_keywords_fullpath

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

PATCH_OPEN_PATH = "arduinokeywords.arduinokeywords.open"

class TestHeaderParser(unittest.TestCase):

    def testParseSimpleHeader(self):

        test_header_path = join(THIS_DIR, "samples", "SimpleHeader", "SimpleHeader.h")

        expected_class = "SimpleClass"
        expected_methods = ["publicMethod", "publicIntMethod", "publicMethodWithInt"]

        parsed_header = parse_header(test_header_path)

        test_class = parsed_header[0]

        self.assertEqual(expected_class, test_class.name)
        self.assertListEqual(sorted(expected_methods), sorted(test_class.get_methods()))

    def testParseMalformedHeader(self):

        test_header_path = join(THIS_DIR, "samples", "MalformedHeader", "MalformedHeader.h")

        expected_classes = []

        self.assertListEqual(expected_classes, parse_header(test_header_path))

    def testParseHeaderWithMultipleClasses(self):

        test_header_path = join(THIS_DIR, "samples", "MultipleClasses", "MultipleClasses.h")

        expected_a_name = "ClassA"
        expected_b_name = "ClassB"
        expected_a_methods = ["publicAMethod", "publicAIntMethod", "publicAMethodWithInt"]
        expected_b_methods = ["publicBMethod", "publicBIntMethod", "publicBMethodWithInt"]

        parsed_header = parse_header(test_header_path)

        # Assign the classes to the right variables
        for check_class in parsed_header:
            if check_class.name == expected_a_name:
                class_a = check_class
            elif check_class.name == expected_b_name:
                class_b = check_class

        self.assertEqual(expected_a_name, class_a.name)
        self.assertEqual(expected_b_name, class_b.name)

        self.assertListEqual(sorted(expected_a_methods), sorted(class_a.get_methods()))
        self.assertListEqual(sorted(expected_b_methods), sorted(class_b.get_methods()))

    def testSearchLibraryForHeadersAtRootLevel(self):

        test_library_path = join(THIS_DIR, "samples", "DeepClasses")

        expected_header_files = ["ClassA.h", "ClassB.h"]
        expected_header_files = [join(test_library_path, f) for f in expected_header_files]

        found_headers = find_header_files(test_library_path)

        self.assertListEqual(sorted(expected_header_files), sorted(found_headers))

    def testSearchLibraryForHeadersWithDepth2(self):

        test_library_path = join(THIS_DIR, "samples","DeepClasses")

        expected_header_files = ["ClassA.h", "ClassB.h", join("DeepOne", "ClassC.h")]
        expected_header_files = [join(test_library_path, f) for f in expected_header_files]

        found_headers = find_header_files(test_library_path, 2)

        self.assertListEqual(sorted(expected_header_files), sorted(found_headers))

    def testSearchLibraryForHeadersWithDepth4(self):

        test_library_path = join(THIS_DIR, "samples","DeepClasses")

        expected_header_files = ["ClassA.h", "ClassB.h", join("DeepOne", "ClassC.h"),
                                 join("DeepOne", "DeepTwo", "ClassD.h"),
                                 join("DeepOne", "DeepTwo", "DeepThree", "ClassE.h")]

        expected_header_files = [join(test_library_path, f) for f in expected_header_files]

        found_headers = find_header_files(test_library_path, 4)

        self.assertListEqual(sorted(expected_header_files), sorted(found_headers))

    def testParseLibraryWithSingleRootLevelHeader(self):

        test_library_path = join(THIS_DIR, "samples", "SimpleHeader")
        expected_classes = ["SimpleClass"]

        parsed_classes = parse_library(test_library_path)
        retrieved_classes = sorted([c.name for c in parsed_classes])

        self.assertListEqual(expected_classes, retrieved_classes)

    def testParseLibraryWithMultipleRootLevelHeaders(self):

        test_library_path = join(THIS_DIR, "samples", "DeepClasses")
        expected_classes = ["ClassA", "ClassB"]

        parsed_classes = parse_library(test_library_path)
        retrieved_classes = sorted([c.name for c in parsed_classes])

        self.assertListEqual(expected_classes, retrieved_classes)

    def testParseLibraryWithMultipleHeadersOverSeveralDirectories_MaxDepth2(self):

        test_library_path = join(THIS_DIR, "samples", "DeepClasses")
        expected_classes = ["ClassA", "ClassB", "ClassC"]

        parsed_classes = parse_library(test_library_path, max_depth=2)
        retrieved_classes = sorted([c.name for c in parsed_classes])

        self.assertListEqual(expected_classes, retrieved_classes)

    def testParseLibraryWithMultipleHeadersOverSeveralDirectories_MaxDepth4(self):

        test_library_path = join(THIS_DIR, "samples", "DeepClasses")
        expected_classes = ["ClassA", "ClassB", "ClassC", "ClassD", "ClassE"]

        parsed_classes = parse_library(test_library_path, max_depth=4)
        retrieved_classes = sorted([c.name for c in parsed_classes])

        self.assertListEqual(expected_classes, retrieved_classes)

    def testGetKeywordsPath_WithFilename(self):

        keywords_filename = join(THIS_DIR, "samples", "keywords.txt")
        expected_result = os.path.abspath(keywords_filename)

        self.assertEqual(expected_result, get_keywords_fullpath(keywords_filename))

    def testGetKeywordsPath_WithoutFilename(self):

        keywords_filename = join(THIS_DIR, "samples")
        expected_result = join(os.path.abspath(keywords_filename), "keywords.txt")

        self.assertEqual(expected_result, get_keywords_fullpath(keywords_filename))

    def testWritingKeywordsTxtFile(self):

        m = mock_open()
        with patch(PATCH_OPEN_PATH, m, create=True):

            test_keywords_filename = "keywords.txt"
            test_library_path = join(THIS_DIR, "samples", "SimpleHeader")
            test_calls = [
                call(test_keywords_filename, 'w+'),
                call().__enter__(),
                call().write("SimpleClass\tKEYWORD1"),
                call().write('\n'),
                call().write('publicIntMethod\tKEYWORD2'),
                call().write('\n'),
                call().write('publicMethod\tKEYWORD2'),
                call().write('\n'),
                call().write('publicMethodWithInt\tKEYWORD2'),
                call().write('\n'),
                call().__exit__(None, None, None)
            ]

            classes = parse_library(test_library_path)

            output_keywords(classes, test_keywords_filename)

            m.assert_has_calls(test_calls)

    def testWritingKeywordsTxtFileWithAdditionalMethodsAndConstants(self):

        m = mock_open()
        with patch(PATCH_OPEN_PATH, m, create=True):

            test_keywords_filename = "keywords.txt"
            test_library_path = join(THIS_DIR, "samples", "SimpleHeader")
            test_calls = [
                call(test_keywords_filename, 'w+'),
                call().__enter__(),
                call().write("SimpleClass\tKEYWORD1"),
                call().write('\n'),
                call().write('publicIntMethod\tKEYWORD2'),
                call().write('\n'),
                call().write('publicMethod\tKEYWORD2'),
                call().write('\n'),
                call().write('publicMethodWithInt\tKEYWORD2'),
                call().write('\n'),
                call().write('const1\tLITERAL1'),
                call().write('\n'),
                call().write('const2\tLITERAL1'),
                call().write('\n'),
                call().__exit__(None, None, None)
            ]

            classes = parse_library(test_library_path)

            additional_constants = ["const1", "const2"]

            output_keywords(classes, test_keywords_filename, additional_constants)

            m.assert_has_calls(test_calls)
