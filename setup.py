from setuptools import setup, find_packages



setup(
        name='signal visualizer',
        version ='0.0.1',
        author='',
        author_email='',
        url = '',
        description="Application for signal visualization",
        packages=find_packages(include=[
                'dexterous_bioprosthesis_sig_visual',
                'dexterous_bioprosthesis_sig_visual.*',
                ]),
        install_requires=[ 
                'dexterous_bioprosthesis_2021_raw_datasets @ git+https://github.com/ptrajdos/dexterous-bioprosthesis-2021-raw-dataset.git@ba0f6f256a5d75af3d3129c998afba9a85a14658',
                'matplotlib==3.8.3',
                
        ],
        test_suite='test'
        )
