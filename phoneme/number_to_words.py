# -*- coding: UTF-8 -*-

import codecs
import re
import sys

# 0-19 feminine
ones_tens_feme = u"صِفْر,واحِدَة,إِثْنَتانِ,ثَلاث,أَرْبَع,خَمْس,سِت,سَبْع,ثَماني,تِسْع,عَشْر,إِحْدى عَشْرَةَ,إِثْنَتا عَشْرَةَ,ثَلاث عَشْرَةَ,أَرْبَع عَشْرَةَ,خَمْسَ عَشْرَةَ,سِتَ عَشْرَةَ,سَبْعَ عَشْرَةَ,ثَماني عَشْرَةَ,تِسْعَ عَشْرَةَ".split(
    u",")

# 0-19 masculine
ones_tens_masc = u"صِفْر,واحِد,إِثْنانِ,ثَلاثَة,أَرْبَعَة,خَمْسَة,سِتَة,سَبْعَة,ثَمانِيَة,تِسْعَة,عَشَرَة,أَحَدَ عَشْرَةَ,إِثْنا عَشَرَ,ثَلاثَةَ عَشَرَ,أَرْبَعَةَ عَشَرَ,خَمْسَةَ عَشَرَ,سِتَةَ عَشَرَ,سَبْعَةَ عَشَرَ,ثَمانِيَةَ عَشَرَ,تِسْعَةَ عَشَرَ".split(
    u",")

# 0,10,20,30 ... No gender needed (plural)
mul_tens = u"صِفْر,عَشَرَة,عِشْرونَ,ثَلاثونَ,أَرْبَعونَ,خَمْسونَ,سِتونَ,سَبْعونَ,ثَمانونَ,تِسْعونَ".split(u",")

# Hundred,hundreds,hundreds
mul_hund = u"مِئَة,مِئَتانِ,مِئَة".split(u",")

# Thousand,thousands,thousands(for more than 10 thousand)
mul_thou = u"أَلْف,أَلْفانِ,آلاف".split(u",")

# Million,millions,millions(for more than 10 million)
mul_mill = u"مِلْيون,مِلْيونانِ,مَلايِين".split(u",")

# Billion,billions,billions(for more than 10 billion)
mul_bill = u"مِلْيار,مِلْيارانِ,مِلْيارات".split(u",")

# Trillion,quadrillion ... No plural needed here
mul_rest = u"تْرِلْيُون,كْوادْرِلْيُون,كْوِينْتِلْيُون,سِكْسْتِلْيُون,سِبْتِلْيُون".split(u",")

# Symbol map
symbols = {
    u"£": u"باونْدْ",
    u"$": u"دولارْ",
    u"€": u"يُورُو",
    u"×": u"ضَرْبْ",
    u"%": u"بِالمِئَةْ",
    u".": u"فاصِلَةْ",
    u",": u"فاصِلَةْ",
    u"@": u"آتْ",
    u"=": u"يُساوِي",
    u"+": u"زائِدْ",
    u"سم": u"سَنْتِمِتْراً",
    u"م": u"مِتْراً",
    u"ملم": u"مِلِّمِتْراً",
    u"مل": u"مِلِّلِتْراً",
    u"ل": u"لِتْراً",
    u"كغ": u"كيلوغْراماً",
    u"غ": u"غْراماً",
    u"-": u" - ",
    u"\/": u" - ",
    u"\\": u" - "
}

# To convert Indian to Arabic numerals
indian_to_arabic = {
    u"٠": u"0",
    u"١": u"1",
    u"٢": u"2",
    u"٣": u"3",
    u"٤": u"4",
    u"٥": u"5",
    u"٦": u"6",
    u"٧": u"7",
    u"٨": u"8",
    u"٩": u"9"
}

MAXINT = 999999999999999999999999999


def number_phrase_to_word(number_in, inflection, gender, nunation, genitive_follows):
    """
    Preprocessor function of number_to_word. Removes unnecessary characters and splits
    the input in to separate digit sequences and also decodes symbols ($ = dollar).
    It is also a post-processor as it deals with nunation and genitive_follows.
    For info about the params, see the info about the args bellow.
    """
    res = u""
    """
    Preprocessing.
    """
    if (type(number_in).__name__ == u"int" or type(number_in).__name__ == u"long"):
        number_in = str(number_in)
    number_in = re.sub(u"[^0-9٠-٩سملكغ\W+]", u"", number_in)
    for key in indian_to_arabic:
        number_in = re.sub(key, indian_to_arabic[key], number_in)
    number_in = re.split(u"(\W)", number_in)
    """
    Main loop.
    """
    for i in range(len(number_in)):
        token = number_in[i].strip()

        if (token != ""):
            if (token in symbols):  # Deal with symbols.
                res += u" " + symbols[token]
            else:  # Deal with numbers.
                number_sections = re.split(u"\s", token)
                for number in number_sections:
                    number_word = number_to_word(number, inflection, gender)

                    """
                    Post-process each individual number sequence.
                    """
                    if (not nunation):
                        if (number_word[-1] == u"ً"):
                            number_word = number_word[0:-1] + u"َ"
                        if (number_word[-1] == u"ٌ"):
                            number_word = number_word[0:-1] + u"ُ"
                        if (number_word[-1] == u"ٍ"):
                            number_word = number_word[0:-1] + u"ِ"
                    if (genitive_follows):
                        if (number_word.endswith(u"َينِ")):
                            number_word = number_word[0:-2]
                    else:
                        if (number_word[-1] in [u"َ", u"ُ", u"ِ", u"ً", u"ٌ", u"ٍ"]):
                            number_word = number_word[0:-1]

                    """
                    The following four lines deal with مئة. Because it should be connected
                    with the ones word before it. example: سبع مئة should be سبعمئة.
                    """
                    number_word = re.sub(u"([َُِ])ي([َُِ])ة([َُِ]) مِئَة", u"\\3مِئَة", number_word)

                    number_word = re.sub(u"([َُِ])ة([َُِ]) مِئَة", u"\\2مِئَة", number_word)

                    number_word = re.sub(u"([َُِ])ي([َُِ])ة مِئَة", u"ُمِئَة", number_word)

                    number_word = re.sub(u"([َُِ])ة مِئَة", u"ُمِئَة", number_word)

                    number_word = re.sub(u"ن([َُِ])ي([َُِ]) مِئَة", u"ن\\2مِئَة", number_word)

                    number_word = re.sub(u" مِئَة", u"مِئَة", number_word)

                    if (number_word != u""):
                        res += u" - " + number_word

    return res.strip()  # Strip spaces and return


def add_inflection_ones(integer, res, inflection, nunation):
    """
    Inflect the number phrase in res, which is the number phrase of integer,
    according to the input inflection. This function is for ones and duals in Arabic.
    """
    temp_res = res
    if (integer <= 10):
        if (integer == 2):
            if (inflection in [u"accusative", u"genitive"]):
                if (temp_res[-3] == u"ا"):
                    temp_res = temp_res[0:-3] + u"َي" + temp_res[-2:]
                else:
                    temp_res = temp_res[0:-3] + u"ي" + temp_res[-2:]
        else:
            if (temp_res.endswith(u"ماني")):
                temp_res = temp_res[0:-1]
            if (inflection == u"accusative"):
                if (nunation):
                    temp_res += u"ً"
                else:
                    temp_res += u"َ"
            if (inflection == u"genitive"):
                if (nunation):
                    temp_res += u"ٍ"
                else:
                    temp_res += u"ِ"
            if (inflection == u"subjective"):
                if (nunation):
                    temp_res += u"ٌ"
                else:
                    temp_res += u"ُ"

    return temp_res


def add_inflection_whole(integer, res, inflection):
    """
    Inflect the number phrase in res, which is the number phrase of integer,
    according to the input inflection. This function is only for duals in Arabic.
    """
    temp_res = res
    if (integer == 2):
        if (inflection in [u"accusative", u"genitive"]):
            if (temp_res[-3] == u"ا"):
                temp_res = temp_res[0:-3] + u"َي" + temp_res[-2:]
            else:
                temp_res = temp_res[0:-3] + u"ي" + temp_res[-2:]

    return temp_res


def number_to_word(number, inflection, gender, composite=False):
    """
    Convert a single sequence of digits to a number phrase
    :param number: str, long or int of number (str should contain only 0-9 characters).
    :param inflection: str containing the required inflection of the output phrase.
    Input empty string for no or minimal inflection. Options are subjective, accusative
    and genitive.
    :param gender: str containing the required gender of the output phrase. Should be
    either masculine or feminine.
    """
    res = u""  # Initialise result container
    """
    Now use the apporpriate list from 0-19 based on the input gender.
    """
    ones_tens_def = ones_tens_masc
    if (gender == u"feminine"):
        ones_tens_def = ones_tens_feme
    """
    Convert the input number to int regardless of its original type.
    """
    integer_string = number
    integer = number
    if (type(integer).__name__ == u"str" or type(integer).__name__ == u"unicode"):
        integer = int(number)
    if (type(integer_string).__name__ == u"int" or type(integer_string).__name__ == u"long"):
        integer_string = str(number)
    """
    Main process.
    """
    if (type(integer).__name__ == u"int" or type(integer).__name__ == u"long"):
        if integer > MAXINT:  # Don't process numbers larger than a certain limit
            return u""
        elif (integer < 20):  # If less than 20, simply output and inflect
            res += u" " + ones_tens_def[integer]
            if (composite):
                res = add_inflection_ones(integer, res, inflection, False)
            else:
                res = add_inflection_ones(integer, res, inflection, True)
        elif (integer < 100):  # If less than 100
            if (integer % 10 != 0):  # If not a multiple of 10
                res += u" " + ones_tens_def[integer % 10]
                res = add_inflection_ones(integer % 10, res, inflection, True)

                res += u" وَ" + mul_tens[integer / 10]  # Process the tens
                res = add_inflection_whole(2, res, inflection)  # Inflect the tens.
            # Important: the 2 passed here is to fool the function as the input is actually plural.
            else:
                res += u" " + mul_tens[integer / 10]  # If a multiple of 10, simply
                res = add_inflection_whole(2, res, inflection)  # Inflect the tens
                # Important: the 2 passed here is to fool the function as the input is actually plural.
        elif (integer <= 999):
            if (integer / 100 <= 2):
                """
                If less than 300 (In Arabic, there is no one hundred or two hundred.
                They are individual words). Now process and inflect.
                This comment applies to all the following elif blocks (except last)
                """
                res += u" " + mul_hund[(integer / 100) - 1]
                res = add_inflection_ones(integer / 100, res, inflection, True)
            else:
                """
                Else, process the ones of hundreds.
                This comment applies to all the following elif blocks (except last).
                """
                res += u" " + ones_tens_def[integer / 100]
                res = add_inflection_ones(integer / 100, res, inflection, False)
                res += u" " + mul_hund[2]  # Now output the hundreds
                if (inflection != "MSA"):
                    res += u"ٍ"
            if (integer % 100 != 0):
                res += u" وَ" + number_to_word(integer % 100, inflection, gender,
                                               composite)  # Finally, process the ones
        elif (integer <= 999999):
            if (integer / 1000 <= 2):
                res += u" " + mul_thou[(integer / 1000) - 1]
                res = add_inflection_ones(integer / 1000, res, inflection, True)
            else:
                if ((integer / 1000) % 100 > 10):
                    """
                    Check if there are more than 10 thousands because in Arabic, the plural for thousand
                    changes when it is more than 10 thousands (goes back to the singular word).
                    This comment applies to all the following elif blocks (except last).
                    """
                    res += u" " + number_to_word(integer / 1000, inflection, "masculine") + u" " + mul_thou[0]
                    if (inflection != "MSA"):
                        res += u"ٍ"
                else:
                    if ((integer / 1000) % 100 > 2):
                        res += u" " + number_to_word(integer / 1000, inflection, "masculine", True) + u" " + mul_thou[2]
                        if (inflection != "MSA"):
                            res += u"ٍ"
                    else:
                        res += u" " + number_to_word(((integer / 1000) / 100) * 100, inflection, "masculine", True)
                        res += u" وَ" + number_to_word(((integer / 1000) % 100) * 1000, inflection, "masculine", True)
            if (integer % 1000 != 0):
                res += u" وَ" + number_to_word(integer % 1000, inflection, gender)
        elif (integer <= 999999999):
            if (integer / 1000000 <= 2):
                res += u" " + mul_mill[(integer / 1000000) - 1]
                res = add_inflection_ones(integer / 1000000, res, inflection, True)
            else:
                if (((integer / 1000000) % 100) > 10):
                    res += u" " + number_to_word(integer / 1000000, inflection, "masculine") + u" " + mul_mill[0]
                    if (inflection != "MSA"):
                        res += u"ٍ"
                        # res = add_inflection_ones(integer / 1000000, res, inflection, True)
                else:
                    res += u" " + number_to_word(integer / 1000000, inflection, "masculine", True) + u" " + mul_mill[2]
                    if (inflection != "MSA"):
                        res += u"ٍ"
            if (integer % 1000000 != 0):
                res += u" وَ" + number_to_word(integer % 1000000, inflection, gender)
        elif (integer <= 999999999999):
            if (integer / 1000000000 <= 2):
                res += u" " + mul_bill[(integer / 1000000000) - 1]
                res = add_inflection_ones(integer / 1000000000, res, inflection, True)
            else:
                if ((integer / 1000000000) % 100 > 10):
                    res += u" " + number_to_word(integer / 1000000000, inflection, "masculine") + u" " + mul_bill[0]
                    if (inflection != "MSA"):
                        res += u"ٍ"
                    res = add_inflection_ones(integer / 1000000000, res, inflection, True)
                else:
                    res += u" " + number_to_word(integer / 1000000000, inflection, "masculine", True) + u" " + mul_bill[
                        2]
                    if (inflection != "MSA"):
                        res += u"ٍ"
            if (integer % 1000000000 != 0):
                res += u" وَ" + number_to_word(integer % 1000000000, inflection, gender)
        else:
            """
            In this section, we deal with all the numbers higher than 999999999999.
            They are simpler as they are simply divided to two sections, the first 3
            digits from the left (section 1) and the rest of the digits (section 2).
            Then each section is dealt with recursively by calling this function again
            while adding the appropriate word between the sections. For example,
            (00)1123123123123 = number_to_word(001) + trillion and + number_to_word(123123123123)
            """
            string_length = len(integer_string)
            number_category = (string_length - 13) / 3
            number_zeros = 12 + 3 * number_category
            number_to_divide = int(u"1" + number_zeros * u"0")

            if (integer / number_to_divide <= 10 or (integer / number_to_divide) % 100 <= 10):
                res += u" " + number_to_word(integer / number_to_divide, inflection, "masculine", True)
                if (res[-1] in [u"َ", u"ً", u"ُ", u"ٌ", u"ِ", u"ٍ"]):
                    res = res[0:-1]
                res += u" " + mul_rest[number_category]
            else:
                res += u" " + number_to_word(integer / number_to_divide, inflection, "masculine", True) + u" " + \
                       mul_rest[number_category]
            if (integer % number_to_divide != 0):
                res += u" وَ" + number_to_word(integer % number_to_divide, inflection, gender)

    res = res.strip()  # Strip number of trailing and preceding spaces
    return re.sub(u"  ", u" ", res)  # Remove duplicate spaces and return result


"""
Main section in case this was run from command line.
This program takes seven command line arguments:
:arg input_file:
:arg out_file:
:arg inflection:
:arg gender:
:arg nunation:
:arg genitive_following:
"""
if __name__ == "__main__":
    res = []
    file_in = codecs.open(sys.argv[1], u"r", encoding=u"utf8")
    number_in = file_in.read()
    file_in.close()

    res.append(
        number_phrase_to_word(number_in, sys.argv[3], sys.argv[4], bool(int(sys.argv[5])), bool(int(sys.argv[6]))))

    file_out = codecs.open(sys.argv[2], u"w", encoding=u"utf8")
    file_out.write("\n".join(res))
    file_out.close()
