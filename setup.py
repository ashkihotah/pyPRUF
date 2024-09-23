from setuptools import setup

setup(
    name='pyPRUF',
    version='0.1.0',
    python_requires=">=3.11",   
    description='A Python library for PRUF, a meaning representation and manipulation language for approximate reasoning purposes, proposed by Zadeh.',
    url='https://github.com/ashkihotah/pyPRUF',
    author='Nicolò Resta',
    author_email='nicoloresta02@gmail.com',
    license='LGPL-3.0-or-later',
    packages=['pyPRUF'],
    install_requires=['pandas'],

    # classifiers=[
    #     'Development Status :: 1 - Planning',
    #     'Intended Audience :: Science/Research',
    #     'License :: OSI Approved :: BSD License',  
    #     'Operating System :: POSIX :: Linux',        
    #     'Programming Language :: Python :: 2',
    #     'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.4',
    #     'Programming Language :: Python :: 3.5',
    # ],
)
