import jinja2 as jj

# from jinja2 import BaseLoader
import toml
import sys

version = "0.0.0"
proj = toml.load("pyproject.toml")
proj["version"] = version
t = jj.Environment(loader=jj.FileSystemLoader(".")).from_string(sys.stdin.read())
print(t.render(**proj))
