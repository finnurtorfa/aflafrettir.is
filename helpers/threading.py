from threading import Thread, Lock

list_lock = Lock()

def run_in_thread(app):
  def wrapper(fn):
    def run(*args, **kwargs):
      app.logger.info('Starting thread: {}'.format(fn.__name__))
      t = Thread(target=fn,
                 args=args,
                 kwargs=kwargs)
      t.start()

      return t

    return run

  return wrapper
