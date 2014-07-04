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

def truncate(string, length=250, suffix=' ...'):
  if len(string) <= length:
    return string
  else:
    list_out = string[:length+1].split(' ')[0:-1]
    last = list_out[-1]
    last = '<span class="readmore">' + last + suffix + '</span>'
    list_out[-1] = last
    return ' '.join(list_out)

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
    
def time_ago(from_date, since_date=None, target_tz=None):
  import datetime

  if not since_date:
    since_date = datetime.datetime.now(target_tz)

  distance_in_time = since_date - from_date
  distance_in_seconds = distance_in_time.days*86400 + distance_in_time.seconds
  distance_in_minutes = distance_in_seconds//60

  if distance_in_minutes <= 1:
    return 'fyrir um mínútu'
  elif distance_in_minutes <= 45:
    return 'fyrir {0} mínútum'.format(distance_in_minutes)
  elif distance_in_minutes <= 90:
    return 'fyrir um klukkustund'
  elif distance_in_minutes <= 1440:
    return 'fyrir um {0} klukkustundum'.format(distance_in_minutes//60)
  elif distance_in_minutes <= 2880:
    return 'fyrir 1 degi'
  elif distance_in_minutes <= 43220:
    return 'fyrir {0} dögum'.format(distance_in_minutes//1440)
  elif distance_in_minutes <= 86400:
    return 'fyrir um 1 mánuði'
  elif distance_in_minutes <= 525600:
    return 'fyrir um {0} mánuðum'.format(distance_in_minutes//43200)
  elif distance_in_minutes <= 1051200:
    return 'fyrir um 1 ári'
  else:
    return 'fyrir um {0} árum'.format(distance_in_minutes//525600)
