from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hr_sum_additionals/__init__.py
from hr_sum_additionals import __version__ as version

setup(
	name="hr_sum_additionals",
	version=version,
	description="1",
	author="1",
	author_email="1",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
