module PRF where


import Numeric.Natural (Natural)
import Test.QuickCheck(Arbitrary(..),arbitrarySizedNatural,shrink)

fromNatural :: Natural -> Nat      -- Transforma
fromNatural 0 = Zero
fromNatural n = Succ (fromNatural $ pred n)

instance Arbitrary Nat where
    arbitrary = fmap fromNatural arbitrarySizedNatural
    shrink Zero         = []
    shrink (Succ n)     = n : shrink n

data Nat = Zero | Succ Nat
        deriving (Eq, Show)

recNat :: a -> (Nat -> a -> a) -> Nat -> a
recNat a _ Zero     = a
recNat a h (Succ n) = h n (recNat a h n)

--Addition Functions. 2 Implementations
--
addP :: Nat -> Nat -> Nat
addP  Zero      n = n                      --Zero as module for addition
addP  (Succ m)  n = Succ (addP m n)        --Recursive performance 1+1+...

addR :: Nat -> Nat -> Nat
addR m n = recNat n (\ _ y -> Succ y) m    --Nest m successors after n

--Predecessor function. 2 implementations
--
predP :: Nat -> Nat -> Nat
predP Zero _     = Zero
predP (Succ n) _ = n

predR :: Nat -> Nat -> Nat
predR Zero _     = Zero
predR (Succ n) _ = recNat n (\ x _ -> x) Zero
--Auxiliar function to create lists
--return list of size n with m as every element
--
auxList :: Nat -> Nat -> [Nat]
auxList _ Zero      = [Zero]
auxList m (Succ n)  = m:auxList m n


--Product functios. 2 implementations
--
prodP :: Nat -> Nat -> Nat
prodP m n = foldl addR Zero (auxList m n)   --Folds over a list with addR

prodR :: Nat -> Nat -> Nat
prodR Zero _ = Zero                 --Base case for the recursion
--Nest n succesors after n (m times)
prodR (Succ m) n    = recNat n (\ _ y -> Succ y) (prodR m n)


--Power functions. 2 implementations
--
powP :: Nat -> Nat -> Nat
powP _ Zero = Succ Zero
powP x (Succ Zero) = x
powP x (Succ n)    = prodR x (powP x n)

powR :: Nat -> Nat -> Nat
powR _ Zero        = Succ Zero
powR a (Succ Zero) = a
powR x (Succ n)=recNat (powP x n) (\ _ y -> Succ y) (prodR (predP x x) (powP x n))


-- Factorial functions. 2 implementations
--
facP :: Nat -> Nat -> Nat
facP Zero _     = (Succ Zero)
facP (Succ x) _ = prodP (Succ x) (facP x x)

facR :: Nat -> Nat -> Nat
facR Zero _     = (Succ Zero)
facR (Succ x) _ = (recNat (facR x x) (\ _ y -> Succ y) (prodR x (facR x x)))


-- Identity function
--
idenP :: Nat -> Nat -> Nat
idenP x _ = x

idenR :: Nat -> Nat -> Nat
idenR x _ = recNat x (\ _ w -> w) Zero


--Signum

signumR :: Nat -> Nat -> Nat
signumR Zero _     = Zero
signumR (Succ _) _ = recNat (Succ Zero) idenP Zero


-- Signum function (No recnat yet)
signumP :: Nat -> Nat -> Nat
signumP Zero _   = Zero
signumP (Succ _) _ = Succ Zero


-- Trunc substraction
--
subsP :: Nat -> Nat -> Nat
subsP Zero _ = Zero
subsP x Zero = x
subsP (Succ x) (Succ y) = subsP x y

subsR :: Nat -> Nat -> Nat
subsR Zero _ = Zero
subsR x Zero = x
subsR x y    = recNat x (\ _ w -> predR w w) y 
