# Wode

A functional language that is (or one day will be) transpiled to Go.

## Usage

The simplest way to install the Wode transpiler is using [pipx](https://pypa.github.io/pipx/installation/).

```shell
pipx install git+https://github.com/Hasnep/wode
```

Then use the `--help` argument for more information.

```shell
wode --help
```

## Inspirations

- Direct inspirations
  - [OCaml](https://ocaml.org/)
  - [ReasonML](https://reasonml.github.io/)
- Other similar projects
  - [Braid](https://github.com/joshsharp/braid)
  - [Have](https://github.com/vrok/have)
  - [Oden](https://oden-lang.github.io/)
- Resources for implementation
  - [Crafting Interpreters](https://craftinginterpreters.com) - Robert Nystrom
  - [Monkey](https://monkeylang.org/) - Thorsten Ball
  - [Simple but Powerful Pratt Parsing](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html) - Aleksey Kladov

## Comparison

This table hopefully gives some idea of where I'd like Wode to sit in relation to other existing languages.

|                   | Native runtime  | Go runtime | Node.js       | JVM          | .NET | Beam VM              |
| ----------------- | --------------- | ---------- | ------------- | ------------ | ---- | -------------------- |
|                   | C               | Go         | JavaScript    | Java, Kotlin | C#   | Erlang, Gleam        |
| Functional        | OCaml, ReasonML | _Wode_     | Rescript      | Scala        | F#   | Elixir               |
| Lisp-y            | Lisp, Scheme    |            | Clojurescript | Clojure      |      | Lisp Flavored Erlang |
| Purely functional | Haskell         |            | Purescript    |              |      |                      |
