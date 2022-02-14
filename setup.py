from setuptools import setup


setup(
    name="customtwitterapi",
    version='0.0.1',
    author='Zhivar Sourati',
    author_email='zhivarsourati@gmail.com',
    install_requires=[
        'requests'
    ],
    package_dir={'': '.'},
    packages=['customtwitterapi']
)
