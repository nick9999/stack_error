try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="stack_error",
    version="0.1",
    url="https://github.com/nick9999/stack_error",
    author="nick9999",
    author_email="nikhilpatil123@gmail.com",
    include_package_data=True,
    packages=["stack_error"],
    entry_points={"console_scripts": ["stack_error = stack_error.stack_error:main"]},
    install_requires=["BeautifulSoup4", "requests", "urllib3"],
    requires=["BeautifulSoup4", "requests", "urllib3"],
    license="MIT"
)