# This file contains all the implementation of the porcelain commands (high level commands) 

# local module misc.py
import misc
from misc import os

# python standard modules
from base64 import b64decode
from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads



# giggity init [directory]
def init(path=os.getcwd()):
    GIGGITY_DIR = os.path.join(path, ".giggity")
    if not os.path.exists(path): os.mkdir(path) 

    if not os.path.exists(GIGGITY_DIR):
        for name in ("", "objects", "refs", "refs/heads", "refs/tags"): os.mkdir(os.path.join(GIGGITY_DIR, name))
        with open(os.path.join(GIGGITY_DIR, "HEAD"), "w") as f:  f.write("ref: refs/heads/main\n") 
        with open(os.path.join(GIGGITY_DIR, "config"), "w") as f:  f.write("""[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true\n""")
        with open(os.path.join(GIGGITY_DIR, "description"), "w") as f:  f.write("Unnamed repository; edit this file 'description' to name the repository.\n") 
        print(f"Initializing empty Giggity repo in {os.path.abspath(GIGGITY_DIR)}")
    else:
        print("Giggity is already initialized in current directory")
        print(f"Reinitialized Giggity repo in {os.path.abspath(GIGGITY_DIR)}")


# giggity clone [--branch=<name>] <repo link> [directory]
def clone(branch, link, dir):
    # link format: https://github.com/tarqfarhan/ggl or https://github.com/taraqfarhan/ggl.git
    parts = link.split("/") # splitting the `link` string using '\' as divider
    OWNER = parts[-2] 
    REPO = parts[-1].split('.')[0] 
    
    if dir is None: DIR = f"{os.path.join(os.getcwd(), REPO)}"
    else: DIR = f"{os.path.join(os.getcwd(), dir)}"

    # Step 1: Fetch the full tree
    tree_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{branch}?recursive=1"
    try:
        response = urlopen(tree_url)
        data = loads(response.read().decode("utf-8"))
    except HTTPError as e: 
        print(f'HTTP {e.code} error: {e.reason}')
        exit(1)
    
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
            if item['type'] == 'tree': os.makedirs(path, exist_ok=True) 
            elif item['type'] == 'blob':
                blob_url = item['url']
                try: 
                    blob_resp = urlopen(blob_url)
                    blob_data = loads(blob_resp.read().decode("utf-8"))
                    file_content = b64decode(blob_data['content'])

                    with open(path, 'wb') as f: f.write(file_content)
                except KeyError: 
                    print(f"Response to {blob_url} Key Error")
                    exit(1)
                except HTTPError as e:
                    print(f'HTTP {e.code} error: {e.reason}')
                    exit(1)
        print("Cloning completed")
    except KeyboardInterrupt: 
        print("Couldn't fetch data properly. Keyboard Interrupted")
        exit(1)
    except KeyError: 
        print(f"Response to {tree_url} Key Error")
        print(data['message'])
        exit(1)
