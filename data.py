import os
import base64
import zlib
from hashlib import sha1
try: import requests 
except ModuleNotFoundError:
    print("You need to install `requests` module via pip (you may need virtual enviroment)\nRun the following commands")
    print("\npython3 -m venv venv && source venv/bin/activate")
    print("pip install requests")
    exit(1)


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


# giggity clone [--branch=<name>] <repo link> [directory]
def clone(branch, link, dir):
    # link format: https://github.com/tarqfarhan/ggl or https://github.com/taraqfarhan/ggl.git
    parts = link.split("/")
    OWNER = parts[3]
    REPO = parts[4].split('.')[0]
    # TOKEN = r'' # your ACCESS_TOKEN
    
    if dir is None: DIR = f"{os.path.join(os.getcwd(), REPO)}"
    else: DIR = f"{os.path.join(os.getcwd(), dir)}"

    # Step 1: Fetch the full tree
    tree_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{branch}?recursive=1"
    # response = requests.get(tree_url, headers={'Authorization': f'access_token {TOKEN}'})
    response = requests.get(tree_url)
    data = response.json()
    
    # Step 2: Process each item
    try:
        print(f"Cloning into '{DIR.split('/')[-1]}'...")
        flag = True 
        for item in data['tree']:
            # only make the directory if the remote branch exists
            if flag:  
                flag = False  # and run the next block only for the first loop
                if not os.path.exists(os.path.join(DIR)): os.mkdir(os.path.join(DIR))
                os.chdir(DIR)

            path = item['path']
            # folder = os.path.dirname(path)
            if item['type'] == 'tree':
                # if folder: os.makedirs(folder, exist_ok=True) # Only create folder if folder is not empty
                os.makedirs(path, exist_ok=True) 
            elif item['type'] == 'blob':
                blob_url = item['url']
                try: 
                    # blob_resp = requests.get(blob_url, headers={"Authorization": f"access_token {TOKEN}"})
                    blob_resp = requests.get(blob_url)
                    blob_data = blob_resp.json()
                    file_content = base64.b64decode(blob_data['content'])
                
                    # folder = os.path.dirname(path)
                    # if folder: os.makedirs(folder, exist_ok=True)

                    with open(path, 'wb') as f: f.write(file_content)
                except KeyError: 
                    print(f"Response to {blob_url} Key Error")
                    exit(1)
        print("Cloning completed")
    except KeyboardInterrupt: 
        print("Couldn't fetch data properly. Keyboard Interrupted")
        exit(1)
    except KeyError: 
        print(f"Response to {tree_url} Key Error")
        print(data['message'])
        exit(1)
        # if ("Not Found" in data['message']):
            # print(f"fatal: Remote branch {branch} not found in upstream origin")
            # exit(1)
        # else: print(data['message'])


# giggity hash-object [-w] <file>
def hash_object(file_path, obj_type=b'blob', write=False):
    if (not os.path.exists(os.path.join(os.getcwd(), file_path))):
        print(f"fatal: no such file {os.getcwd()}/{file_path}")
        exit(1)
        
    contents_of_file = read_file(file_path)
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
def cat_file(obj_id, print=False, size=False, type=False):
    file_path = os.path.join(os.getcwd(), ".giggity", "objects", f"{obj_id[:2]}", f"{obj_id[2:]}")

    if (not os.path.exists(os.path.join(os.getcwd(), file_path))):
        print(f"fatal: no such file {os.getcwd()}/{file_path}")
        exit(1)

    content = read_file(file_path, compressed=True)
    partitions = content.partition(b'\x00')

    if print: return partitions[2].decode("utf-8")
    elif type: return partitions[0].decode("utf-8").split()[0]
    elif size: return partitions[0].decode("utf-8").split()[1]