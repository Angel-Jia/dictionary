# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.common.exceptions
import os

file_name = raw_input("input file name(no postfix): ")
if not os.path.isfile(file_name + '.txt'):
    print "%s not exit" % file_name
    exit(0)
input_file_object = open(file_name + '.txt')
output_file_object = open(file_name + '_usage.md', 'w')
failed_file_object = open(file_name + '_usage_failed.txt', 'w')

pwd = os.getcwd()
Chrome_Path = pwd + r'\chromedriver.exe'

PROXY = r'127.0.0.1:8087'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(Chrome_Path, chrome_options=chrome_options)

try:
    for word in input_file_object.readlines():
        word = word.rstrip()
        url = 'https://www.vocabulary.com/dictionary/' + str(word)
        driver.implicitly_wait(5)
        driver.get(url)

        word_found = driver.find_element_by_xpath('//h1[@class="dynamictext"]')
        if str(word_found.text) != word:
            failed_file_object.write(word + ' can not be found.')
            continue

        cnt = 1
        try:
            usage_examples = driver.find_elements_by_xpath('//div[@class="sentence"]')
            strong_word = driver.find_elements_by_xpath('//div[@class="sentence"]/strong')
            for sentence in usage_examples:
                if cnt > 3:
                    break
                sentence_md = sentence.text.replace(strong_word[cnt - 1].text, u'**' + strong_word[cnt - 1].text + u'**')
                output_file_object.write(sentence_md.encode('utf-8'))
                output_file_object.write('\n')
                cnt += 1
        except selenium.common.exceptions.NoSuchElementException as e:
            print "word " + word + "has no usage example"
            failed_file_object.write(word)
            failed_file_object.write('\n')
finally:
    driver.quit()
input_file_object.close()
output_file_object.close()
failed_file_object.close()

os.system("python disorder.py %s" % (file_name + '_usage'))
