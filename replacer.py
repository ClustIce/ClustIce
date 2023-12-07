import jinja2 as jj

# from jinja2 import BaseLoader
import toml
import sys

proj = toml.load("pyproject.toml")
t = jj.Environment(loader=jj.FileSystemLoader(".")).from_string(sys.stdin.read())
print(t.render(**proj))
