import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyRofex",
    version="0.4.2rc1",
    author="Franco Zanuso",
    author_email="francozanuso89@gmail.com",
    description="Python connector for ROFEX's Rest and Websocket APIs.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/gruporofex/pyRofex",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests>=2.20.0',
        'simplejson>=3.10.0',
        'enum34>=1.1.6',
        'websocket-client>=0.54.0,<0.58.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development"
    ],
)