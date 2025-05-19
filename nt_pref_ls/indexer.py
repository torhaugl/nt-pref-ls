"""
Light-weight index builder for one in-memory N-Triples document.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Set

from rdflib import Graph, URIRef
from rdflib.namespace import SKOS
import re

@dataclass
class DocumentIndex:
    labels: Dict[URIRef, str] = field(default_factory=dict) # uri → skos:prefLabel
    uris:   Set[URIRef]       = field(default_factory=set)  # every uri seen
    ranges: Dict[int, List[Tuple[int, int, URIRef]]] = field(default_factory=dict)
    #            ↑line-nr       ↑(start, end, uri)  per line
    first_pos: Dict[URIRef, Tuple[int, int]] = field(default_factory=dict) # uri → (line, start)

IRI_RE = re.compile(r"<([^>]+)>")

def build(text: str) -> DocumentIndex:
    """Parse the NT buffer once, collect labels *and* textual ranges."""
    idx   = DocumentIndex()
    graph = Graph()
    graph.parse(data=text, format="nt")

    # 1. collect prefLabels with rdflib (accurate RDF semantics)
    for s, p, o in graph:
        if p == SKOS.prefLabel and isinstance(s, URIRef) and o.datatype is None:
            idx.labels[s] = str(o)
        if isinstance(s, URIRef):
            idx.uris.add(s)
        if isinstance(o, URIRef):
            idx.uris.add(o)

    # 2. quick regex pass for character ranges (rdflib loses line numbers)
    for lineno, line in enumerate(text.splitlines()):          # 0-based to match LSP
        for m in IRI_RE.finditer(line):
            uri = URIRef(m.group(1))
            idx.ranges.setdefault(lineno, []).append((m.start(), m.end(), uri))
            idx.first_pos.setdefault(uri, (lineno, m.start()))

    return idx


# ---------------------------------------------------------------------------
# Small helper the server will call
# ---------------------------------------------------------------------------

def uri_at(idx: DocumentIndex, line: int, character: int) -> URIRef | None:
    """Return the URI that spans (line, character) – or None."""
    for start, end, uri in idx.ranges.get(line, []):
        if start <= character < end:
            return uri
    return None

