import os

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
VERSION = open(os.path.join(here, 'VERSION')).read()
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()


def read_requirements(filename):
    content = open(os.path.join(here, filename)).read()
    requirements = map(lambda r: r.strip(), content.splitlines())
    return requirements


requirements = read_requirements('requirements.txt')
test_requirements = read_requirements('test-requirements.txt')


setup(
    name='vic_pyramid',
    version=VERSION,
    author='Victor Lin',
    author_email='bornstub@gmail.com',
    description="Victor's Pyramid Scaffold",
    long_description=README + '\n\n' + CHANGES,
    url='https://bitbucket.org/victorlin/vic_pyramid',
    classifiers=[
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    install_requires=requirements, 
    tests_require=test_requirements,
    entry_points=""" \
    [paste.paster_create_template]
    vic_pyramid=vic_pyramid.scaffolds:VictorPyramidTemplate
    [pyramid.scaffold]
    vic_pyramid=vic_pyramid.scaffolds:VictorPyramidTemplate
    """
)
