# giggity: learn git internals with python

### Start
```sh
#1 clone the repo first
git clone https://github.com/taraqfarhan/giggity

#2 go to that directory
cd giggity

#3 make sure you have python3 installed

#4 install requests module (you may use virtual environment)
python3 -m venv venv && source venv/bin/activate
pip install requests

#5 make an alias and make it global so that you can use anywhere from the terminal
echo "alias giggity='python3 path/to/giggity.py'" >> ~/.zshrc
source ~/.zshrc 
# .zshrc for zsh, .bashrc for bash ...

#6 get additional help
giggity -h  # help about all the commands and options
giggity clone -h  # help about a specific command 
```

Git has tons of features, but most of the times we will use only the common commands. This project is dedicated to learn about the Git internals by implementing Git's most common commands (and the common options) in Python.

```
Porcelain Commands (High level)
clone
init
```

```
Plumbing Commnads (Lower Level)
hash-object
cat-file
```