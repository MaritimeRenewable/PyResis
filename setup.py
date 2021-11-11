import setuptools

setuptools.setup(
    name='PyResis',
    version='1.0.2',
    packages=setuptools.find_packages(),
    url='https://github.com/MaritimeRenewable/PyResis',
    license='MIT',
    author='Yu Cao',
    author_email='tsaoyu@gmail.com',
    description='Python ship Resistance estimation package',
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    install_requires=tuple(
        filter(
            lambda r: not r.startswith("#"), (r.replace("\n", "") for r in open("requirements.txt").readlines())
        )
    )
)
