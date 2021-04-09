import os
import setuptools

from sphinx.setup_command import BuildDoc

import retry_pytest

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('install_requires.txt', 'r') as ir:
    install_requires = [item.strip('\n') for item in ir.readlines()]

version = os.environ.get('PKG_VERSION') or retry_pytest.__version__

dependency_links = []

setuptools.setup(
    name=retry_pytest.__name__.lower(),
    version=version,
    author=retry_pytest.__author__,
    author_email=retry_pytest.__author_email__,
    description='retry_pytest',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=install_requires,
    dependency_links=dependency_links,
    url='https://github.com/Shumodan/retry-pytest',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
    ],
    cmdclass={'build_doc': BuildDoc},
    command_options={
        'build_doc': {
            'project': ('setup.py', retry_pytest.__name__),
            'version': ('setup.py', version),
            'source_dir': ('setup.py', os.path.join(retry_pytest.__name__, 'docs', 'source')),
            'build_dir': ('setup.py', os.path.join(retry_pytest.__name__, 'docs', 'build'))
        }
    },
    package_data={
        f'{retry_pytest.__name__}.docs.build': ['html/*', 'html/*/*'],
    },
)
