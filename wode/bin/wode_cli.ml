(* let cp file = print_endline (Printf.sprintf "Revolt! %s" file) *)

let wode_main file = ignore (Wode.main [| Py.String.of_string file |])
let argument_file = Cmdliner.Arg.(value & pos 0 file "" & info [])

let cmd =
  let cmd_info = Cmdliner.Cmd.info "This is the info" in
  Cmdliner.Cmd.v cmd_info Cmdliner.Term.(app (const wode_main) argument_file)

let cli () = exit (Cmdliner.Cmd.eval cmd)
