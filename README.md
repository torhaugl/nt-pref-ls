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
Ideally, install it with `pipx` so that the command is always available, even
from virtual environments.

## Neovim setup

As of Neovim 0.11, language servers can be configured by making a file
`.config/nvim/lsp/nt_pref_ls.lua` with this snippet inside:
```lua
return {
  cmd = { 'nt-pref-ls' },
  filetypes = { 'nt' },
}
```
In addition, you can enable your Neovim to start the LSP whenerver it enters a
`.nt` file with this snippet in your `init.lua` or equivalent:
```lua
-- neovim does not recognize .nt files, add it here
vim.filetype.add { extension = { nt = 'nt' } }

vim.lsp.enable { 'nt_pref_ls' }
```

The hover functionality is accessed with 'K' in Normal mode by default. In
addition, it is useful to add keybinds to enable hints or virtual lines:
```lua
-- Toggle virtual hints and lines
vim.keymap.set('n', '<leader>th', function()
  vim.lsp.inlay_hint.enable(not vim.lsp.inlay_hint.is_enabled { bufnr = 0 })
end, { desc = '[T]oggle Inlay [H]ints' })

vim.keymap.set('n', '<leader>tv', function()
  local current = vim.diagnostic.config().virtual_lines
  vim.diagnostic.config { virtual_lines = not current }
end, { desc = '[T]oggle [V]irtual Lines' })

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
