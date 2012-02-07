########################################################################
#                                                                      #
#    f i n d c n t . p y                                               #
#                                                                      #
# Usage: findcnt.py --help | -h                                        #
#                                                                      #
# findcnt.py version 0.9                                               #
#                                                                      #
# Options:                                                             #
#   -h, --help        show this help message and exit                  #
#   -s PATTERN        single pattern, may be regex, OR:                #
#   -l PATTERN_FILE   file containing patterns, one per line           #
#   -f SOURCES_FILE   use this file only OR:                           #
#   -d PATH_TO_FILES  directory, searched for plain files (recursive)  #
#   -t SOURCES_TYPE   resrict filenames to file-type, f.e.: *tex       #
#                                                                      #
#                                                                      #
########################################################################
#                                                                      #
# License: GNU General Public License version 3 or newer               #
# Date:    2012-02-07                                                  #
# Author:  sl0.self@googlemail.com                                     #
#                                                                      #
########################################################################
# This is file README.txt for my patternmatching script.
# Its main purpose is to provide inline tests for the program.
# The tests rely on intact content of files test1.dat and test2.dat
# the first test shows correctness of reading patterns into 
# the findcnt Object:

   >>> #coding=utf-8
   >>> 
   >>> from findcnt import findcnt, Patterns
   >>> p = Patterns("test1.dat")
   >>> print p.data.values()
   ['eins', 'zwei', 'drei', 'der', 'die', 'das', 'class', 'for', 'def']


# Test findcnt Object the same way

   >>> s = findcnt("test2.dat")
   >>> print s.data
   ['README.txt', 'findcnt.py', 'Makefile']

# third Test, plain printout, remove ugly list symbols

   >>> for pp in s:
   ...     print pp,
   README.txt findcnt.py Makefile

# Now test MyCounters Object with data already read above

   >>> from findcnt import MyCounters
   >>> my_csv = MyCounters(p, s)
   >>> my_csv.count_patterns()
   Dateiname\Muster;eins;zwei;drei;der;die;das;class;for;def;Summe
   README.txt;2;2;2;2;2;2;2;6;2;22
   findcnt.py;0;0;0;0;0;0;3;20;16;39
   Makefile;0;0;0;0;0;0;0;0;0;0

# Finally test sum_line
   >>> my_csv.sum_line()
   Summen;2;2;2;2;2;2;5;26;18;61

# now only main() is untested, thats a simple user duty
# If you like it, please send me an email to
#                     sl0.self __at_ googlemail.com
#
# Have fun,
#      sl0
########################################################################
#EOF
