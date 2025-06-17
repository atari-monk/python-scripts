from setuptools import setup, find_packages

setup(
    name="python-scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            # script
            "case_converter=script.case_converter:main",
            "merger=script.merger:main",
            "attention=script.attention:main",
            "interval_beeper=script.interval_beeper:main",
            "little_star=script.little_star:main",
            "pomodoro_timer=script.pomodoro_timer:main",
            "stuff_done=script.stuff_done:main",
            # tools
            "tracker=tool.tracker.cli:main",
            "copy_paste=tool.copy_paste.cli:main",
            "dev_blog_index=tool.dev_blog_index.cli:main",
            "dev_blog_post=tool.dev_blog_post.cli:main",
            "dir_tree=tool.dir_tree.cli:main",
            "folder_indexer=tool.folder_indexer.cli:main",
            "form_fill=tool.form_fill.cli:main",
            "script_info=tool.script_info.cli:main",
        ],
    },
    python_requires=">=3.7",
)
