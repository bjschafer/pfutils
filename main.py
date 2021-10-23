# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import os


# def parse_single_monster(url: str):
#     print(parser.url_to_md(url))
import parser

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="PFRPG Utilities")
    subparsers = argparser.add_subparsers()
    monster_sub = subparsers.add_parser("monster", help="Monster utilities")
    monster_sub.add_argument("url", type=str, help="URL to get monster from")
    monster_sub.add_argument("-n", "--no-convert", action='store_true', help="Stop before converting to markdown")
    monster_sub.add_argument("-o", "--output", type=str, help="Path to output file or folder")

    args = vars(argparser.parse_args())

    if 'url' in args:
        for statblock, monster_name in parser.parse_monster(args['url'], args['no_convert']):
            out_path = args['output']
            if out_path:
                if os.path.isdir(out_path):
                    out_path = os.path.join(out_path, monster_name)
                if not out_path.endswith(".md"):
                    out_path += ".md"
                with open(out_path, 'w') as f:
                    f.write(statblock)
#        [print(m) for m in parser.parse_monster(args['url'], args['no_convert'])]
