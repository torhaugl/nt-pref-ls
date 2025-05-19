nt-pref-ls
==========

A lightweight **Language Server for N-Triples (`*.nt`) files** that replaces opaque
UUID-style IRIs with their human-friendly `skos:prefLabel`s inside Neovim.
Hovering over any IRI defined in the same file shows its label; missing labels
are flagged as diagnostics.

## Install

Install as a python package, clone it and `pip install -e .`.

## neovim

Add the following to `init.lua` in neovim to start the language server.
```lua
local client = vim.lsp.start_client {
  name = 'nt_pref_ls',
  cmd = { 'nt-pref-ls' },
}

vim.api.nvim_create_autocmd('FileType', {
  pattern = 'nt',
  callback = function()
    vim.lsp.buf_attach_client(0, client)
  end,
})

-- neovim does not recognize nt files, add it here
vim.filetype.add { extension = { nt = 'nt' } }
```
