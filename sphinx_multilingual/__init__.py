"""A sphinx extension to enable multilingual capabilities in theme"""

import logging
import re
from apt.cache import _test

# from typing import TYPE_CHECKING

__version__ = "0.0.2"
__credits__ = 'Odoo'

SPHINX_LOGGER = logging.getLogger(__name__)

# if TYPE_CHECKING:
#     from sphinx.application import Sphinx

def _generate_alternate_urls(app, pagename, templatename, context, doctree):
    """ Add keys of required alternate URLs for the current document in the rendering context.

    Alternate URLS are required for:
      - The canonical link tag
      - The version switcher
      - The language switcher and related link tags
    """

    def _canonicalize():
        """ Add the canonical URL for the current document in the rendering context.

        The canonical version is the last released version of the documentation.
        For a given language, the canonical root of a page is in the same language so that web
        searches in that language don't redirect users to the english version of that page.

        E.g.:
        - /documentation/xxx.html -> canonical = /documentation/14.0/xxx.html
        - /documentation/1.0/fr/yyy.html -> canonical = /documentation/3.0/fr/yyy.html
        """
        # If the canonical version is not set, assume that the project has a single version
        _canonical_version = app.config.canonical_version or app.config.version
        _canonical_lang = app.config.canonical_language or "en"
        context['canonical'] = _build_url(_version=_canonical_version, _lang=_canonical_lang)

    def _versionize():
        """ Add the pairs of (version, url) for the current document in the rendering context.

        The entry 'version' is added by Sphinx in the rendering context.
        """
        context['version_display_name'] = app.config.versions_names.get(app.config.version)
        # If the list of versions is not set, assume that the project has no alternate version
        _provided_versions = app.config.versions and app.config.versions.split(',') or []
              # Map alternate versions to their display names and URLs.
        context['alternate_versions'] = []
        for _alternate_version, _display_name in app.config.versions_names.items():
            if _alternate_version in _provided_versions and _alternate_version != app.config.version:
                context['alternate_versions'].append(
                    (_display_name, _build_url(_alternate_version))
                )

    def _localize():
        """ Add the pairs of (lang, code, url) for the current document in the rendering context.

        E.g.: ('French', 'fr', 'https://.../fr_BE/...')

        The entry 'language' is added by Sphinx in the rendering context.
        """
        _current_lang = app.config.language or 'en'
        # Replace the context value by its translated description ("Français" instead of "french")
        context['language'] = app.config.supported_languages.get(_current_lang)

        # If the list of languages is not set, assume that the project has no alternate language
        _alternate_languages = app.config.languages and app.config.languages.split(',') or []
        context['alternate_languages'] = [
            (
                app.config.supported_languages.get(_alternate_lang),
                _alternate_lang.split('_')[0] if _alternate_lang != 'en' else 'x-default',
                _build_url(_lang=_alternate_lang),
            )
            for _alternate_lang in _alternate_languages
            if _alternate_lang in app.config.supported_languages and _alternate_lang != _current_lang
        ]

    def _build_url(_version=None, _lang=None):
        if app.config.is_remote_build:
            # Project root like https://www.odoo.com/documentation
            _root = app.config.project_root
        else:
            # Project root like .../documentation/_build/html/14.0/fr
            _root = re.sub(rf'(/{app.config.version})?(/{app.config.language})?$', '', app.outdir)
        # If the canonical version is not set, assume that the project has a single version
        _canonical_version = app.config.canonical_version or app.config.version
        _canonical_language = app.config.canonical_language or 'en'
        _version = _version or app.config.version
        _lang = _lang or app.config.language or 'en'
        _canonical_page = f'{pagename}.html'
        if app.config.is_remote_build:
            _canonical_page = _canonical_page.replace('index.html', '')
        return f'{_root}' \
               f'{f"/{_version}" if app.config.versions else ""}' \
               f'{f"/{_lang}" if _lang != _canonical_language else ""}' \
               f'/{_canonical_page}'

    _canonicalize()
    _versionize()
    _localize()

def setup(app: "Sphinx") -> dict:
    
    _supported_languages = {
    'de': 'Deutsch',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'nl': 'Nederlands',
    'pt_BR': 'Português (BR)',
    'uk': 'українська',
    'zh_CN': '简体中文',
    }

    _versions_names = {
    'A': "Class A",
    'C': "Class C",
    }

    app.add_config_value('project_root', None, 'env')
    app.add_config_value('canonical_version', None, 'env')
    app.add_config_value('canonical_language', None, 'env')
    app.add_config_value('versions', None, 'env')
    app.add_config_value('languages', None, 'env')
    app.add_config_value('is_remote_build', None, 'env')  # Whether the build is remotely deployed
    app.add_config_value('supported_languages', _supported_languages, 'env')
    app.add_config_value('versions_names', _versions_names, 'env')
    
    app.connect('html-page-context', _generate_alternate_urls)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
