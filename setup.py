import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="while-transpiler",
    version="0.0.1",
    author="Steven Shan",
    author_email="dev@stevenshan.com",
    description="Transpiler written in Python to convert WHILE source code to C.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stevenshan/while-transpiler",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'whiletranspiler=whiletranspiler:main',
        ],
    },
    install_requires=[
        "Flask",
        "python-socketio",
    ],
    include_package_data=True,
    zip_safe=False,
)
