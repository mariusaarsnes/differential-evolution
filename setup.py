import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="simple-differential_evolution",
    version="0.0.1",
    author="mariusaarsnes",
    author_email="marius.aarsnes@gmail.com",
    description="A simple interface to run differential evolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mariusaarsnes/differential-evolution"
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "Licence :: OSI Approved :: MIT Licence",
                 "Operating System :: OS INdependent"],
    python_requires='>=3.6.8'
)
