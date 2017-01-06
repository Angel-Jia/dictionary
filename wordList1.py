# -*- coding:utf-8 -*-
import re
import urllib2

word_pattern = re.compile(r'<a class="word dynamictext".*?>(.*?)</a>')

address = ["/lists/1395487", "/lists/1395488", "/lists/1395490", "/lists/1395491", "/lists/1395493", "/lists/1395492", "/lists/1395495", "/lists/1395496", "/lists/1395497", "/lists/1395498"]
i = 1
wordList_name = "economist-"
for addr in address:
    with open(wordList_name + str(i) + ".txt", 'w') as output:
        response = urllib2.urlopen('https://www.vocabulary.com' + addr)
        html = response.read()
        words = re.findall(word_pattern, html)
        i += 1

        for word in words:
            output.write(word + "\n")

