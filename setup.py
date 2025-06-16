from setuptools import setup, find_packages

setup(
    name="python-scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            # scripts
            "tracker=scripts.tracker:main",
            "attention=scripts.attention:main",
            "interval_beeper=scripts.interval_beeper:main",
            "little_star=scripts.little_star:main",
            "pomodoro_timer=scripts.pomodoro_timer:main",
            "stuff_done=scripts.stuff_done:main",
            # tools
            "copy_paste=tools.copy_paste.cli:main",
            "dev_blog_index=tools.dev_blog_index.cli:main",
            "dev_blog_post=tools.dev_blog_post.cli:main",
            "dir_tree=tools.dir_tree.cli:main",
            "folder_indexer=tools.folder_indexer.cli:main",
            "form_fill=tools.form_fill.cli:main",
            "script_info=tools.script_info.cli:main",
        ],
    },
    python_requires=">=3.7",
)
