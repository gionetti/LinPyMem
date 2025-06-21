from setuptools import setup, find_packages

setup(
    name="linpymem",
    version="0.1.0",
    author="gionetti",
    author_email="its.only.a.matter.of.time.000@gmail.com",
    description="Low-level physical memory access via Linpmem kernel driver",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gionetti/linpymem",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware",
    ],
    python_requires='>=3.7',
    include_package_data=True,
)
