import os
import sys
import time

import regex as re
import requests
from googletrans import Translator
from xpinyin import Pinyin

PINYIN_CHARS = "a-zA-ZĀāÁáǍǎÀàĒēÉéĚěÈèĪīÍíǏǐÌìŌōÓóǑǒÒòŪūÚúǓǔÙùÜüǗǘǙǚǛǜ"


def int_input(prompt: str, lower_bound: int, upper_bound: int) -> int:
    while True:
        try:
            user_input = int(input(prompt))
            if not lower_bound <= user_input <= upper_bound:
                raise ValueError
            return user_input
        except ValueError:
            print("\nError: Invalid input, try again.")


def format_cloze_braces(string: str) -> str:
    return re.sub("({)", r"{{c1::", re.sub("(})", r"}}", string))


def get_possible_pinyins(hz_string: str) -> list:
    return Pinyin().get_pinyins(hz_string, tone_marks="marks", splitter="-")


def get_pinyin(hz_string: str) -> str:
    pinyin_string = ""
    char_pinyin_map = {}

    for i, char in enumerate(hz_string):
        if not re.match("\p{Han}", char):
            pinyin_string += char
            continue

        if char not in char_pinyin_map:
            pinyins = get_possible_pinyins(char)

            if len(pinyins) == 1:
                pinyin = pinyins[0]
            else:
                print(f"\n[!] Multiple pinyins for {char}:\n")

                max_pinyin = max(map(len, map(str, range(1, len(pinyins) + 1))))
                for n, p in enumerate(pinyins, 1):
                    print(f"\t{n:>{max_pinyin}}. {p}")

                choice = int_input(f"\n[?] Choose a pinyin for {char}: ", 1, len(pinyins))
                pinyin = pinyins[choice - 1]
                char_pinyin_map[char] = pinyin
        else:
            pinyin = char_pinyin_map[char]

        if i < len(hz_string) - 1 and re.match("\p{Han}", hz_string[i + 1]):
            pinyin += "-"

        pinyin_string += pinyin

    return pinyin_string


def process_read_cards(rows: list) -> list:
    processed_cards = []

    for hz_string in rows:
        processed_cards.append(
            "\t".join(
                [
                    hz_string,
                    get_pinyin(hz_string),
                    Translator().translate(hz_string).text,
                ]
            )
            + "\n"
        )

    return processed_cards


def process_write_cards(rows: list) -> list:
    processed_cards = []

    for hz_char in rows:
        if len(hz_char) != 1:
            continue
        resp = requests.get(f"http://www.strokeorder.info/mandarin.php?q={hz_char}")
        gif_id = re.search("http:\/\/bishun\.strokeorder\.info\/characters\/.(\d+).gif", resp.text).group(1)
        processed_cards.append("\t".join([get_pinyin(hz_char), hz_char, gif_id]) + "\n")

    return processed_cards


def process_cloze_cards(rows: list) -> list:
    processed_cards = []

    for hz_string in rows:
        cloze_str = format_cloze_braces(hz_string)

        pinyin = format(
            format_cloze_braces(
                re.sub(
                    f"\{'{'}(?=[{PINYIN_CHARS}{'}'}])",
                    "}-",
                    re.sub(f"(?<=[{PINYIN_CHARS}{'}'}])\{'{'}", "-{", get_pinyin(hz_string)),
                )
            )
        )

        plain_str = hz_string.replace("{", "").replace("}", "")
        processed_cards.append(
            "\t".join([cloze_str, plain_str, pinyin, Translator().translate(plain_str).text]) + "\n"
        )

    return processed_cards


def main(in_filepath: str, format: str) -> None:
    with open(in_filepath, "r", encoding="utf-8") as in_file:
        in_rows = set(in_file.read().splitlines())

    match format:
        case "read":
            cards = process_read_cards(in_rows)
        case "write":
            cards = process_write_cards(in_rows)
        case "cloze":
            cards = process_cloze_cards(in_rows)
        case _:
            print("Error: Invalid format type.")
            return

    out_name = f"{format}_{int(time.time())}.out"
    with open(out_name, "w+", encoding="utf-8") as out_file:
        out_file.writelines(cards)

    print(f'\n[+] Done! {len(cards)} cards written to "{out_name}"')


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print(f"Usage: python {sys.argv[0]} <in_file> <out_format>")
    elif not os.path.isfile(sys.argv[1]):
        print(f"Error: {sys.argv[1]} is not a file.")
    else:
        main(sys.argv[1], sys.argv[2])
