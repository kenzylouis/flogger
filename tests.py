# Set the path
import sys, pathlib, os
# sys.path.append(pathlib.Path(__file__).parents[0]) 
'''
had this error when using pathlib

ERROR: author.tests (unittest.loader._FailedTest)
----------------------------------------------------------------------
ImportError: Failed to import test module: author.tests
Traceback (most recent call last):
  File "/Users/klouis/projects/Anaconda/install/anaconda3/lib/python3.7/unittest/loader.py", line 436, in _find_test_path
    module = self._get_module_from_name(name)
  File "/Users/klouis/projects/Anaconda/install/anaconda3/lib/python3.7/unittest/loader.py", line 377, in _get_module_from_name
    __import__(name)
  File "/Users/klouis/projects/flogger/author/tests.py", line 10, in <module>
    from author.models import Author
  File "/Users/klouis/projects/flogger/author/models.py", line 1, in <module>
    from application import db
  File "/Users/klouis/projects/flogger/application.py", line 4, in <module>
    from flaskext.markdown import Markdown
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/flaskext/markdown.py", line 33, in <module>
    import markdown as md
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/markdown/__init__.py", line 25, in <module>
    from .core import Markdown, markdown, markdownFromFile
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/markdown/core.py", line 29, in <module>
    import pkg_resources
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3251, in <module>
    @_call_aside
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3235, in _call_aside
    f(*args, **kwargs)
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3279, in _initialize_master_working_set
    for dist in working_set
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3279, in <genexpr>
    for dist in working_set
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/pkg_resources/__init__.py", line 2785, in activate
    declare_namespace(pkg)
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/pkg_resources/__init__.py", line 2284, in declare_namespace
    _handle_ns(packageName, path_item)
  File "/Users/klouis/projects/flogger/.env/lib/python3.7/site-packages/pkg_resources/__init__.py", line 2201, in _handle_ns
    loader = importer.find_module(packageName)
  File "<frozen importlib._bootstrap_external>", line 431, in _find_module_shim
  File "<frozen importlib._bootstrap_external>", line 1346, in find_loader
  File "<frozen importlib._bootstrap_external>", line 1391, in find_spec
  File "<frozen importlib._bootstrap_external>", line 59, in _path_join
  File "<frozen importlib._bootstrap_external>", line 59, in <listcomp>
AttributeError: 'PosixPath' object has no attribute 'rstrip'
ERROR: blog.tests (unittest.loader._FailedTest)

'''
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import unittest
loader = unittest.TestLoader()
tests = loader.discover('.')
testRunner = unittest.runner.TextTestRunner()

if __name__ == "__main__":
    testRunner.run(tests)