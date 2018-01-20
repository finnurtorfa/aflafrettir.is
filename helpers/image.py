#!/usr/bin/env python
# -*- coding: utf-8 -*-
#pylint: disable-msg=E1101,W0603,W0212

import os, time
from threading import Thread

from PIL import Image
from flask import current_app

from app import db, imgs
from app.models import Image as Img
from app.models import Post

from helpers.text import get_all_imgs

_image_thread = None

def jpeg_convert(infile):
  """ Try to convert and compress an image to jpeg"""
  f, _ = os.path.splitext(infile)
  outfile = f + '.jpg'

  try:
    img = Image.open(infile)
    base_width = 932
    w, h = img.size

    if w > base_width:
      ratio = base_width/w
      new_height = int(h*ratio)

      img = img.resize((base_width, new_height), Image.ANTIALIAS)

    img.save(outfile, dpi=[100,100], quality=80)
  except IOError:
    current_app.logger.exception('Could not save file: ')
    return os.path.basename(infile)

  return os.path.basename(outfile)

def get_image_properties(path):
    """ Returns images base path, width and height in a tuple """
    try:
        img = Image.open('app{}'.format(path))
        width, height = img.size
    except FileNotFoundError as e:
        current_app.logger.error("Could not finde file: {}".format(path))
        return (None, None, None)

    return (os.path.basename(path), width, height)

def crop_image(infile):
  """ Crop an image. Check width and height, and crop according to the lower
  parameter from the center"""
  f, e = os.path.splitext(infile)
  outfile = f + '_crop' + e

  original = Image.open(infile)
  w, h = original.size
  max_width = 152

  if w < h:
    l = 0
    r = w
    t = (h // 2) - (w // 2)
    b = (h // 2) + (w // 2)
  elif h < w:
    l = (w // 2) - (h // 2)
    r = (w // 2) + (h // 2)
    t = 0
    b = h

  cropped = original.crop((l,t,r,b))
  w, h = cropped.size

  if w > max_width and h > max_width:
    cropped = cropped.resize((max_width, max_width), Image.ANTIALIAS)

  cropped.save(outfile)

def remove_images(app):
  from datetime import datetime

  while True:
    time.sleep(1800)
    conf = app.config['IMAGE_DELETE']
    with app.app_context():
      if ( datetime.utcnow().hour in conf['TIME_OF_DAY'] and
           datetime.utcnow().weekday() in conf['WEEKDAY'] ):
        images = Img.get_all_imgs()
        db_imgs = [img.location + img.filename for img in images]

        posts = Post.get_all()
        post_imgs = get_all_imgs((post.body_html for post in posts))

        diff_imgs = set(db_imgs) - set(post_imgs)

        if diff_imgs:
          app.logger.debug('Images to delete: {}'.format(db_imgs))

        for i in images:
          if i.location + i.filename in diff_imgs:
            if os.path.isfile(imgs.path(i.filename)):
              os.remove(imgs.path(i.filename))
              f, e = os.path.splitext(i.filename)

              if os.path.isfile(imgs.path(f + '_crop' + e)):
                os.remove(imgs.path(f + '_crop' + e))
            db.session.delete(i)
            db.session.commit()

def start_image_deletion_thread():
  if not current_app.config['TESTING']:
    global _image_thread

    if _image_thread is None:
      _image_thread = Thread(target=remove_images,
                             args=[current_app._get_current_object()])

      current_app.logger.debug('Starting image deletion thread')
      _image_thread.start()
