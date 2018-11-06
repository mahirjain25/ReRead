from sys import argv
import nltk
import language_check

inp_file = argv[1]
out_file = argv[2]

f = open(inp_file, 'r')

s = f.read()
# print(s)

tool = language_check.LanguageTool('en-US')
matches = tool.check(s)

language_check.correct(s, matches)

f.close()

new_f = open(out_file, 'w')
new_f.write(s)

new_f.close()