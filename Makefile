#############################################################
#
# This is Makefile for findcnt.py to make easiser test & dev
#
# Usage: findcnt.py --help | -h 
# 
# findcnt.py version 0.9
# 
# Options:
#   -h, --help        show this help message and exit
#   -s PATTERN        single pattern, may be regex, OR:
#   -l PATTERN_FILE   file containing patterns, one per line
#   -f SOURCES_FILE   use this file only OR:
#   -d PATH_TO_FILES  directory, searched for plain files (recursive)
#   -t SOURCES_TYPE   resrict filenames to file-type, f.e.: *tex
#
# Have fun
#      sl0
#
#############################################################

all:	findcnt.py test1.dat test2.dat
	@python findcnt.py -l test1.dat -f test2.dat

t:
	@clear
	@python -m doctest README.txt -v
	@rm *.pyc

r:
	@python findcnt.py -l regexen -d files

clean:
	rm -f *pyc

