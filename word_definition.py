# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium.common.exceptions
import os

file_name = raw_input("input file name(no postfix): ")
if not os.path.isfile(file_name + '.txt'):
    print "%s not exit" % file_name
    exit(0)
input_file_object = open(file_name + '.txt')
output_file_object = open(file_name + '_definition.md', 'w')
failed_file_object = open(file_name + '_definition_failed.txt', 'w')

pwd = os.getcwd()
Chrome_Path = pwd + r'\chromedriver.exe'

PROXY = r'127.0.0.1:8087'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(Chrome_Path, chrome_options=chrome_options)
output_file_object.write("-----\n")

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
        output_file_object.write("# " + word + "\n")
        try:
            word_definition = driver.find_element_by_xpath('//p[@class="short"]')
            output_file_object.write("- definition: %s\n" % (word_definition.text.encode('utf-8')))
            try:
                word_etymology = word_definition.find_element_by_xpath('../p[@class="long"]').text
                output_file_object.write("- etymology: %s\n" % (word_etymology.encode('utf-8')))
            except selenium.common.exceptions.NoSuchElementException:
                pass
        except selenium.common.exceptions.NoSuchElementException:
            pass

        cnt = 0
        for definition in driver.find_elements_by_xpath('//h3[@class="definition"]'):
            definition_type = definition.find_element_by_xpath('./a').get_attribute("title")
            output_file_object.write("%d. `%s` %s\n" % (cnt + 1, definition_type,
                                                        definition.text.splitlines()[1]))
            try:
                example = definition.find_element_by_xpath('../div[@class="defContent"]/div[@class="example"]')
                strong_word = example.find_element_by_xpath('./strong').text
                sentence = example.text.replace(strong_word, "**%s**" % strong_word)
                output_file_object.write("  - " + sentence.encode('utf-8') + '\n')
            except selenium.common.exceptions.NoSuchElementException:
                pass

            synonyms = definition.find_elements_by_xpath('../div[@class="defContent"]/dl')
            synonyms_line = r'  - **Synonyms:** '
            if synonyms and synonyms[0].find_element_by_xpath('./dt').text == u'Synonyms:':
                for synonym in synonyms[0].find_elements_by_xpath('./dd/a'):
                    synonyms_line = synonyms_line + synonym.text + r', '
                output_file_object.write(synonyms_line[0:-2].encode('utf-8') + "\n")
            cnt += 1
        output_file_object.write("\n-----\n")
finally:
    driver.quit()
input_file_object.close()
output_file_object.close()
failed_file_object.close()

