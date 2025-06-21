#!/usr/bin/env python3  # path to python3 interpreter
# This is the main file (entry point of the program)

# local modules arguments.py, procelain.py, plumbing.py and misc.py
import arguments, porcelain, plumbing
from misc import os



def main():
    args = arguments.parse_arguments()
    
    # repository check: only allow `init` and `clone` if there's no .giggity directory
    if args.func.__name__ not in ("init", "clone"):
        if not os.path.isdir(os.path.join(os.getcwd(), ".giggity")):
            print("fatal: not a giggity repository\ninitialize the repo first using giggity init [dir]")
            exit(1)

    args.func(args)        



def init(args): porcelain.init(args.directory)
def clone(args): porcelain.clone(args.branch, args.link, args.directory)

def hash_object(args):
    if (args.write): plumbing.hash_object(args.file, write=True)
    else: plumbing.hash_object(args.file)
def cat_file(args): 
    if (args.printing): print(plumbing.cat_file(args.object, printing=True))
    elif (args.size): print(plumbing.cat_file(args.object, size=True))
    elif (args.type): print(plumbing.cat_file(args.object, type=True))

if __name__ == "__main__": main()