import ast
import argparse

from transformers.curry import CurryTransformer
from transformers.bind import BindTransformer
from transformers.normalize import NormalizeTransformer
from transformers.namescrabler import NameScramblerTransformer
from transformers.unbind import UnbindTransformer

def obfuscate(node, level=3):
    if level >= 0:
        node = CurryTransformer().visit(node)
    if level >= 1:
        node = NormalizeTransformer().visit(node)
    if level >= 2:
        node = BindTransformer().visit(node)
    if level >= 3:
        node = NameScramblerTransformer().visit(node)
    
    node = ast.fix_missing_locations(node)
    return node


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input_file", help="input file to obfuscate")
    description_text_level = """obfuscation level:
    - 0: curry transform
    - 1: normalize
    - 2: bind functions
    - 3: obfuscate names
    """
    parser.add_argument("-l", "--level", help=description_text_level, type=int, default=3, choices=[0, 1, 2, 3])
    parser.add_argument("-d", "--deobfuscate", help="deobfuscate instead of obfuscate", action="store_true")
    args = parser.parse_args()


    # read sample file
    with open(args.input_file, "r") as f:
        sample = f.read()

    if args.deobfuscate:
        # assume that the lambda terms are on the last line
        preamble, sample = sample.strip().rsplit("\n", 1)
    else:
        preamble, sample = sample.split("# obfuscate", 1)


    parsed = ast.parse(sample)


    if args.deobfuscate:
        # deobfuscate
        parsed = UnbindTransformer().visit(parsed)
        parsed = ast.fix_missing_locations(parsed)
    else:
        # obfuscate
        parsed = obfuscate(parsed, level=args.level)

    script = f"{preamble.strip()}\n\n{ast.unparse(parsed)}"

    print(script)

if __name__ == "__main__":
    main()