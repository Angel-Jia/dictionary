# -*- coding:utf-8 -*-
import re
import urllib2

word_pattern = re.compile(r'<a class="word dynamictext".*?>(.*?)</a>')
word_definition = re.compile(r'<div class="definition">(.*?)</div>')

address = ["1319921", "1319959", "1319996", "1320011", "1320964", "1321073", "1321078", "1321079", "1350658", "1350664", "1377707", "1378388", "1378416", "1378444"]
with open("word_list_in_latex", 'w') as output:
    output.write("\\documentclass{article}\n\\usepackage{geometry}\n"
                 "\\geometry{left=2.0cm,right=2.0cm, top=1.5cm,bottom=1.5cm}\n"
                 "\\usepackage{multicol}\n\\begin{document}\n\\begin{multicols}{2}\n")
    for addr in address:
        response = urllib2.urlopen('https://www.vocabulary.com/lists/' + addr)
        html = response.read()
        words = re.findall(word_pattern, html)
        definitions = re.findall(word_definition, html)

        length = len(words)
        i = 0

        while i < length:
            output.write("\\textbf{\huge{%s}}  \\\\\n" % words[i])
            output.write("\\normalsize{%s}  \\\\\n" % definitions[i])
            i += 1
    output.write("\\end{multicols}\n\\end{document}\n")

