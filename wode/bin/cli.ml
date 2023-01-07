let cp () = print_endline "Revolt!"

let verbose =
  let doc = "Print file names as they are copied." in
  Cmdliner.Arg.(value & flag & info [ "v"; "verbose" ] ~doc)

let recurse =
  let doc = "Copy directories recursively." in
  Cmdliner.Arg.(value & flag & info [ "r"; "R"; "recursive" ] ~doc)

let force =
  let doc =
    "If a destination file cannot be opened, remove it and try again."
  in
  Cmdliner.Arg.(value & flag & info [ "f"; "force" ] ~doc)

let srcs =
  let doc = "Source file(s) to copy." in
  Cmdliner.Arg.(
    non_empty & pos_left ~rev:true 0 file [] & info [] ~docv:"SOURCE" ~doc)

let dest =
  let doc =
    "Destination of the copy. Must be a directory if there is more than one \
     $(i,SOURCE)."
  in
  let docv = "DEST" in
  Cmdliner.Arg.(
    required & pos ~rev:true 0 (some string) None & info [] ~docv ~doc)

let cmd =
  let cmd_info = Cmdliner.Cmd.info "cp" in
  Cmdliner.Cmd.v cmd_info Cmdliner.Term.(app (const cp) (const ()))

let main () = exit (Cmdliner.Cmd.eval cmd)
