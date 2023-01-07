let () = Py.initialize ()
let wode_module = Py.import "wode"
let main = Py.Module.get_function wode_module "main"
let rec sum = function [] -> 0 | x :: xs -> x + sum xs
