from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name="paystackpy",
    version="1.0",
    packages=find_packages(),
    install_requires=install_requires,
    author="Al-Areef",
    author_email="alareefadegbite@gmail.com",
    description="Python package for Paystack API integration",
    url="https://github.com/NUCCASJNR/paystackpy",
    keywords=["Paystack", "payment", "API"],
)