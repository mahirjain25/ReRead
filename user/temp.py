from sys import argv 
import os

def createSummaryFromFile(filepath,len_pct):
	inputFile, file_extension = filepath.split('.')
	print(inputFile)
	# if the input file is a pdf file
	if file_extension == "pdf":
		cmd = "pdftotext %s %s" % (inputFile, inputFile + ".txt")
		os.system(cmd)
		inputFile = inputFile + ".txt"

	outputFile = inputFile + '_abtracted.txt'
	print(outputFile)
	bashCommand = "sumy lex-rank --length={}% --file={} > {}".format(len_pct, inputFile+'.txt', outputFile)

	os.system(bashCommand)

filepath = argv[1]
len_pct = argv[2]

createSummaryFromFile(filepath, len_pct)
