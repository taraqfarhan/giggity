import argparse
import giggity

def parse_arguments():
    parser = argparse.ArgumentParser(description="Git implementation in Python to learn Git in depth", prog='giggity', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True, metavar="commands")
    
    # init
    init_parser = commands.add_parser("init", help="initialize a giggity repo")
    init_parser.add_argument("directory", nargs='?', default=".", help="name of the directory to initialize Giggity")
    init_parser.set_defaults(func=giggity.init)
    
    # hash-object
    hashobject_parser = commands.add_parser("hash-object", help="computes the unique hash key of the content")
    hashobject_parser.add_argument('-w', '--write', action="store_true", help="compute the object hash and store it in the Giggity database")
    hashobject_parser.add_argument("file", help="name of the file")
    hashobject_parser.set_defaults(func=giggity.hash_object)

    # cat-file
    catfile_parser = commands.add_parser("cat-file", help="show the contents of a file")
    catfile_parser.add_argument('-p', '--print', action="store_true", help="pretty-print the contents of <object> based on its type")
    catfile_parser.add_argument('-t', '--type', action="store_true", help="show the object type identified by <object>")
    catfile_parser.add_argument('-s', '--size', action="store_true", help="show the object size identified by <object>")
    catfile_parser.add_argument('object', help="object hash of the file")
    catfile_parser.set_defaults(func=giggity.cat_file)
    
    return parser.parse_args()