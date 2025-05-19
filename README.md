nt-pref-ls
==========

A lightweight **Language Server for N-Triples (`*.nt`) files** that replaces
opaque UUID-style IRIs with their human-friendly `skos:prefLabel`s inside
Neovim. Hovering over any IRI defined in the same file shows its label; missing
labels are flagged as diagnostics. This language server also supports inlay
hints.

## Install

Install as a python package, e.g.,
```sh
pip install git+https://github.com/torhaugl/nt-pref-ls.git
```

## Neovim setup

Add this snippet to `init.lua` or equivalent:
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

-- add a key to toggle inlay hints
vim.keymap.set('n', '<leader>th', function()
  vim.lsp.inlay_hint.enable(not vim.lsp.inlay_hint.is_enabled { bufnr = 0 })
end, { desc = '[T]oggle Inlay [H]ints' })
```

## Example

Hover tooltips and inline inlay‑hints for two labelled UUID IRIs; the
unlabelled one is underlined as a Hint diagnostic.

![Hover and diagnostics](/figs/example.png)

Inlay hints show up next to the IRI with the prefLabel.
![Inlay hints](/figs/example2.png)

## AI Attribution

Large parts of this code is automatically generated with an LLM (ChatGPT-o3)
and then refined by hand.
