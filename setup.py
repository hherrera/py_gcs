from setuptools import setup, find_packages

setup(
    name="py_gcs_library",
    version="1.0",
    packages=find_packages(),
        entry_points = {
        'console_scripts': ['gcs=cli:app']}
)