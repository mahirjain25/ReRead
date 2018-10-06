'''Creates a summary from a given file. First argument is the input file. Second is the output file. Output file need not be created at the time of calling this script'''
import os
import sys


inputFile = sys.argv[1]
outputFile = sys.argv[2]

bashCommand = "sumy lex-rank --length=100% --file={} >> {}".format(inputFile, outputFile)

os.system(bashCommand)
