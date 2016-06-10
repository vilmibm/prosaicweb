#!/usr/bin/env python

from setuptools import setup

setup(
    name='prosaicweb',
    version='1.0.0',
    description='web frontend to prosaic',
    url='https://github.com/nathanielksmith/prosaicweb',
    author='nathaniel k smith',
    author_email='nathanielksmith@gmail.com',
    license='AGPL',
    classifiers=[
        'Topic :: Artistic Software',
        'License :: OSI Approved :: Affero GNU General Public License v3 (AGPLv3)',
    ],
    packages=['prosaicweb'],
    install_requires = ['SQLAlchemy==1.0.12',
                        'flask==0.11.1',
                        'psycopg2==2.6.1',
                        'prosaic==4.0.0'],
    entry_points = {
          'console_scripts': [
              'prosaicweb = prosaicweb.__init__:main'
          ]
    },
)
