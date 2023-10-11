#     retry_pytest is a library for pytest test framework
#     Copyright (C) 2021  Alexander Evdokimov
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


import nox


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', '--exclude=.nox/', '.')


@nox.session
def test(session):
    session.install('pytest')
    session.log('test')


@nox.session
def build(session):
    session.install('wheel')
    session.install('sphinx==6.1.3')
    session.install('-r', 'install_requires.txt')
    session.run('python', 'setup.py', 'build_doc')
    session.run('python', 'setup.py', 'sdist', 'bdist_wheel')


@nox.session
def upload(session):
    session.install('twine')
    session.run('twine', 'upload', 'dist/*')


@nox.session
def test_upload(session):
    session.install('twine')
    session.run('twine', 'upload', '--repository', 'testpypi', 'dist/*')
