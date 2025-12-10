"""
Human Layer Ingestion Package
Parsers for importing data from external sources into the human layer.
"""

from .linkedin import LinkedInParser

__all__ = ["LinkedInParser"]
