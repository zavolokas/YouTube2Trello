from setuptools import setup, find_packages

install_requires = [
]

dev_requires = [
    "flake8>=3.3.0",
    "pip-tools==3.3.1",
]

setup(
    name="YouTube2Trello",
    version="1.0.0b",
    url="git@github.com:zavolokas/YouTube2Trello.git",
    author="zavolokas",
    author_email="",
    description="",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires,
    setup_requires=[],
    tests_require=dev_requires,
    extras_require={"dev": dev_requires},
)
