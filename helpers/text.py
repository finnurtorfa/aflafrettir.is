#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata 

from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
  def __init__(self):
    super(HTMLStripper, self).__init__()
    self.reset()
    self.fed = []

  def handle_starttag(self, tag, attrs):
    pass

  def handle_endtag(self, tag):
    pass

  def handle_data(self, d):
    self.fed.append(d)

  def get_data(self):
    return ''.join(self.fed)

def slugify(string):
  string = string.replace('æ', 'ae').replace('ð','d').replace('þ','th')\
                 .replace('!','').replace('?', '').replace('"', '')\
                 .replace('#', '').replace('%', '').replace('%', '')\
                 .replace('(', '').replace(')', '').replace('*', '')\
                 .replace("'", '').replace(',', '').replace('.', '')\
                 .replace('/', '').replace(':', '').replace(';', '')
  return unicodedata.normalize('NFKD', string)\
          .lower().replace(' ', '-').encode('ascii', 'ignore')

def remove_html_tags(string):
  s = HTMLStripper()
  s.feed(string)
  return s.get_data()

def truncate(string, length=250, suffix=''):
  if len(string) <= length:
    return string
  else:
    return ' '.join(string[:length+1].split(' ')[0:-1]) + suffix
