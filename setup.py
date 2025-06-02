from setuptools import setup, find_packages

setup(
    name="colourpeek",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "colorthief",
        "climage"
    ],
    entry_points={
        "console_scripts": [
            "colourpeek=colourpeek.__main__:main"
        ]
    },
    author="Your Name",
    description="A CLI tool to preview images and extract dominant colours.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
    ],
    python_requires='>=3.6',
)
