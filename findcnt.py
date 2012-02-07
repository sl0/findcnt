#! /usr/bin/env python
#coding=utf-8
#
"""Module findcnt provides objects for investigation of files

Author:  sl0
Date:    February 7th, 2012
License: GNU General Public License Version 3 or newer

Input-Parameter
===============
-d für den Pfad (zu den Dateien, soll rekursiv durchsucht werden)
-t für den Dateityp (wenn nicht angegeben, alle Dateien durchsuchen)
-l Suchwort-Liste
-s einzelnes Suchwort

Ausgabeformat
=============
Dateiname-Suchwort1-Suchwort2-...-SuchwortN-Gesamttreffer
=========|=========|=========|===|=========|=============
Name1    ;Treffer11;Treffer12;   ;Treffer1N;1Nges
Name2    ;Treffer21;Treffer22;   ;Treffer2N;2Nges
...

"""

from UserDict import UserDict
from UserList import UserList
from optparse import OptionParser
import re
import sys
import os

class Patterns(UserDict):
    """Patterns object contains content of a file, one
    pattern each line; pattern may be regex in python style.
    """

    def __init__(self, filename=""):
        """initialize with content of patternfile"""
        UserDict.__init__(self)
        self.data = {}
        self.cnt = 1
        if len(filename) > 0:
            self.__read_pattern_file(filename)

    def set_pattern(self, pattern):
        """set one pattern manually"""
        self.data[1] = pattern

    def __read_pattern_file(self, filename):
        """reads file and creates self.data
        for every line read successfully
        """
        try:
            pfile = open(filename, 'r')
            for zeile in pfile:
                line = str(zeile.strip())
                self.data[self.cnt] = line
                self.cnt += 1
        except IOError, err:
            print filename + ": ", err.strerror

    def __repr__(self):
        """representaion of pattern-Object for printouts"""
        retstr = u''
        for key in self.data:
            st0 = u''
            try:
                st0 = u"# %-15s: %-59s #\n" % (key, str(self['key']))
                print "s:", st0
            except IOError, err:
                print err.strerror
                continue
            retstr += st0
        return retstr

    def headline(self):
        """do a nice Startline for our csv"""
        lin = ""
        #lin += u'"Dateiname\Muster";'
        lin += u'Dateiname\Muster;'
        for mus in self.data.values():
            #such = "\"%s\"" % (mus)
            such = "%s" % (mus)
            lin += such
            lin += ';'
        #lin += u'"Summe"'
        lin += u'Summe'
        print str(lin)

class findcnt(UserList):
    """findcnt object contains content of a file, one filename each line
    """

    def __init__(self, filename=None):
        """provide the list object"""
        UserList.__init__(self)
        self.data = []
        self.filetype = ""
        self.path = "."
        if filename:
            self.__read_file(filename)

    def set_filetype(self, ftype):
        """estension means filename ending"""
        self.filetype = ftype

    def read_many_files(self, pathname):
        """Returns all the filenamess in a directory as a list"""
        self.path = pathname
        try:
            for dirpath, dirnames, filenames in \
                    os.walk(pathname, topdown=False):
                #pylint meckert wg. unused dirnames 
                for fil in filenames:
                    full = os.path.join(dirpath, fil)
                    if len(self.filetype):
                        if re.search(self.filetype, fil):
                            self.data.append(full)
        except UnboundLocalError:
            pass


    def __read_file(self, filename):
        """initial read file into object"""
        try:
            myfile = open(filename, 'r')
            for zeile in myfile:
                line = str(zeile.strip())
                self.data.append(line)
        except IOError, err:
            print filename + ": ", err.strerror

    def __repr__(self):
        """representaion of findcnt-Object for printouts"""
        retstr = u''
        for key in self.data:
            st0 = u''
            try:
                st0 = u"# %-15s: %-59s #\n" % \
                    (key, str(self['key']))
                print "s:", st0
            except IOError, err:
                print err.strerror
                continue
            #except:
            #    continue
            retstr += st0
        return retstr

def count_one_pattern_one_line(muster, zeile):
    """ein Muster in einer Zeile Text finden"""
    retval = 0
    mat = re.search(muster, zeile)
    if mat:
        retval = 1
    return retval

def count_one_pattern_one_file(muster, datei):
    """ein Muster in einer Datei finden"""
    counter = 0
    try:
        fil0 = open(datei, 'r')
        while True:
            line = fil0.readline()
            if not line:
                break
            counter += count_one_pattern_one_line(muster, line)
        fil0.close()
    except IOError, err:
        print datei + ": ", err.strerror
    return counter


class MyCounters(object):
    """MyCounters contains all the stuff needed"""

    def __init__(self, muster, dateien):
        self.muster = muster
        self.all = dateien.data
        self.sums_line = {}

    def count_patterns(self):
        """do it all, not ready"""
        self.muster.headline()
        for fil in self.all:
            fsum = 0
            lin = ""
            tmp_list = []
            #tmp_list.append("\"%s\";" % (fil))
            tmp_list.append("%s;" % (fil))
            for mus in self.muster.values():
                cnt = count_one_pattern_one_file(mus, fil)
                try:
                    old = self.sums_line[mus]
                except KeyError, err:
                    old = 0
                self.sums_line[mus] = old + cnt
                fsum += cnt
                word = "%d;" % (cnt)
                tmp_list.append(word)
            fwrd = "%d" % (fsum)
            tmp_list.append(fwrd)
            for lwrd in tmp_list:
                lin += lwrd
            print lin

    def sum_line(self):
        """give us the last line of the csv"""
        retstr = "Summen"
        vsum = 0
        for mus in self.muster.values():
            vsum += self.sums_line[mus]
            retstr += ";%d" % (self.sums_line[mus])
        retstr += ";%d" % vsum
        print retstr
        return


def main():
    """ main(), for test and daily usage
    Options, 2 must be given
    -d für den Pfad (zu den Dateien, soll rekursiv durchsucht werden)
    -t für den Dateityp (wenn nicht angegeben, alle Dateien durchsuchen)
    -f für eine Datei mit Dateinamen (Alternative zu -d)
    -l Suchwort-Liste
    -s einzelnes Suchwort
    """
    usage = "usage: %prog --help | -h \n\n%prog version 0.9"
    parser = OptionParser(usage)
    parser.disable_interspersed_args()
    # long options not used for better readability
    parser.add_option("-s", "", #"--pattern",
                      dest = "pattern",
                      help="single pattern, may be regex, OR:")
    parser.add_option("-l", "", #"--pattern-list",
                      dest = "pattern_file",
                      help="file containing patterns, one per line")
    parser.add_option("-f", "", #"--file-of-files",
                      dest = "sources_file",
                      help="use this file only OR:")
    parser.add_option("-d", "", #"--path-to-files",
                      dest = "path_to_files",
                      help="directory, searched for plain files (recursive)")
    parser.add_option("-t", "", #"--file-type",
                      dest = "sources_type",
                      help="resrict filenames to file-type, f.e.: *tex")
    (options, args) = parser.parse_args()
    hlp = "\n\tplease use \"--help\" as argument, abort!\n"
    if options.sources_type == None:
        filetype = "[A-Za-z0-9]"
    else:
        filetype = options.sources_type
    if options.sources_file == None and options.path_to_files == None:
        print "\tNo files or directory given, " + hlp
        sys.exit(1)
    else:
        if options.sources_file:
            srcs = findcnt(options.sources_file)
        else:
            srcs = findcnt()
            srcs.set_filetype(filetype)
            srcs.read_many_files(options.path_to_files)
    if options.pattern_file == None and options.pattern == None:
        print "\tNo patterns_file given, " + hlp
        sys.exit(1)
    else:
        if options.pattern_file:
            patts = Patterns(options.pattern_file)
        else:
            patts = Patterns()
            patts.set_pattern(options.pattern)
    if len(args) != 0:
        parser.error("too many arguments, " + hlp)
        sys.exit(1)
    # now do the real job
    my_csv = MyCounters(patts, srcs)
    my_csv.count_patterns()
    my_csv.sum_line()
    sys.exit(0)

if __name__ == "__main__":
    main()
