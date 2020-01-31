chmod a+x lexer.py
DIR=~/.local/bin
if [ -d "$DIR" ]; then
    echo "$DIR exist"

else 
    echo "$DIR does not exist"
    mkdir ~/.local/bin
fi
cp lexer.py ~/.local/bin
ln -s lexer.py ~/.local/bin/willy
FILE=~/.bash_profile
if [ -f "$FILE" ]; then
    echo "$FILE exist"
    echo -e 'export PATH="$PATH:~/.local/bin"' >> ~/.bash_profile
else 
    echo "$FILE does not exist"
    touch ~/.bash_profile
    echo -e 'export PATH="$PATH:~/.local/bin"' >> ~/.bash_profile
fi
source ~/.bash_profile