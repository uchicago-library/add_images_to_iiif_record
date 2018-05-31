
from setuptools import setup, find_packages
from os import getcwd
from os.path import exists, join

def get_readme():
    path_to_readme = join(getcwd(), 'README.md')
    if exists(path_to_readme):
        content = open(path_to_readme, 'r', encoding='utf-8').read()
    else:
        content = 'A CLI application to take a IIIF record containing metadata only and append images from a list of IIIF links'
    return content
setup(
    name='CompletingTheIIIFRecord',
    version='1.0.0',
    author='Tyler Danstrom',
    author_email='tdanstrom@uchicago.edu',
    description='A CLI application to take a IIIF record containing metadata only and append images from a list of IIIF links',
    license='LGPL3.0',
    keywords='iiif presentation images cli',
    url='https://github.com/uchicago-library/add_images_to_iiif_record',
    packages=find_packages(),
    long_description=get_readme(),
    entry_points = {
                    
        'console_scripts': ['extend_record=AddingImages2IIIF.__main__:main']
    },
    dependency_links = [
        'https://github.com/uchicago-library/pyiiif/tarball/master#egg=pyiiif'
    ],
    install_requires = [
        'requests'
    ]
)