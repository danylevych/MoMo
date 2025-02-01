from setuptools import setup, find_packages

setup(
    name='momo-morphological-modeling',
    version='1.3.0',
    description='MoMo is a module that does Morphological Modeling',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Oleh Danylevych',
    author_email='danylevych123@email.com',
    url='https://github.com/danylevych/MoMo',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
