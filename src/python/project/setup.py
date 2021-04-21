from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# long_description = (here / 'README.md').read_text(encoding='utf-8')

if __name__ == '__main__':
    setup(
        name="Project",
        version="1.0.0",
        description="Pipeline",
        # long_description=long_description,
        # long_description_content_type='text/markdown',
        # url='https://github.com/pypa/sampleproject',
        author="xxxxxxx",
        author_email="xxxxxxx",
        license="xxxxxxx",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: , Analysts, Data Engineers",
            "Topic :: ETL, xxxxxxx xxxxxxx, Pipeline",
            "License :: xxxxxxx",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7.5",
        ],
        keywords="databricks, notebook, testing, pipeline, etl",
        # package_dir={'': ''},
        # py_modules=[""],
        # packages=find_packages('project_pipeline'),
        packages=[
            "project_pipeline.helpers"
        ],
        python_requires=">=3.6, <4",
        # install_requires=['sendgrid', 'databricks_api', 'junit_xml'],
        # extras_require={
        #     'dev': ['check-manifest'],
        #     'test': ['coverage'],
        # },
        # package_data={
        #     'scrapy.cfg': [''],
        # },
        # data_files=[''],
        #     'console_scripts': [
        #         'sample=sample:main',
        #     ],
        # },
        # project_urls={
        #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        #     'Source': 'https://github.com/pypa/sampleproject/'
        # },
        zip_safe=False,
    )
