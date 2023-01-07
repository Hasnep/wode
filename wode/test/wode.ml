open OUnit2

let tests =
  "Test suite for wode"
  >::: [
         ("empty" >:: fun _ -> assert_equal (Wode.sum []) 1);
         ("singleton" >:: fun _ -> assert_equal (Wode.sum [ 1 ]) 1);
         ("two_elements" >:: fun _ -> assert_equal (Wode.sum [ 1; 2 ]) 3);
       ]

let _ = run_test_tt_main tests
