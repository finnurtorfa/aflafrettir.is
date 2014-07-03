#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unicodedata 

from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
  def __init__(self):
    super(HTMLStripper, self).__init__()
    self.reset()
    self.fed = []
    self.escape = False

  def handle_starttag(self, tag, attrs):
    if tag == 'table':
      self.escape = True

  def handle_endtag(self, tag):
    if tag == 'table':
      self.escape = False

  def handle_data(self, d):
    if not self.escape:
      self.fed.append(d)

  def get_data(self):
    return ''.join(self.fed)

class HTMLThumbnailExtractor(HTMLParser):
  def __init__(self):
    super(HTMLThumbnailExtractor, self).__init__()
    self.reset()
    self.thumbnail = ''

  def handle_starttag(self, tag, attrs):
    if not self.thumbnail and tag == 'img':
      for attr in attrs:
        if attr[0] == 'src':
          self.thumbnail = attr[1]
          raise StopIteration


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

def get_thumbnail(html):
  s = HTMLThumbnailExtractor()
  try:
    s.feed(html)
  except StopIteration:
    pass

  if s.thumbnail:
    f, e = os.path.splitext(s.thumbnail)
    thumbnail = f + '_crop' + e
    return os.path.split(thumbnail)

  return os.path.split(s.thumbnail)
    


