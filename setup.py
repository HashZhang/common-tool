from setuptools import setup
from setuptools import find_packages
# or
# from distutils.core import setup

setup(
        name='common-tool',     # 包名字
        version='1.0.0.dev2',   # 包版本
        description='This is a test of the setup',   # 简单描述
        author='zhxhash',  # 作者
        author_email='zhxhash@vip.sina.com',  # 作者邮箱
        url='https://https://github.com/HashZhang/common-tool',      # 包的主页
        packages=find_packages(where='.', exclude=(), include=('*',)),                 # 包，搜索所有的包含__init__.py的目录
)