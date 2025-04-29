# giggity: learn git internals with python
Git has tons of features, but most of the times we will use only the common commands. This project is dedicated to learn about the Git internals by implementing Git's most common commands (and the common options) in Python.

## Start Here
```sh
#1 clone the repo first
git clone https://github.com/taraqfarhan/giggity

#2 go to that directory and delete .git/ and .giggity/ directory
cd giggity && rm -rf .git/ .giggity/

#3 make an alias and make it global so that you can use `giggity` anywhere from the terminal
echo "alias giggity='python3 path/to/giggity.py'" >> ~/.zshrc
source ~/.zshrc 
# .zshrc for zsh, .bashrc for bash ...

#4 get additional help
giggity -h  # help about all the commands and options
giggity clone -h  # help about a specific command 
```

## Files
1. giggity.py (the main file, entry point of the program)
2. arguments.py (handles command line arguments and options)
3. data.py (actual implementation of the commands)
 
 > Read the comments (docstrings) from each file to understand the program easily. I will encourage you to follow the order i've mentioned, but you can choose not to follow the order.

## Commands implemented
##### Porcelain Commands (Higher level: User Friendly)
```
clone
init
```
##### Plumbing Commnads (Lower Level: For Nerds)
```
hash-object
cat-file
```