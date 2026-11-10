# Configuration file for the Sphinx documentation builder.
#
# Created with sphinx-quickstart and then extended with the three extensions.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

project = "grid-analysis"
copyright = "2026, Workshop"
author = "Workshop"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]

# Generates one page per module from the autosummary directive in index.rst.
autosummary_generate = True

# The real powerfactory module only exists with a licence.
# During the build an empty placeholder replaces it.
autodoc_mock_imports = ["powerfactory"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "specs"]

html_theme = "alabaster"
