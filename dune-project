(lang dune 2.7)

(name wode)

(generate_opam_files true)

(source
 (github hasnep/wode))

(license GPL3)

(authors "Alice Smith")

(maintainers "alice@example.com")

(package
 (name wode)
 (synopsis "A library for useful number functions")
 (description "This library provides useful number functions")
 (depends
  (alcotest :with-test)
  (pyml
   (= 20220905))))
