# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "distlib==0.3.8",
# ]
# ///

import sys

from distlib.scripts import ScriptMaker


def main():
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    executable = sys.argv[3]
    script_maker = ScriptMaker(source_dir, dest_dir)
    script_maker.executable = executable
    script_maker.make("pipx")


if __name__ == "__main__":
    main()
