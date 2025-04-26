#!/Users/taraqfarhan/Desktop/buildnlearn/Projects/giggity/venv/bin/python3  # source to your interpreter 

import data, arguments

def main():
    args = arguments.parse_arguments()
    
    # repository check: only allow `init` if there's no .giggity directory
    if args.func.__name__ != "init":
        if not data.os.path.isdir(data.os.path.join(data.os.getcwd(), ".giggity")):
            print("fatal: not a giggity repository\ninitialize the repo first using giggity init [dir]")
            exit(1)

    args.func(args)        

def init(args): data.init(args.directory)
def hash_object(args):
    if (args.write): data.hash_object(args.file, write=True)
    else: data.hash_object(args.file)
def cat_file(args): 
    if (args.print): print(data.cat_file(args.object, print=True))
    elif (args.size): print(data.cat_file(args.object, size=True))
    elif (args.type): print(data.cat_file(args.object, type=True))
def clone(args): data.clone(args.branch, args.link, args.directory)

if __name__ == "__main__": main()