import setuptools 

from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

print(find_packages())
setuptools.setup(
	name = 'resumeassistant',
	version = '0.0.0',
	author = 'Harish Sita',
	author_email = 'harish2sista@gmail.com',
	description = 'Resume Assistant',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/harish2sista/resumeassistant.git',
	project_urls = {
		'Bug Tracker': 'https://github.com/harish2sista/resumeassistant.git'
	},
	license = 'BSD 3-Clause License',
	packages = find_packages(),
	install_requires = ['openai', 'pdf2image', 'poppler']
	)