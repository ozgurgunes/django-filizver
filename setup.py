# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re

# Dynamically calculate the version based on filizver.VERSION.
VERSION = (0, 1, 0, 'alpha', 0)

def get_version(version=None):
    """Derives a PEP386-compliant version number from VERSION."""
    if version is None:
        version = VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        # At the toplevel, this would cause an import loop.
        from django.utils.version import get_svn_revision
        svn_revision = get_svn_revision()[4:]
        if svn_revision != 'unknown':
            sub = '.dev%s' % svn_revision

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links
    
setup(
    name="django-filizver",
    version=get_version(),
    description = "A package to help automate creation of web applications in Django",
    long_description=open("README").read(),
    author = "Ozgur Gunes",
    author_email = "o.gunes@gmail.com",
    url = "http://github.com/ozgurgunes/django-filizver/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    include_package_data=True,
    zip_safe=False,
)
