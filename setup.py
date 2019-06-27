import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='firefly-sqlalchemy',
    version='0.1',
    author="JD Williams",
    author_email="me@jdwilliams.xyz",
    description="SQL Alchemy support for Firefly.",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/firefly19/python-infrastructure-sqlalchemy",
    package_dir={'': 'src'},
    packages=setuptools.PEP420PackageFinder.find('src'),
    install_requires=['sqlalchemy>=1.3.3', 'firefly-framework>=0.1'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)
