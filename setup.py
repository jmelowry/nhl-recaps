from distutils.core import setup

setup(
    name='nhl-recaps',
    version='0.1dev',
    packages=['selenium','beautifulsoup4','dateparser'],
    license='MIT',
    long_description=open('README.txt').read(),
)
