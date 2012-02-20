########################################################################
#                                                                      #
#    f i n d c n t . p y                                               #
#                                                                      #
# Usage: findcnt.py --help | -h                                        #
#                                                                      #
# findcnt.py version 0.9                                               #
#                                                                      #
# Options:                                                             #
#   -h, --help       show this help message and exit                   #
#   -s PATTERN       single pattern, may be regex, OR:                 #
#   -l PATTERN_FILE  file containing patterns, one per line            #
#   -d SOURCES_FILE  single file OR: search recursive in this directory#
#   -t SOURCES_TYPE  resrict filenames to file-type, f.e.: 'php$'      #
#                                                                      #
########################################################################
#                                                                      #
# License: GNU General Public License version 3 or newer               #
# Date:    2012-02-17                                                  #
# Author:  sl0.self@googlemail.com                                     #
#                                                                      #
########################################################################
# This is file README.txt for patternmatching script.
# Its main purpose is to provide inline tests for the program.
# All the tests rely on intact content of file test1.dat
# test1.dat contains the lines in between the minus-signs:
#---------------------------
# class
# print
# for
# def
# if
# try:
#---------------------------
# To create a test1.dat, remoe the leading '# ' of the lines above
#
# The first test shows correctness of reading patterns into 
# the findcnt Object:

   >>> #coding=utf-8
   >>> 
   >>> from findcnt import findcnt, Patterns
   >>> p = Patterns("test1.dat")
   >>> print p.data.values()
   ['class', 'print', 'for', 'def', 'if', 'try:']

# Test findcnt Object the same way

   >>> s = findcnt("./","py$")
   >>> print s.data
   ['./findcnt.py']

# third Test, plain printout, remove ugly list symbols

   >>> for pp in s:
   ...     print pp,
   ./findcnt.py

# Now test MyCounters Object with data already read above

   >>> from findcnt import MyCounters
   >>> my_csv = MyCounters(p, s)
   >>> my_csv.count_patterns()
   Dateiname\Muster;class;print;for;def;if;try:;Summe
   ./findcnt.py;3;16;19;15;13;8;74

#
# Finally test sum_line
   >>> my_csv.sum_line()
   Summen;3;16;19;15;13;8;74



#
# these tests simulate the following commandline call
# ./findcnt.py -l test1.dat -d ./ -t 'py$'
#
# now only main() is untested, thats a simple user duty
# If you like it, please send me an email to
#                     sl0.self __at_ googlemail.com
#
# Have fun,
#      sl0
########################################################################
#EOF
