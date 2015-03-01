from flask import render_template, current_app, after_this_request

from . import feed
from ..models import Post

@feed.route('/', alias=True)
@feed.route('/frettir')
@feed.route('/frettir/<int:page>')
def index(page=1):
  #pylint: disable-msg=W0612
  @after_this_request
  def add_header(response):
    response.headers['Content-type'] = 'text/xml'
    return response

  posts = Post.get_per_page(page, current_app.config['POSTS_PER_PAGE'])

  return render_template('rss/news.html',
                         posts=posts)

@feed.route('/frettir/flokkur/<int:cid>')
@feed.route('/frettir/flokkur/<int:cid>/sida/<int:page>')
def category(cid, page=1):
  #pylint: disable-msg=W0612
  @after_this_request
  def add_header(response):
    response.headers['Content-type'] = 'text/xml'
    return response

  posts = Post.get_by_category(cid, page, current_app.config['POSTS_PER_PAGE'])

  return render_template('rss/news.html',
                         posts=posts)
