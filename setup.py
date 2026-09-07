from setuptools import setup, find_packages


setup(
    name="signal visualizer",
    version="0.0.1",
    author="",
    author_email="",
    url="",
    description="Application for signal visualization",
    packages=find_packages(
        include=[
            "dexterous_bioprosthesis_sig_visual",
            "dexterous_bioprosthesis_sig_visual.*",
        ]
    ),
    install_requires=[
        "dexterous_bioprosthesis_2021_raw_datasets @ git+https://github.com/ptrajdos/dexterous-bioprosthesis-2021-raw-dataset.git",
        "matplotlib>=3.8.3",
    ],
    extras_require={
        "dev": [
            "coverage>=7.2.5",
            "pyinstaller>=6.6.0",
            "setuptools>=69.5.1",
            "pdoc3>=0.11.1, <0.12",
            "pylint>=3.3.9, <4.0.0",
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=2.0.0"
        ],
    },
    test_suite="test",
)
