Py.initialize ()

let wode = Py.import "wode"
let main = Py.Module.get_function wode "main"
let result = main [| Py.String.of_string "./example.wode" |]
