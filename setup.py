from setuptools import setup

# todo: finish or delete this
setup(
   name='foo',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['src'], install_requires=['scikit-learn', 'pandas', 'numpy']  #same as name
)