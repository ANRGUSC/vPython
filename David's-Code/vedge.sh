#/bin/sh
DIRECTORY='cover_dir-'$(date +'%b-%d-%Y->%H:%M:%S%Z')
echo $DIRECTORY
mkdir $DIRECTORY
touch $DIRECTORY/trace.log
python3.5 -m trace -g -s --count $1 >> $DIRECTORY/trace.log
#python3.5 -m trace -g -s --count -C $DIRECTORY/ -tg -m cProfile $1 >> $DIRECTORY/trace.log

