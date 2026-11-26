"""Grumo — public compatibility namespace for the programmable runtime.

During the coordinated distribution migration, implementations remain in
`voodoo`. Importing from Grumo exposes the same public classes and decorators,
without creating a second runtime or silently migrating existing projects.
Advanced modules continue to live under `voodoo.*` until their individual
compatibility contracts have been implemented.
"""

from voodoo import Agent, App, Model, page, state, task, tool

__version__ = "3.2.2"

__all__ = ["Agent", "App", "Model", "page", "state", "task", "tool"]
