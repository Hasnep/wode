(* let cp file = print_endline (Printf.sprintf "Revolt! %s" file) *)

let wode_main source_file_path = ignore (Wode.main source_file_path)
let argument_file = Cmdliner.Arg.(value & pos 0 file "" & info [])

let cmd =
  let cmd_info = Cmdliner.Cmd.info "This is the info" in
  Cmdliner.Cmd.v cmd_info Cmdliner.Term.(app (const wode_main) argument_file)

let cli () = exit (Cmdliner.Cmd.eval cmd)
