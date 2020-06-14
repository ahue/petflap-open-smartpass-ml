from setuptools import setup, find_packages

setup(
    name='pfo_ppredict',
    version='0.1',
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
        patpred=pfo_ppredict.main:cli
    ''',
)

# %%

# %%
