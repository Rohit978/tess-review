from setuptools import setup

setup(
    name="tess-review",
    version="2.0.0",
    py_modules=["tess_review"],
    install_requires=[
        "openai>=1.0.0",
        "rich>=13.0.0"
    ],
    entry_points={
        "console_scripts": [
            "tess-review=tess_review:main",
            "tess=tess_review:main"
        ],
    },
)
