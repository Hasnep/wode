# Development

Create a switch

```shell
opam switch create ocaml-base-compiler
```

Activate the switch

```shell
eval (opam env --switch=ocaml-base-compiler)
```

Install development dependencies

```shell
opam install --yes \
  ocaml-lsp-server \
  ocamlformat \
  ounit2
```

Install build dependencies

```shell
opam install --yes pyml
```
