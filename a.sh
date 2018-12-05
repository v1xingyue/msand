cython msand.py --embed
gcc -o msand msand.c `python-config --libs` `python-config --includes`
