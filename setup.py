from setuptools import setup
about = {}
with open("easy_html_table/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name='easy_html_table',
      version=about["__version__"],
      description=about["__summary__"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Zachary Cutlip",
      author_email="uid000@gmail.com",
      url="TBD",
      license="MIT",
      packages=['easy_html_table'],
      entry_points={
          'console_scripts': ['easy-html-table=easy_html_table.cli:main'], },
      python_requires='>=3.7',
      install_requires=[],
      package_data={'easy_html_table': ['config/*']},
      )
