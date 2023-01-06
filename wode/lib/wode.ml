let rec range a b = if a > b then [] else a :: range (a + 1) b
