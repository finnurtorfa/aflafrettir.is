#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PIL import Image

def jpeg_convert(infile):
  """ Try to convert and compress an image to jpeg"""
  f, e = os.path.splitext(infile)
  outfile = f + '.jpg'

  try:
    img = Image.open(infile)
    base_width = 975
    w, h = img.size

    if w > base_width:
      ratio = base_width/w
      new_height = int(h*ratio)

      img = img.resize((base_width, new_height), Image.ANTIALIAS)
    
    img.save(outfile, dpi=[100,100], quality=80)
  except IOError:
    return os.path.basename(infile)
  
  return os.path.basename(outfile)

def crop_image(infile):
  """ Crop an image. Check width and height, and crop according to the lower
  parameter from the center"""
  f, e = os.path.splitext(infile)
  outfile = f + '_crop' + e

  original = Image.open(infile)
  w, h = original.size
  max_width

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
