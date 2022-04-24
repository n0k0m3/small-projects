front_matter_str = """---
layout: default
title: 123123
parent: Data Analysis
grand_parent: Projects
nav_order: 1
---"""

import subprocess


def conv_nb_jekyll(filename, front_matter):

    """
    this function will convert your jupyter notebook to html and
    prepend the front matter string you provide to the top of the resulting html file

    Args:
        filename: filename of input jupyter notebook (.ipynb file)
        front_matter: python formatted string resembling YAML jekyll front matter
    Returns:
        jekyll_html_post: location of final html file to post on your jekyll blog
    """

    # convert jupyter notebook to html
    subprocess.call(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            "--template",
            "full",
            "--no-input",
            filename,
        ]
    )

    # function that will prepend given string to given filename
    def prepend_string(filename, string):
        with open(filename, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write(string.rstrip("\r\n") + "\n" + content)

    # call function to prepend front matter to the file
    html_file = filename.replace(".ipynb", ".html")
    prepend_string(html_file, front_matter)
    print("converted html file at: ", html_file)

    return html_file


jekyll_html_post = conv_nb_jekyll(
    filename="analysis.ipynb", front_matter=front_matter_str
)
