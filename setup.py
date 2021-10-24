""" Install autofile
"""

from distutils.core import setup


setup(
    name="autofile",
    version="0.4.0",
    packages=[
        "autofile",
        "autofile.data_types",
        "autofile.schema",
        "autofile.info"
    ]
)
