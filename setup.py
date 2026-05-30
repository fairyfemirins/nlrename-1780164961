from setuptools import setup, find_packages

setup(
    name="nlrename",
    version="0.1.0",
    py_modules=["nlrename"],
    install_requires=["click", "python-dateutil"],
    entry_points={"console_scripts": ["nlrename=nlrename:cli"]},
)