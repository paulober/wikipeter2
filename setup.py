from setuptools import setup

# need setup.cfg
# setup()

# py_compile solution
# import py_compile
import re
import compileall
compileall.compile_dir(r".\wikipeter2", rx=re.compile(r'[/\\][.]git'))
