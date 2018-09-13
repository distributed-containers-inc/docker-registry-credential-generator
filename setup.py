import os

from setuptools import setup, find_packages

requires = [
  'kubernetes==7.0.0',
]

setup(
    name='dockerregistrycredgen',
    version='1.0',
    description='docker registry credential generator: sidecar to registry:2 which produces a cryptographically secure htpasswd file at /data/htpasswd if it does not already exist.',
    classifiers=[
      'Programming Language :: Python',
      'Framework :: Pyramid',
      'Topic :: Internet :: WWW/HTTP',
      'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Colin Chartier',
    author_email='colin@kubenow.com',
    url='https://kubenow.com',
    keywords='build ci deployment kubernetes',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
      'console_scripts': [
        'entrypoint = dockerregistrycredgen.main:main',
      ],
    },
)
