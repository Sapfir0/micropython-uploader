from setuptools import setup, find_packages

with open("README.md") as f:
    longDescr = f.read()

setup(
    name='micropython-uploader',
    version='0.1.5',
    packages=find_packages(),
    author='Alex Yurev',
    author_email='sapfir999999@yandex.ru',
    install_requires=['ampy'],
    license='MIT',

    long_description=longDescr,
    url='https://github.com/Sapfir0/micropython-uploader',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='hardware micropython circuitpython uploaders uploader ampy',
    entry_points={
            'console_scripts': [
                'mploader=uploader.uploader:uploader',
            ],
    },
)


