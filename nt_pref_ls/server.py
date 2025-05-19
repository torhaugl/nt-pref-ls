"""
Start an LSP server over stdio
Answer `initialize`
On `textDocument/didOpen`, build an index and log the counts
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict

from pygls.server import LanguageServer
from lsprotocol import types

from .indexer import build as build_index, DocumentIndex, uri_at


LOG_LEVEL = logging.INFO
logging.basicConfig(
    format="%(levelname)s %(asctime)s [%(name)s] %(message)s",
    level=LOG_LEVEL,
)
log = logging.getLogger("nt_pref_ls")


class NtPrefLanguageServer(LanguageServer):
    """Minimal pygls‐based server fulfilling """
    def __init__(self):
        super().__init__("nt-pref-ls", "0.0.1")
        self._documents: Dict[str, DocumentIndex] = {}


ls = NtPrefLanguageServer()


# ---------------------------------------------------------------------------
# LSP handlers
# ---------------------------------------------------------------------------

@ls.feature(types.INITIALIZE)
def on_initialize(ls: NtPrefLanguageServer, params: types.InitializeParams):
    """
    Respond to the client’s `initialize` request.
    """
    log.info("initialize request from client %s", params.client_info)

    capabilities = types.ServerCapabilities(
        hover_provider=True,
    )
    server_info = types.InitializeResultServerInfoType(
        name = "nt-pref-ls",
        version = "0.0.1",
    )
    return types.InitializeResult(capabilities=capabilities, server_info=server_info)


@ls.feature(types.TEXT_DOCUMENT_DID_OPEN)
def on_did_open(ls: NtPrefLanguageServer, params: types.DidOpenTextDocumentParams):
    """
    Build document index immediately on first open.
    """
    text_doc = params.text_document
    uri      = text_doc.uri
    text     = text_doc.text

    idx = build_index(text)
    ls._documents[uri] = idx

    log.info(
        "indexed %d URIs / %d prefLabels  (%s)",
        len(idx.uris), len(idx.labels), uri
    )

# ---------------------------------------------------------------------------
#                           Hover handler (M2)
# ---------------------------------------------------------------------------

@ls.feature(types.TEXT_DOCUMENT_HOVER)
def on_hover(ls: NtPrefLanguageServer, params: types.HoverParams):
    uri  = params.text_document.uri
    idx  = ls._documents.get(uri)
    if idx is None:
        return None

    pos = params.position
    hit = uri_at(idx, pos.line, pos.character)
    if hit is None:
        return None

    label = idx.labels.get(hit)
    if not label:
        return None                # don’t show a hover if we’ve no label

    md = f"**prefLabel:** {label}\n\n`<{hit}>`"
    return types.Hover(
        contents=types.MarkupContent(kind="markdown", value=md),
        range=types.Range(
            start=types.Position(line=pos.line, character=pos.character),
            end=types.Position(line=pos.line, character=pos.character + len(str(hit)) + 2),
        ),
    )

# ---------------------------------------------------------------------------
# Entry-points
# ---------------------------------------------------------------------------

def start_io() -> None:            # defined as console-script in pyproject
    """Run the language server on stdio (Neovim’s default launch mode)."""
    ls.start_io(sys.stdin.buffer, sys.stdout.buffer)


if __name__ == "__main__":
    start_io()
