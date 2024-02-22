module Main where
import PRF
import Numeric.Natural()
import Test.QuickCheck(verboseCheck)


--Instances of functions to test
--
comparator :: [Nat->Nat->Nat]
comparator = [predP,idenP,prodP,signumP,subsP]

check :: [Nat->Nat->Nat]
check      = [predR,idenR,prodR,signumR,subsR]


--Property check function
--
propCheckBi :: [Nat -> Nat -> Nat] -> [Nat -> Nat -> Nat] ->  Nat -> Nat -> Bool
propCheckBi [] [] _ _         = True --exaustive pattern match
propCheckBi [] _ _ _          = True
propCheckBi _ [] _ _          = True
propCheckBi (x:xs) (y:ys) i j = (x i j == y i j) && propCheckBi xs ys i j


--------------------------------------------------------------------------------
main :: IO ()
main = (verboseCheck $ propCheckBi comparator check)
