import os
import zlib
from hashlib import sha1

def read_file(path, compressed=False):
    if (os.path.exists(path) and os.path.isfile(path)):
        if not compressed: 
            with open(path, "rb") as file: return file.read()
        else:
            with open(path, "rb") as file: return zlib.decompress(file.read()) # returns utf-8 encoded data
    else: print(f"fatal: could not open '{path}' for reading: No such file")
 
 
# giggity init [directory]
def init(path=os.getcwd()):
    GIGGITY_DIR = os.path.join(path, ".giggity")
    if not os.path.exists(path): os.mkdir(path) 

    if not os.path.exists(GIGGITY_DIR):
        for name in ("", "objects", "refs", "refs/heads"): os.mkdir(os.path.join(GIGGITY_DIR, name))
        with open(os.path.join(GIGGITY_DIR, "HEAD"), "w") as f: 
            f.write("ref: refs/heads/main") 
        print(f"Initializing empty Giggity repo in {os.path.abspath(GIGGITY_DIR)}")
    else:
        print("Giggity is already initialized in current directory")
        print(f"Reinitialized Giggity repo in {os.path.abspath(GIGGITY_DIR)}")


# giggity hash-object [-w] <file>
def hash_object(file_path, obj_type=b'blob', write=False):
    # Object Hash = sha1(<object_type> + " " + <size_of_file> + "\0" + <contents_of_file>)  
    if (not os.path.exists(os.path.join(os.getcwd(), file_path))):
        print(f"fatal: no such file {os.getcwd()}/{file_path}")
        exit(1)
        
    contents_of_file = read_file(file_path)
    size_of_file = str(len(contents_of_file)).encode("utf-8") # os,path.getsize('file_path')

    if isinstance(contents_of_file, str): contents_of_file = contents_of_file.encode("utf-8")
    
    header = obj_type + b' ' + size_of_file + b'\x00'
    # header = b'blob ' + size_of_file + b'\x00' # \0 can be replaced with \x00 (we are working with files only for now)
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
def cat_file(obj_id, print=False, size=False, type=False):
    file_path = os.path.join(os.getcwd(), ".giggity", "objects", f"{obj_id[:2]}", f"{obj_id[2:]}")
    content = read_file(file_path, compressed=True)
    partitions = content.partition(b'\x00')

    if print: return partitions[2].decode("utf-8")
    elif type: return partitions[0].decode("utf-8").split()[0]
    elif size: return partitions[0].decode("utf-8").split()[1]