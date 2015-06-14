from os import walk, remove

def get_all_files(directory):
  """ Method for listing files within a directory
  """
  f = []
  for (_, _, filenames) in walk(directory):
    f.extend(filenames)

  return f

def remove_file(filename, directory):
  """ Method for removing a file within a directory
  """
  try:
    remove(directory + '/' + filename)
  except FileNotFoundError:
    pass
