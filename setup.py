from setuptools import setup

setup(
    name='kafkatunnel',
    version='0.2',
    py_modules=['kafkatunnel','Instance'],
    install_requires=[
        'Click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        kafkatunnel=kafkatunnel:cli
    '''
)
