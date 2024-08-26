from setuptools import setup, find_packages

# File for older version of python that can't read setup.cfg.

setup(
    name="starrail",
    version="1.0.1",
    author="Kevin L.",
    author_email="kevinliu@vt.edu",
    description="Honkai: Star Rail Command Line Tool (CLI)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ReZeroE/StarRail",
    project_urls={
        "Bug Tracker": "https://github.com/ReZeroE/StarRail/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=open("requirements.txt").read().splitlines(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "starrail = starrail.entrypoints.entrypoints:start_starrail",
        ],
    },
)
