from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='diakaplug',
  version='0.0.2',
  description='a simple python library to receive notifications from diaka.ua',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/d3kxrma/diakaplug',  
  author='dekxrma',
  author_email='qqdjnuxez@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='python, diaka, diaka api, diakapy',
  packages=find_packages(),
  install_requires=['sseclient', 'aiosseclient', 'requests', 'aiohttp', 'bs4'] 
)