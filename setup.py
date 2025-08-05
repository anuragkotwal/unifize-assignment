from setuptools import setup, find_packages

setup(
    name='discount-service',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A discount service for an e-commerce platform handling various discount scenarios.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'decimal',  # Add any other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)