# coding: utf-8

import os
import sys

sourceFolder  = os.path.abspath('../../')
libFolder     = os.path.join(sourceFolder, 'Lib')
source_suffix = ['.rst']

project     = 'hTools3'
author      = 'Gustavo Ferreira'
copyright   = '2018-2020, %s' % author
version     = '0.4' # get version from lib
release     = 'alpha'
master_doc  = 'index'
smartquotes = True
nitpicky    = False

exclude_patterns         = ['.DS_Store']
todo_include_todos       = False
autoclass_content        = 'class'
add_module_names         = True
add_function_parentheses = True

html_title           = project
html_short_title     = html_title
html_theme           = ['classic', 'nature', 'sphinx_rtd_theme', 'fontPartsTheme'][0]
html_theme_options_  = {
    'classic' : {
        'collapsiblesidebar'         : True
    },
    'nature' : {},
    'sphinx_rtd_theme' : {
        # 'canonical_url'              : '',
        # 'logo_only'                  : False,
        # 'display_version'            : True,
        # 'prev_next_buttons_location' : 'bottom',
        # 'style_external_links'       : False,
        # 'vcs_pageview_mode'          : '',
        # 'collapse_navigation'        : True,
        # 'sticky_navigation'          : True,
        # 'navigation_depth'           : 4,
        # 'includehidden'              : True,
        # 'titles_only'                : False
    },
    'fontPartsTheme' : {},
}
html_theme_options   = html_theme_options_[html_theme]
html_theme_path      = ['_themes']
html_static_path     = ['_static']
html_show_sourcelink = True

pygments_style = 'sphinx'
templates_path = ['_templates']
extensions     = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

autodoc_member_order  = 'bysource'
autodoc_default_flags = [
    'members',
    'undoc-members',
    'private-members',
    'show-inheritance',
]
# new in Sphinx 1.8:
# autodoc_default_options = {
#     'members': None,
#     'member-order': 'bysource',
#     'undoc-members': None,
#     'special-members': '__init__',
# }
autodoc_mock_imports = [
    'vanilla',
    'mojo',
    # 'mojo.roboFont',
    # 'mojo.events',
    # 'mojo.UI',
    # 'mojo.tools',
    # 'mojo.drawingTools',
    'fontPens',
    'fontParts',
    # 'fontPens.penTools',
    'glyphConstruction',
    # 'lib.tools.notifications',
    # 'lib.UI.fileBrowser',
    'fontTools',
    # 'fontTools.agl',
    # 'fontTools.misc',
    # 'fontTools.misc.xmlWriter',
    # 'fontTools.misc.py23',
    # 'fontTools.misc.transform',
    # 'fontTools.misc.bezierTools',
    # 'fontTools.pens.basePen',
    # 'fontTools.ufoLib.pointPen',
    # 'fontParts.base',
    # 'fontParts.fontshell',
    # 'fontParts.world',
    'defcon',
    # 'Foundation',
    'AppKit',
    # 'objc',
    'lib',
]

sys.path.insert(0, libFolder)

def setup(app):
   app.add_stylesheet("custom.css")
