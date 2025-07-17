# Copyright (C) 2020-2025 Motphys Technology Co., Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import site
import sys
from pathlib import Path

project_root = Path(__file__).parents[2].resolve()
motrixsim_path = None

# 优先检查项目目录中的包
pkg_candidate = project_root / "motrixsim"
if (pkg_candidate / "__init__.py").exists():
    motrixsim_path = pkg_candidate
else:
    # 检查site-packages目录
    for site_path in map(Path, site.getsitepackages()):
        candidate = site_path / "motrixsim"
        if (candidate / "__init__.py").exists():
            motrixsim_path = candidate
            break

print(f"MotrixSim Package Path: {motrixsim_path}")

if not motrixsim_path:
    raise ImportError(
        "motrixsim package not found in:\n"
        f"- Project directory: {project_root}\n"
        f"- Site-packages: {site.getsitepackages()}"
    )

# 确保路径唯一性且优先加载
if str(motrixsim_path) not in sys.path:
    sys.path.insert(0, str(motrixsim_path))

__version__ = "0.1.0"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "MotrixSim"
copyright = "2025, Motphys"
author = "Motphys"
release = __version__
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Include documentation from docstrings
    "sphinx.ext.autodoc",
    # Support for NumPy and Google style docstrings
    "sphinx.ext.napoleon",
    # Generate autodoc summaries
    "sphinx.ext.autosummary",
    # Extending your autodoc API docs with a summary
    "autodocsumm",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx_subfigure",
    "sphinxcontrib.video",
    "sphinx_togglebutton",
    "sphinx_design",
]

# https://sphinx-design.readthedocs.io/en/pydata-theme/get_started.html#usage
myst_enable_extensions = ["colon_fence", "deflist"]

### Autodoc configurations ###
# put type hints inside the signature instead of the description (easier to maintain)
autodoc_typehints = "both"
# Define the order in which automodule and autoclass members are listed
autodoc_member_order = "groupwise"
# default autodoc settings
autodoc_default_options = {
    "autosummary": True,
}

autodoc_typehints_description_target = "all"
autodoc_default_flags = ["members", "show-inheritance", "undoc-members"]


# generate autosummary even if no references
autosummary_generate = True
autosummary_generate_overwrite = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = ["colon_fence", "dollarmath"]
# https://github.com/executablebooks/MyST-Parser/issues/519#issuecomment-1037239655
myst_heading_anchors = 4

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_title = "MotrixSim Documentation"
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_logo = "_static/Motphys_logo_Black.svg"
html_favicon = "_static/Motphys_Logo_only_Black_100x100px.svg"
html_show_copyright = True
html_show_sphinx = False
html_last_updated_fmt = ""  # to reveal the build date in the pages meta

html_theme_options = {
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/navigation.html
    "show_nav_level": 2,
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/source-buttons.html#add-an-edit-button
    "use_edit_page_button": False,
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/indices.html#add-indices-links
    "primary_sidebar_end": ["indices.html"],
    "logo": {
        "image_light": "_static/Motphys_logo_Black.svg",
        "image_dark": "_static/Motphys_logo_White.svg",
    },
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#configure-the-navbar-center-alignment
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],  # "version-switcher"
    "navbar_persistent": ["search-field.html"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#configure-the-navbar-center-alignment
    "navbar_align": "content",
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/page-toc.html#per-page-secondary-sidebar-content
    "secondary_sidebar_items": ["page-toc", "sidebar-ethical-ads"],
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#footer-content
    "show_prev_next": True,
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/announcements.html#version-warning-banners
    "show_version_warning_banner": False,
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#footer-content
    "footer_start": ["copyright", "sphinx-version"],
    "footer_end": ["theme-version"],
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/header-links.html#navigation-bar-external-links
    "external_links": [
        {"name": "Issues", "url": "https://github.com/Motphys/motrixsim-docs/issues"},
        {"name": "Discussions", "url": "https://github.com/Motphys/motrixsim-docs/discussions"},
    ],
    "header_links_before_dropdown": 2,
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/header-links.html#icon-links
    "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/Motphys/motrixsim-docs",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "About Motphys",
            "url": "https://www.motphys.com",
            "icon": "fa-solid fa-building",
            "type": "fontawesome",
        },
    ],
}
project_version = os.environ.get("READTHEDOCS_VERSION")
if project_version is None:
    project_version = __version__
html_context = {}
html_css_files = [
    "css/custom.css",
]
html_js_files = [
    "js/custom.js",
]
