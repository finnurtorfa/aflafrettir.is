#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PIL import Image

def crop_image(infile):
  f, e = os.path.splitext(infile)
  outfile = f + '_crop' + e

  original = Image.open(infile)
  w, h = original.size

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
  cropped.save(outfile)

  

