"""Compatibility shim — rendering lives in ``grumo.ui.rendering`` and
sitemap/robots generation in ``grumo.core.sitemap``."""

from grumo.core.sitemap import _generate_robots_txt, _generate_sitemap_xml
from grumo.ui.rendering import render_page

__all__ = ["render_page", "_generate_sitemap_xml", "_generate_robots_txt"]
