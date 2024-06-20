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
                'dexterous_bioprosthesis_2021_raw_datasets @ git+https://github.com/ptrajdos/dexterous-bioprosthesis-2021-raw-dataset.git@72a8b9be4498680f024da6f57f54316b02fa89ba',
                'matplotlib==3.8.3',
                
        ],
        test_suite='test'
        )
