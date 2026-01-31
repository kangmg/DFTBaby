from distutils.core import setup, Extension
import numpy

ff_extension = Extension("ff", sources=["ff_pythonmodule.c", "ff.c", "linked_list.c", "input.c"],
                         include_dirs=[numpy.get_include()],
                         extra_link_args=["-lm", "-llapack"])

setup(name = "ff",
      version = "0.0.1",
      description = "Force field with periodic boundary conditions",
      ext_modules = [ff_extension])
