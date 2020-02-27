chmod a+x main.py
DIR=~/.local/bin
if [ -d "$DIR" ]; then
    echo "$DIR exist"

else 
    echo "$DIR does not exist"
    mkdir ~/.local/bin
    echo "$DIR NOW CREATED"
fi
cp main.py ~/.local/bin
ln -s main.py ~/.local/bin/willy
FILE=~/.bash_profile
if [ -f "$FILE" ]; then
    echo "$FILE exist"
    echo -e 'export PATH="$PATH:~/.local/bin"' >> ~/.bash_profile
else 
    echo "$FILE does not exist"
    touch ~/.bash_profile
    echo -e 'export PATH="$PATH:~/.local/bin"' >> ~/.bash_profile
    echo "$FILE NOW CREATED"
fi
source ~/.bash_profile
echo "command willy has been added to your path"