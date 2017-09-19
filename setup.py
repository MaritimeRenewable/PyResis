import setuptools

setuptools.setup(
    name='PyResis',
    version='1.0.1',
    packages=setuptools.find_packages(),
    package_data={'PyResis': ['cr.txt']},
    url='https://github.com/MaritimeRenewable/PyResis',
    license='MIT',
    author='Yu Cao',
    author_email='tsaoyu@gmail.com',
    description='Python ship Resistance estimation package'
)
