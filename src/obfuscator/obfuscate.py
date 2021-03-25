# -*- coding:utf-8 -*-
import random
import re
import string
import jieba

URL_REGEX = (
    r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.]("
    r"?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx"
    r"|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv"
    r"|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er"
    r"|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu"
    r"|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu"
    r"|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr"
    r"|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk"
    r"|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy"
    r"|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s("
    r")]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'"
    r'".,'
    r"<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.]("
    r"?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx"
    r"|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv"
    r"|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er"
    r"|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu"
    r"|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu"
    r"|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr"
    r"|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk"
    r"|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy"
    r"|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"
)


class Obfuscator:
    def __init__(self, N=12, mapping_dict=None):

        self._N = N
        if mapping_dict is not None:
            self._mapping_dict = mapping_dict
        else:
            self._mapping_dict = {}
        self._reverse_mapping_dict = {}

    def _generate_random_chinese_character(self) -> str:

        val = random.randint(0x4E00, 0x9FFF)
        return chr(val)

    def _strip_url(self, string) -> str:

        return re.sub(URL_REGEX, "", string)

    def _bNN(self, n, N, NN, chars=string.ascii_lowercase) -> str:

        s = ""
        for _ in range(N):
            s += chars[n % NN]
            n //= NN
        return s

    def _generate_alpha_numeric_substring_mapping(self, sub_string) -> str:
        needs_new_key = True

        n_chars = sum(c.isalpha() for c in sub_string)
        n_numbers = sum(c.isdigit() for c in sub_string)

        while needs_new_key:
            key_sorted = self._bNN(
                random.randint(0, 26 ** self._N), n_chars, 26, chars=string.ascii_lowercase
            ) + self._bNN(random.randint(0, 10 ** self._N), n_numbers, 10, chars=string.digits)
            key = "".join(random.sample(key_sorted, len(key_sorted)))
            if key not in self._mapping_dict.values():
                self._mapping_dict[sub_string] = key
                needs_new_key = False

        return key

    def _generate_hash(self, sub_string) -> str:

        needs_new_key = True
        while needs_new_key:
            key = self._bNN(
                random.randint(0, 36 ** self._N),
                self._N,
                36,
                string.ascii_uppercase + string.digits,
            ).lower()
            if key not in self._mapping_dict.values():
                self._mapping_dict[sub_string] = key
                needs_new_key = False

        return key

    def _generate_chinese_token_mapping(self, chinese_token) -> str:
        needs_new_key = True

        while needs_new_key:
            key = "".join(
                [self._generate_random_chinese_character() for i in range(len(chinese_token))]
            )

            if key not in self._mapping_dict.values():
                self._mapping_dict[chinese_token] = key
                needs_new_key = False

        return key

    def _generate_chinese_substring_mapping(self, chinese_substring) -> str:
        token_list = jieba.lcut(chinese_substring)

        # check if only ascii or chinese characters are in the string, generate hash if not
        if not all(
            [
                re.search(u"[\u4e00-\u9fff]", token) is not None
                for token in token_list
                if not token.isascii()
            ]
        ):
            key = self._generate_hash(chinese_substring)
            return key

        # generate keys for all unknown parts of the tokenized string (if non-empty)
        for token in token_list:
            if token not in self._mapping_dict.keys():
                if token == "":
                    continue
                if re.search(u"[\u4e00-\u9fff]", token):
                    _ = self._generate_chinese_token_mapping(token)
                else:
                    _ = self._generate_alpha_numeric_substring_mapping(token)

        # use the generated keys to obfuscate the chinese_substring
        concatenated_key = " ".join(
            [self._mapping_dict[token] for token in token_list if token != ""]
        )

        self._mapping_dict[chinese_substring] = concatenated_key

        return concatenated_key

    def _generate_equivalent_new_key(self, sub_string) -> str:

        if re.search(u"[\u4e00-\u9fff]", sub_string):
            key = self._generate_chinese_substring_mapping(sub_string)

        elif not sub_string.isascii():
            key = self._generate_hash(sub_string)

        else:
            key = self._generate_alpha_numeric_substring_mapping(sub_string)

        return key

    def _split_by_punctuation_empty_space(self, no_url_string) -> list:
        return [
            (item, any(c in string.punctuation for c in item))
            for item in map(str.strip, re.split(r"(\W+|_)", no_url_string))
        ]

    def obfuscate(self, raw_string) -> str:
        lower_str = raw_string.lower()
        no_url_string = self._strip_url(lower_str)
        obfuscated_string = ""

        if len(no_url_string) > 0:
            string_is_sign_list = self._split_by_punctuation_empty_space(no_url_string)

            for sub_string, is_sign in string_is_sign_list:

                if sub_string == "":
                    obfuscated_string += " "
                    continue
                if is_sign:
                    obfuscated_string += sub_string
                    continue
                if sub_string not in self._mapping_dict.keys():
                    _ = self._generate_equivalent_new_key(sub_string)
                suffix = ""
                if len(obfuscated_string) > 0:
                    most_recent_character = obfuscated_string[-1]
                    if not (
                        (most_recent_character in string.punctuation)
                        or (most_recent_character == " ")
                    ):
                        suffix = " "

                obfuscated_string += suffix + self._mapping_dict[sub_string]

            # remove most recent added suffix
            obfuscated_string = obfuscated_string.rstrip()

        return obfuscated_string

    def reverse_obfuscation(self, obfuscated_string) -> str:
        if self._mapping_dict == {}:
            raise ValueError("No mapping available")
        # updating reverse dict
        unknown_strings = set(self._mapping_dict.keys()) - set(self._reverse_mapping_dict.values())
        new_mappings = {self._mapping_dict[new_string]: new_string for new_string in unknown_strings}
        self._reverse_mapping_dict.update(new_mappings)
        restored_string = ""

        string_is_sign_list = self._split_by_punctuation_empty_space(obfuscated_string)

        for sub_string, is_sign in string_is_sign_list:

            if sub_string == "":
                restored_string += " "
                continue
            if is_sign:
                restored_string += sub_string
                continue
            if sub_string not in self._reverse_mapping_dict.keys():
                raise ValueError(f"token {sub_string} has not been generated by this obfuscator")

            suffix = ""
            if len(restored_string) > 0:
                most_recent_character = restored_string[-1]
                if not (
                    (most_recent_character in string.punctuation)
                    or (most_recent_character == " ")
                ):
                    suffix = " "

            restored_string += suffix + self._reverse_mapping_dict[sub_string]

        # remove most recent added suffix
        restored_string = restored_string.rstrip()

        return restored_string
