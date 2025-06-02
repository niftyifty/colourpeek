from setuptools import setup

setup(
    name="colourpeek",
    version="1.0.0",
    packages=["colourpeek"],
    install_requires=[
        "colorthief",
        "climage",
    ],
    entry_points={
        "console_scripts": [
            "colourpeek = colourpeek.__main__:main",
        ],
    },
    author="Your Name",
    description="Preview image and extract dominant colours",
)
