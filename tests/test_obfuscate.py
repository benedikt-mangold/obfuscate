# -*- coding:utf-8 -*-
import os
import pickle
import re
import string
import unittest
import random
import pytest
from obfuscator.obfuscate import Obfuscator


__author__ = "Benedikt Mangold"
__copyright__ = "Benedikt Mangold"
__license__ = "MIT"



class TestObfuscator(unittest.TestCase):
    def setUp(self):
        seed = 42
        random.seed(seed)
        self.obfuscator = Obfuscator()

    def test_init(self):
        self.assertEqual(self.obfuscator._N, 12)

    def test_generate_random_chinese_character(self):
        value = self.obfuscator._generate_random_chinese_character().encode("utf-8")
        expected_value = b"\xe9\xbf\x98"
        self.assertEqual(expected_value, value)

    def test_strip_url(self):
        url = "the url is www.google.com and basta"
        value = self.obfuscator._strip_url(url)
        expected_value = "the url is  and basta"
        self.assertEqual(expected_value, value)

    def test_b26(self):
        value = self.obfuscator._bNN(
            87744431587408660, self.obfuscator._N, 26, chars=string.ascii_lowercase
        )
        expected_value = "motselsmroxx"
        self.assertEqual(expected_value, value)

    def test_b10(self):
        value = self.obfuscator._bNN(559585652290, self.obfuscator._N, 10, chars=string.digits)
        expected_value = "092256585955"
        self.assertEqual(expected_value, value)

    def test_update_mapping_dict_new_key_alpha_numeric(self):
        self.assertEqual(self.obfuscator._mapping_dict, {})
        self.obfuscator._generate_alpha_numeric_substring_mapping("myteststring")
        self.assertEqual({"myteststring": "brjphicetbnr"}, self.obfuscator._mapping_dict)

    def test_generate_alpha_numeric_substring_mapping_alpha_only(self):
        value = self.obfuscator._generate_alpha_numeric_substring_mapping("myteststring")
        expected_value = "brjphicetbnr"
        self.assertEqual(expected_value, value)

    def test_generate_alpha_numeric_substring_mapping_alphanumeric(self):
        test_string = "myteststring1"
        value = self.obfuscator._generate_alpha_numeric_substring_mapping(test_string)
        expected_value = "brephb3jtcirn"
        self.assertEqual(expected_value, value)
        self.assertEqual(len(expected_value), len(test_string))

    def test_generate_hash(self):
        value = self.obfuscator._generate_hash("myteststring1")
        expected_value = "r9ssjevh142h"
        self.assertEqual(expected_value, value)
        self.assertEqual(self.obfuscator._N, len(value))

    def test_update_mapping_dict_new_key_hash(self):
        test_string = "myteststring1"
        self.assertEqual(self.obfuscator._mapping_dict, {})
        hash_string = self.obfuscator._generate_hash(test_string)
        self.assertEqual(self.obfuscator._mapping_dict, {test_string: "r9ssjevh142h"})
        self.assertEqual(len(hash_string), len(self.obfuscator._mapping_dict[test_string]))

    def test_generate_chinese_substring_mapping_chinese_only(self):
        value = self.obfuscator._generate_chinese_substring_mapping("我来到北京清华大学").encode("utf-8")
        expected_value = (
            b"\xe9\xbf\x98 \xe5\xb1\x80\xe5\x84\xb3 \xe7\x84\xb4\xe6\xb5\x98 "
            b"\xe6\xaa\x92\xe5\xbf\x9c\xe5\xac\x9e\xe9\x8f\x8e"
        )
        self.assertEqual(expected_value, value)

    def test_generate_chinese_substring_mapping_chinese_with_vietnamese(self):
        value = self.obfuscator._generate_chinese_substring_mapping("học 我来到北京清华大学")
        expected_value = "r9ssjevh142h"
        self.assertEqual(expected_value, value)

    def test_generate_chinese_substring_mapping_chinese_with_ascii(self):
        encoded_substring_list = [
            sub_string.encode("utf-8")
            for sub_string in self.obfuscator._generate_chinese_substring_mapping(
                "我来到北ABC京清华大学"
            ).split(" ")
        ]

        self.assertTrue(b"wlp" in encoded_substring_list)
        encoded_substring_list.remove(b"wlp")

        self.assertTrue(
            [
                re.search(u"[\u4e00-\u9fff]", sub_string.decode("utf-8")) is not None
                for sub_string in encoded_substring_list
            ]
        )

    def test_update_mapping_dict_new_key_chinese_mapping(self):
        test_string = "我来到北京清华大学"
        self.assertEqual(self.obfuscator._mapping_dict, {})
        hash_string = self.obfuscator._generate_chinese_substring_mapping(test_string)
        chinese_mapped_token_list = hash_string.split(" ")
        self.assertEqual(4, len(chinese_mapped_token_list))
        print(self.obfuscator._mapping_dict)
        self.assertTrue(hash_string in self.obfuscator._mapping_dict.values())
        self.assertTrue(
            all(
                hash_sub_string in self.obfuscator._mapping_dict.values()
                for hash_sub_string in chinese_mapped_token_list
            )
        )
        self.assertTrue(test_string in self.obfuscator._mapping_dict.keys())

    def test_generate_equivalent_new_key_chinese(self):
        test_string = "我来到北ABC京清华大学"
        value = self.obfuscator._generate_equivalent_new_key(test_string)
        self.assertTrue(re.search(u"[\u4e00-\u9fff]", value) is not None)

    def test_generate_equivalent_new_key_ascii(self):
        test_string = "mystring1"
        value = self.obfuscator._generate_equivalent_new_key(test_string)
        self.assertTrue(re.search(u"[\u4e00-\u9fff]", value) is None)
        self.assertTrue(value.isascii())

    def test_generate_equivalent_new_key_vietnamese(self):
        test_string = "học"
        value = self.obfuscator._generate_equivalent_new_key(test_string)
        self.assertTrue(re.search(u"[\u4e00-\u9fff]", value) is None)
        self.assertTrue(self.obfuscator._N, len(value))

    def test_split_by_punctuation_empty_space(self):
        test_string = "this is a string and-oem which is ok!"
        split_tuple_list = self.obfuscator._split_by_punctuation_empty_space(test_string)

        self.assertTrue(
            all(not is_sign for element, is_sign in split_tuple_list if element == "")
        )
        alpha_list = [element for element, is_sign in split_tuple_list if not is_sign]
        self.assertEqual(9, len([element for element in alpha_list if element != ""]))

    def test_split_by_punctuation_underscore(self):
        test_string = "qa_1234_sq is the keycode"
        split_tuple_list = self.obfuscator._split_by_punctuation_empty_space(test_string)
        value = "".join(tup[0] if tup[0] != "" else " " for tup in split_tuple_list)
        self.assertEqual(value, test_string)

    @pytest.mark.skip(reason="double emptyspaces are currently stripped out")
    def test_split_by_punctuation_double_empty_space(self):
        test_string = "qa_1234_sq is  the keycode"
        split_tuple_list = self.obfuscator._split_by_punctuation_empty_space(test_string)
        value = "".join(tup[0] if tup[0] != "" else " " for tup in split_tuple_list)
        print(value)
        self.assertEqual(value, test_string)

    @pytest.mark.skip(reason="emptyspaces after punctiation is not covered")
    def test_split_by_punctuation_double_empty_space(self):
        test_string = "qa_1234_sq is, the keycode"
        split_tuple_list = self.obfuscator._split_by_punctuation_empty_space(test_string)
        value = "".join(tup[0] if tup[0] != "" else " " for tup in split_tuple_list)
        print(value)
        self.assertEqual(value, test_string)

    def test_obfuscate_ascii(self):
        test_string = "qa_1234_sq is the keycode"
        value = self.obfuscator.obfuscate(test_string)
        expected = "ht_1489_ad cv koa cnmthkv"
        self.assertEqual(expected, value)

    def test_obfuscate_ascii_identical_token_remains_identical(self):
        test_string = "qa_1234_qa is the keycode"
        value = self.obfuscator.obfuscate(test_string)
        expected = "ht_1489_ht ad cvg kxixsoj"
        self.assertEqual(expected, value)

    def test_obfuscate_hash(self):
        test_string = "qa_1234_sq is the học"
        value = self.obfuscator.obfuscate(test_string)
        expected = "ht_1489_ad cv koa cn02uawbq9qt"
        self.assertEqual(expected, value)

    def test_obfuscate_chinese(self):
        test_string = "qa_1234_sq is the 来"
        value = self.obfuscator.obfuscate(test_string)
        expected = "ht_1489_ad cv koa 禍"
        self.assertEqual(expected, value)


class TestReverseObfuscation(unittest.TestCase):
    def setUp(self):
        seed = 42
        random.seed(seed)
        self.obfuscator = Obfuscator()
        self.test_string = "qa_1234_qa is the keycode"
        self.obfuscated_test_string = self.obfuscator.obfuscate(self.test_string)
        self.assertTrue("ad" in self.obfuscated_test_string)

    def test_reverse_obfuscation_dict_created(self):
        self.assertEqual(self.obfuscator._reverse_mapping_dict, {})
        _ = self.obfuscator.reverse_obfuscation("ad")
        expected_value = {v: k for k, v in self.obfuscator._mapping_dict.items()}
        self.assertEqual(expected_value, self.obfuscator._reverse_mapping_dict)

    def test_reverse_obfuscation_dict_updated(self):
        _ = self.obfuscator.reverse_obfuscation("ad")
        reversed_matching_dict_before_update = {v: k for k, v in self.obfuscator._mapping_dict.items()}
        reverse_dict_before_update = self.obfuscator._reverse_mapping_dict
        self.assertEqual(reversed_matching_dict_before_update, reverse_dict_before_update)

        second_test_string = "mein erster string"
        second_obfuscated_string = self.obfuscator.obfuscate(second_test_string)
        reversed_matched_dict_after_update = {v: k for k, v in self.obfuscator._mapping_dict.items()}

        self.assertTrue("hrif" in second_obfuscated_string)
        self.assertEqual(reversed_matching_dict_before_update, self.obfuscator._reverse_mapping_dict)

        _ = self.obfuscator.reverse_obfuscation("hrif")
        reverse_dict_after_update = self.obfuscator._reverse_mapping_dict

        self.assertEqual(reversed_matched_dict_after_update, reverse_dict_after_update)
        self.assertNotEqual(reversed_matched_dict_after_update, reversed_matching_dict_before_update)

    def test_error_for_unknown_tokens(self):
        with pytest.raises(ValueError):
            _ = self.obfuscator.reverse_obfuscation("blabla")

    def test_revese_obfuscation(self):
        self.assertEqual(self.test_string, self.obfuscator.reverse_obfuscation(self.obfuscated_test_string))


class TestPickling(unittest.TestCase):
    def setUp(self):
        seed = 42
        random.seed(seed)

    def test_pickling_obfuscator_class(self):
        of = Obfuscator()
        test_string = "qa_1234_qa is the keycode"
        _ = of.obfuscate(test_string)

        target_path_2 = os.path.join(os.path.dirname(__file__), '../test_data/test_pickle_file.pkl')
        file_name = os.path.normpath(target_path_2)

        with open(file_name, "wb") as f:
            pickle.dump(of, f, pickle.HIGHEST_PROTOCOL)

        with open(file_name, "rb") as f:
            of_loaded = pickle.load(f)

        self.assertEqual(of._mapping_dict, of_loaded._mapping_dict)

