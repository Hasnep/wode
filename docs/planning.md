# Planning

> All the Wode syntax in this is just temporary, I'll think more carefully about the syntax once I've implemented enough of the language to try using it.

- The Wode transpiler will be written in OCaml.
  - OCaml's "killer app" could be implementing language tooling, so I think it's a good choice for the Wode transpiler.
  - The initial scanner and parser are currently written in Python, but it's a very functional style of Python, so it shouldn't be too hard to translate it to OCaml.
  - I have a pretty robust test-suite for the existing code, so I can make sure I replicate the behaviour in OCaml.
  - It's pretty easy to call Python from OCaml, so I can swap out the Python implementation piece by piece until it's all rewritten.
- Wode will be transpiled to Go.
  - Go was designed by Google to avoid the problems they saw with C++, but some of the ways it solves those problems limit the expressiveness of the language.
  - Go doesn't seem to have any way to plug into its compiler (_e.g._, there's no way to give it a Go AST to compile, so it needs to be given raw Go syntax).
  - Transpiling to Go should allow easy interop with existing Go code, at the very least calling Go functions in some way, and maybe automatically creating bindings for Go libraries.
  - In theory Wode libraries could be transpiled and imported in Go programs, but they wouldn't be very useable because of all the hacky ways Wode's features will be implemented on top of Go.
- The transpiled code will not be idiomatic Go or even very readable.
  - Because Go doesn't have a lot of the features I want in Wode, they will have to be implemented in hacky ways.
  - For example, trying to create something like an algebraic type in Go makes an un-maintanable mess (more than writing Go normally does), but as long as the transpiler produces code that does the right thing, we don't need to worry about the actual Go code.
- Wode is not intended to be very fast.
  - Because it's going to produce un-idiomatic Go, it likely won't be very fast.
  - It'll still be AOT compiled, so I'm hoping for at least Python-speeds, so it should be acceptable for simple use-cases like CLI tools.
  - I'm planning to benchmark some simple examples and compare them against handwritten Go, OCaml and Python to see where Wode sits.
    That'll also let me see if there's a sudden performance regression in the output of the Wode transpiler.
- Wode will be expression based.
  - This means everything must return something, and things that are normally statements like `print` will return a null/unit value `()`.
- Wode will be statically typed.
  - Types make me happy :)
- Pattern matching
  - Pretty standard for a functional ML-style language, and will be necessary to efficiently use the type system.
- Variables will be immutable by default.
  - Again, pretty standard functional principle.
  - I'm not sure how to handle mutation in terms of syntax or semantics, I'll probably start by making mutation impossible and add it later if I feel it's needed.
- Generic types
  - Recent versions of Go now have generics, but I haven't tried them yet.
- Algebraic types (i.e., tuples and unions and the ability to mix them arbitrarily)
  - Works really well with pattern matching in OCaml
- Pipes.
  - Pipes are nice when the stdlib puts the most likely thing to be piped as the first argument to functions.
  - It's equivalent to the dot-notation for methods in object-oriented languages (_e.g._, instead of `"123".parse_int()` I prefer `parse_int("123")` or `"123" |> parse_int()`).
- Possible features that I'm considering:

  - Multiple dispatch

    - Julia does this by looking at the types of the arguments of a function call and JIT compiling the right method.
    - For Wode, this could be done at transpile time.
      That would let you define two methods for a function like this:

    ```wode
    let f = (x: Int) -> 2 * x
    let f = (x: Float) -> x/2
    f(1) == 2
    f(2.0) == 1.0
    ```

    where each of those methods of the function `f` would be transpiled to separate Go functions.
    But if you had an ambiguous situation, e.g. a union type like this:

    ```wode
    let x: Union[Int, Float] = 1
    let y: Union[Int, Float] = 2.0
    ```

    it's not possible for the transpiler to know which method of `f` to use, so `f(x)` would be syntactic sugar for:

    ```wode
    match x {
      Int(x) => f(x)
      Float(x) => f(x)
    }
    ```

    which isn't the worst to be fair.

  - Interfaces
    - Not sure how this would interact with multiple dispatch, is it even needed with multiple dispatch?
    - Rust seems to do well with interfaces, and there are Julia packages with macros that add interfaces, so it's not entirely redundant if you have multiple dispatch.
    - If I don't add interfaces, I think I'll have to implement some sort of abstract base class system like Julia uses, which is pushing me towards just adding interfaces.
    - Not sure how well these would transpile to Go, I think I would just check all the interfaces are satisfied at transpile time and then ignore them in the Go code?
