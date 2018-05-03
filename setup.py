from setuptools import setup, find_packages


setup(
    name="cost_per_view",
    version="0.0.1",
    description="",
    author="Kris Neuharth",
    author_email="kris.neuharth@gmail.com",
    license="Other/Proprietary",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Bottle",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5"
    ],
)
