from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='VKapi',
      version=version,
      description="VKontakte api in python for server side script or computer application",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='vkontakte api',
      author='Lo\xc3\xafc Faure-Lacroix',
      author_email='lamerstar@gmail.com',
      url='http://delicieuxgateau.ca',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
