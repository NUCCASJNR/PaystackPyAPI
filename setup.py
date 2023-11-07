from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name="PaystackApiClient",
    version="0.1.1",
    packages=find_packages(),
    install_requires=install_requires,
    author="Al-Areef",
    author_email="alareefadegbite@gmail.com",
    description="Python package for Paystack API integration",
    url="https://github.com/NUCCASJNR/paystackpy",
    keywords=["Paystack", "payment", "API"],
)
