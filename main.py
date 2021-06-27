# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse


# def parse_single_monster(url: str):
#     print(parser.url_to_md(url))
import parser

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="PFRPG Utilities")
    subparsers = argparser.add_subparsers()
    monster_sub = subparsers.add_parser("monster", help="Monster utilities")
    monster_sub.add_argument("url", type=str, help="URL to get monster from")

    args = vars(argparser.parse_args())

    if 'url' in args:
        [print(m) for m in parser.parse_monster(args['url'])]
