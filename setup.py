from setuptools import setup

with open("/home/gqx/repos/Play_2048/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python2048",  # 模块名称
    version="1.0.0b1",  # 当前版本
    author="GQX",  # 作者
    author_email="kill114514251@outlook.com",  # 作者邮箱
    description="Python 2048",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://github.com/BinaryGuo/Py2048",  # 模块github地址
    packages=["py2048",],  # 自动找到项目中导入的模块
    include_package_data=True,
    # 模块相关的元数据
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: pygame",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Environment :: GUI (Graphical User Interface)",
        #"Operating System :: OS Independent",
        "Operating System :: Linux",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10"
    ],
    # 依赖模块
    install_requires=[
        "pygame>=2.5.0",
        "pygame_menu>=4.5.0"
    ],
    python_requires=">=3.10"
)
