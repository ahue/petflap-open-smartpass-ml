from setuptools import setup, find_packages

setup(
    name='pfo_smartpass',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        "pandas",
        "scikit-learn",
        "numpy",
        "aioredis"
    ],
    entry_points='''
        [console_scripts]
        smartpass=pfo_smartpass.main:cli
    ''',
)

# %%

# %%
