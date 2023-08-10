# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License (jvherck on GitHub)

from setuptools import setup, find_packages
from roastedbyai import __version__

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="roastedbyai",
    version=__version__,
    license="CC BY-NC-SA 4.0",
    author="jvherck",
    author_email="contact@janvh.be",
    maintainer="jvherck",
    maintainer_email="contact@janvh.be",
    url="https://github.com/jvherck/roastedbyai",
    project_urls={"Documentation": "https://github.com/jvherck/roastedbyai", "Source": "https://github.com/jvherck/roastedbyai", "Tracker": "https://github.com/jvherck/roastedbyai/issues"},
    description="A package to roast and get roasted by AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests', 'brotli'],
    python_requires='>=3.7',
    keywords=['python', 'ai', 'roasting', 'roasted', 'roast', 'roastedbyai'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS", # :: MacOS X
        "Operating System :: Microsoft :: Windows",
        "License :: Free for non-commercial use",
        "Topic :: Games/Entertainment",
        "Topic :: Other/Nonlisted Topic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
