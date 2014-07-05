#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unicodedata 

from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
  """ HTMLStripper class to strip HTML tags from a HTML document """
  def __init__(self):
    super(HTMLStripper, self).__init__()
    self.reset()
    self.fed = []
    self.escape = False

  def handle_starttag(self, tag, attrs):
    """ Handler for a opening of a tag like body, img, a, p etc. """
    if tag == 'table':
      self.escape = True

  def handle_endtag(self, tag):
    """ Handler for a closing of a tag like body, img, a, p etc. """
    if tag == 'table':
      self.escape = False

  def handle_data(self, d):
    """ Handler for the data inside tags """
    if not self.escape:
      self.fed.append(d)

  def get_data(self):
    """ Return the data collected by the parser """
    return ''.join(self.fed)

class HTMLThumbnailExtractor(HTMLParser):
  """ HTMLThumbnailExtractor class to get the url for the first image in a HTML
  document """
  def __init__(self):
    super(HTMLThumbnailExtractor, self).__init__()
    self.reset()
    self.thumbnail = ''

  def handle_starttag(self, tag, attrs):
    """ Handler for a opening of a tag like body, img, a, p etc. """
    if not self.thumbnail and tag == 'img':
      for attr in attrs:
        if attr[0] == 'src':
          self.thumbnail = attr[1]
          raise StopIteration


def slugify(string):
  """ Returns a URL friendly representation of a string """
  string = string.replace('æ', 'ae').replace('ð','d').replace('þ','th')\
                 .replace('!','').replace('?', '').replace('"', '')\
                 .replace('#', '').replace('%', '').replace('%', '')\
                 .replace('(', '').replace(')', '').replace('*', '')\
                 .replace("'", '').replace(',', '').replace('.', '')\
                 .replace('/', '').replace(':', '').replace(';', '')
  return unicodedata.normalize('NFKD', string)\
          .lower().replace(' ', '-').encode('ascii', 'ignore')

def remove_html_tags(string):
  """ Removes all HTML tags from a HTML document """
  s = HTMLStripper()
  s.feed(string)

  return s.get_data()

def truncate(string, length=250, suffix=' ...'):
  """ Returns the first 'length' characters from a string plus a suffix """
  if len(string) <= length:
    return string
  else:
    list_out = string[:length+1].split(' ')[0:-1]
    last = list_out[-1]
    last = '<span class="readmore">' + last + suffix + '</span>'
    list_out[-1] = last
    return ' '.join(list_out)

def get_thumbnail(html):
  """ Extracts the first image from a HTML document """
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
    
def time_ago(from_date, since_date=None):
  """ Returns distance in time between two datetime objects in words """
  import datetime

  if not since_date:
    since_date = datetime.datetime.utcnow()

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
