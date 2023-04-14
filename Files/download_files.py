# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 20:40:05 2021

@author: amitk
"""

# Download Files from Project Grutenberg

import urllib
import codecs

text_list = [66618, 66619, 66620, 66621, 66622]
for i in text_list:
    url = f"https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt"
    file = urllib.request.urlopen(url)
    
    decoded_text = ''
    for line in file:
        decoded_line = line.decode("utf-8")
        decoded_text = decoded_text + '\n' + decoded_line
        
    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for ele in decoded_text:  
        if ele in punc:  
            decoded_text = decoded_text.replace(ele, " ")  

    decoded_text = decoded_text.lower()
    
    text_file = codecs.open(f"C:\\Users\\amitk\\Desktop\\Assignment\\Engr-E516\\Assignment4\\Files\\book_{i}.txt", "w", "utf-8")
    n = text_file.write(decoded_text)
    text_file.close()