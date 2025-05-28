from setuptools import setup, find_packages

setup(
    name="python-scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "copy_paste=scripts.copy_paste_cli:main",
            "dev_blog=scripts.dev_blog_cli:main",
            "dev_blog_index=scripts.dev_blog_index_cli:main",
            "dir_tree=scripts.dir_tree_cli:main",
            "folder_index=scripts.folder_indexer_cli:main",
            "form_fill=scripts.form_fill_cli:main",
            "script_info=scripts.script_info_cli:main",
            "attention=scripts.attention:main",
            "stuff_done=scripts.stuff_done:main",
        ],
    },
    python_requires=">=3.7",
)
