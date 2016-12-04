from flask import Blueprint
from collections import namedtuple
from importlib import import_module

class SayluaRouter(Blueprint):
  """URL Routing syntas xugar."""
  def register_urls(self, urls):
    for _url in urls:
      self.add_url_rule(rule=_url.rule, endpoint=_url.name, view_func=_url.view_func, methods=_url.methods)

def url(rule, view_func, name=None, methods=["GET"]):
  """Simple URL wrapper for SayluaRouter.

  Usage:
  ```
  from . import views

  url('/explore/', view_func=views.explore_home, name='explore_home', methods=['GET'])
  url('/explore/', view_func=views.explore_home, name='explore_home')
  url('/explore/', views.explore_home, 'explore_home')
  url('/explore/', views.explore_home)
  ```

  # Note that 'endpoint' is now 'name'.
  # Note also that the name and view_func parameters are reversed from that of
  a normal flask URL.
  """

  __url = namedtuple('Url', ['rule', 'name', 'view_func', 'methods'])
  return __url(rule, name, view_func, methods)

def register_urls(app, modules):
  """Don't try to understand this."""

  for module_name in modules:
    formatted_module = "saylua.modules.{}".format(module_name)
    __module = import_module(formatted_module)
    app.register_blueprint(__module.blueprint)
