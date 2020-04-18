chmod a+x main.py
DIR=~/local1/
if [ -d "$DIR" ]; then
    echo "$DIR exist"

else
    echo "$DIR does not exist"
    mkdir ~/local1/
    echo "$DIR NOW CREATED"
fi
cp main.py ~/local1/
ln -s main.py ~/local1/willy
FILE=~/.bash_profile
if [ -f "$FILE" ]; then
    echo "$FILE exist"
    echo -e 'export PATH="$PATH:~/local1/willy"' >> ~/.bash_profile
else
    echo "$FILE does not exist"
    touch ~/.bash_profile
    echo -e 'export PATH="$PATH:~/local1/willy"' >> ~/.bash_profile
    echo "$FILE NOW CREATED"
fi
source ~/.bash_profile
echo "command willy has been added to ysudour path"