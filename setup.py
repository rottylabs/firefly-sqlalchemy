import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()


def configure_module():
    from firefly.infrastructure.framework import get_project_config, save_project_config
    section = 'sqlalchemy'
    config = get_project_config()
    if not config.has_section(section):
        config.add_section(section)
        config.set(section, 'namespace', 'firefly.sqlalchemy')
    save_project_config(config)


class PostDevelopCommand(develop):
    def run(self):
        configure_module()
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        configure_module()
        install.run(self)


setuptools.setup(
    name='firefly-infrastructure-sqlalchemy',
    version='0.1',
    author="JD Williams",
    author_email="me@jdwilliams.xyz",
    description="SQL Alchemy support for Firefly.",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/firefly19/python-infrastructure-sqlalchemy",
    package_dir={'': 'src'},
    packages=setuptools.PEP420PackageFinder.find('src'),
    install_requires=['sqlalchemy>=1.3.3', 'firefly-framework'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)
