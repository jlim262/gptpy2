from setuptools import setup, find_packages

setup(
    name="gptpy2",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # list your package dependencies
        'openai>=1.3.8'
    ],
    # Additional metadata about your package
)
