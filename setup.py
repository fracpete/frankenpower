from setuptools import setup


setup(
    name="frankenpower",
    description="Python 3 library for working with Frank Energy (NZ) usage data.",
    url="https://github.com/fracpete/frankenpower",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
    ],
    license='Apache 2.0 License',
    package_dir={
        '': 'src'
    },
    packages=[
        "fp",
    ],
    version="0.0.1",
    author='Peter "fracpete" Reutemann',
    author_email='fracpete@gmail.com',
    install_requires=[
        "pandas",
        "selenium",
    ],
    entry_points={
        "console_scripts": [
            "fp-download=fp.download:sys_main",
        ]
    }
)
