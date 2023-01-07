let () = Py.initialize ()
let wode_module = Py.import "wode"
let wode_source_module = Py.import "wode.source"
let wode_scanner_module = Py.import "wode.scanner"
let wode_parser_module = Py.import "wode.parser"
let wode_ast_to_s_expression_module = Py.import "wode.ast_to_s_expression"

(* let main = Py.Module.get_function wode_module "main" *)
let rec sum = function [] -> 0 | x :: xs -> x + sum xs

let read_whole_file filename =
  let ch = open_in filename in
  let s = really_input_string ch (in_channel_length ch) in
  close_in ch;
  s

let py_source = Py.Module.get_function wode_source_module "Source"
let py_parser_state = Py.Module.get_function wode_parser_module "ParserState"

let scan_all_tokens =
  Py.Module.get_function wode_scanner_module "scan_all_tokens"

let parse_all = Py.Module.get_function wode_parser_module "parse_all"

let convert_to_s_expression =
  Py.Module.get_function wode_ast_to_s_expression_module
    "convert_to_s_expression"

let stringify_s_expression =
  Py.Module.get_function wode_ast_to_s_expression_module
    "stringify_s_expression"

let main source_file_path =
  let source =
    py_source
      [|
        Py.String.of_string source_file_path;
        Py.String.of_string (read_whole_file source_file_path);
      |]
  in
  let tokens_and_scanner_errors = scan_all_tokens [| source |] in
  let tokens, _scanner_errors = Py.Tuple.to_tuple2 tokens_and_scanner_errors in
  let expressions_and_parsing_errors =
    parse_all [| py_parser_state [| tokens; source |] |]
  in
  let expressions_py, _parsing_errors =
    Py.Tuple.to_tuple2 expressions_and_parsing_errors
  in
  let expressions = Py.List.to_list expressions_py in
  let s_expressions =
    List.map (fun e -> convert_to_s_expression [| e |]) expressions
  in
  let s_expressions_py_strings =
    List.map (fun x -> stringify_s_expression [| x |]) s_expressions
  in
  let s_expressions_strings =
    List.map Py.String.to_string s_expressions_py_strings
  in
  let s_expressions_string = String.concat "\n" s_expressions_strings in
  print_endline s_expressions_string
