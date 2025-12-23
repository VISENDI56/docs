"""
iLuminara-Core Setup
Install governance_kernel as a local package
"""

from setuptools import setup, find_packages

setup(
    name="iluminara-core",
    version="1.0.0",
    description="Global sovereign health architecture for disease surveillance",
    author="iLuminara Health",
    author_email="engineering@iluminara.health",
    url="https://github.com/VISENDI56/iLuminara-Core",
    packages=find_packages(include=["governance_kernel", "governance_kernel.*", "edge_node", "edge_node.*"]),
    install_requires=[
        "cryptography>=41.0.7",
        "pyyaml>=6.0.1",
        "jsonschema>=4.20.0",
        "python-dateutil>=2.8.2",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "isort>=5.13.2",
            "mypy>=1.7.1",
        ],
        "cloud": [
            "google-cloud-bigquery>=3.14.1",
            "google-cloud-storage>=2.14.0",
            "google-cloud-spanner>=3.40.1",
            "google-cloud-kms>=2.19.2",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)
