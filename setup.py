from setuptools import setup, find_packages

setup(
    name="python-scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
             "dev_blog=scripts.dev_blog_cli:main",
             "folder_index=scripts.folder_indexer_cli:main",
             "form_fill=scripts.form_fill_cli:main",
        ],
    },
    python_requires=">=3.7",
)
