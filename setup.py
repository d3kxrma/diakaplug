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
  version='0.0.1',
  description='a simple library to receive notifications from diaka.ua',
  long_description=open('README.md').read(),
  url='https://github.com/d3kxrma/diakaplug',  
  author='dekxrma',
  author_email='qqdjnuxez@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['sseclient', 'aiosseclient', 'requests', 'aiohttp', 'bs4'] 
)