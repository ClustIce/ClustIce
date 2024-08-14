import jinja2 as jj
from clustice import __version__

# from jinja2 import BaseLoader
import toml
import sys

proj = toml.load("pyproject.toml")
proj["version"] = __version__
t = jj.Environment(loader=jj.FileSystemLoader(".")).from_string(sys.stdin.read())
print(t.render(**proj))
