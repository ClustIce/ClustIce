import jinja2 as jj

# from jinja2 import BaseLoader
import toml
import sys

proj = toml.load("pyproject.toml")
# env = jj.Environment(loader=BaseLoader)
# t = env.get_template(sys.stdin.read())
t = jj.Template(sys.stdin.read())
print(t.render(**proj))
