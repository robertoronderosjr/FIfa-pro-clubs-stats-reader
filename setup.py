import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fifa-pro-clubs-stats-reader",
    version="0.0.1",
    author="Roberto Ronderos",
    author_email="robertoronderosjr@gmail.com",
    description="Alpha version of tool to read stats from fifa pro club screen shots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertoronderosjr/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)