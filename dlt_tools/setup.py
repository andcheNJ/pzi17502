from setuptools import setup, find_packages

setup(
    name="DLT-Tools",
    version="0.8",
    packages=find_packages(),
    install_requires=["scapy","pyinstaller"],
    author="Friedrich Zimmer",
    author_email="friedrich.zimmer@arrk-engineering.com",
    description="Reading and writing of DLT Data to Files and Stream",
    url="http://sntee.pzs.de:8080/cb/git/ens_stresstest",
    license="Proprietary"
)
