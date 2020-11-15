from setuptools import setup, find_packages

setup(
    name='stock_digest',
    version='0.1.1',
    author='Lucas Hadfield',
    packages=find_packages(),
    entry_points={'console_scripts': ['stock_digest = stock_digest.main:main']},
)
