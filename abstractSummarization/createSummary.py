'''Creates a summary from a given file. First argument is the input file. Second is the output file. Output file need not be created at the time of calling this script'''
import os
import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]

filename, file_extension = os.path.splitext('dependencies.txt')

# if the input file is a pdf file
if file_extension == ".pdf":
    cmd = "pdftotext %s %s" % (inputFile, inputFile + ".txt")
    os.system(cmd)
    inputFile = inputFile + ".txt"


bashCommand = "sumy lex-rank --length=100% --file={} >> {}".format(inputFile, outputFile)

os.system(bashCommand)
