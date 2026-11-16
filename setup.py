from setuptools import setup, find_packages

setup(
    name="python_supermarket_pos_billing",
    version="1.0.0",
    description="Python Supermarket Pos Billing - Production Grade Python Engine",
    author="Shyamkumar Pandey",
    author_email="shyampandey1104@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=["pytest>=7.0.0"]
)
