from __future__ import unicode_literals

"""This pattern was from

http://www.python.org/dev/peps/pep-0318/#examples

"""

def singleton(cls):
    """Make a class be singleton, for example

    ..

      @singleton
      class Foo(object):
         pass

    And use the Foo() everywhere

    """
    instances = {}
    def getinstance(*kargs, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*kargs, **kwargs)
        return instances[cls]
    return getinstance