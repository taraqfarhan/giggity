# This file contains all the implementation of the plubming commands (lower level commands)

# local module misc.py
import misc
from misc import os
from misc import zlib

# python standard modules
from hashlib import sha1



# giggity hash-object [-w] <file>
def hash_object(file_path, obj_type=b'blob', write=False):
    if (not os.path.exists(os.path.join(os.getcwd(), file_path))):
        print(f"fatal: no such file {os.getcwd()}/{file_path}")
        exit(1)
    elif (os.path.isdir(os.path.join(os.getcwd(), file_path))):
        print(f"fatal: unable to hash {file_path}, because it's a directory")
        exit(1)
        
    contents_of_file = misc.read_file(file_path)
    size_of_file = str(len(contents_of_file)).encode("utf-8") # os.path.getsize('path/to/file')

    if isinstance(contents_of_file, str): contents_of_file = contents_of_file.encode("utf-8")
    
    # Object Hash = sha1(<object_type> + " " + <size_of_file> + "\0" + <contents_of_file>)  
    header = obj_type + b' ' + size_of_file + b'\x00' # \0 can be replaced with \x00 (we are working with files only for now)
    obj_hash = sha1((header + contents_of_file)).hexdigest()
    print(obj_hash)

    if write: 
        data = header + contents_of_file
        compressed_data = zlib.compress(data)

        dir_path = os.path.join(os.getcwd(), ".giggity", "objects", f"{obj_hash[:2]}")
        try: os.mkdir(dir_path)
        except FileExistsError: pass

        file_path = os.path.join(os.getcwd(), ".giggity", "objects", f"{obj_hash[:2]}", f"{obj_hash[2:]}")
        with open(file_path, "wb") as f: f.write(compressed_data)
    else: return obj_hash


# giggity <-p | -s | -t> <object hash>
def cat_file(obj_id, printing=False, size=False, type=False):
    file_path = os.path.join(os.getcwd(), ".giggity", "objects", f"{obj_id[:2]}", f"{obj_id[2:]}")
    
    if (not os.path.exists(file_path)):
        print(f"fatal: no such file {file_path}")
        exit(1)
        
    content = misc.read_file(file_path, compressed=True)
    partitions = content.partition(b'\x00')

    if printing: return partitions[2].decode("utf-8")
    elif type: return partitions[0].decode("utf-8").split()[0]
    elif size: return partitions[0].decode("utf-8").split()[1]