import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

import dsf  # noqa: E402

project = "dsf-python"
author = "Duet3D Ltd."
copyright = "Duet3D Ltd."
release = dsf.__version__
version = release

extensions = ["sphinx.ext.autodoc"]

# Signatures such as `type[ObjectModel]` are otherwise matched against the many `type` properties
suppress_warnings = ["ref.python"]

autodoc_member_order = "bysource"
autodoc_default_options = {"members": True, "undoc-members": True, "show-inheritance": True}


def skip_foreign_members(app, what, name, obj, skip, options):
    # Packages re-export their classes (:imported-members:), but stdlib imports such as Enum must not be documented
    if what == "module" and not getattr(obj, "__module__", "dsf").startswith("dsf"):
        return True
    return None


def setup(app):
    app.connect("autodoc-skip-member", skip_foreign_members)
