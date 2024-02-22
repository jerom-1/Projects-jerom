{
{-# OPTIONS_GHC -Wno-missing-local-signatures #-} -- Flags
module Lexer where 
import Syntax -- imports Tokens from the Syntax.hs file
}


 	
-- first part of a brief contruction of a lambda calculus parser using alex.

-- Syntax and contruction based on https://www.haskell.org/alex/doc/html/



%wrapper "basic"
$digit = 0-9 
$alpha = [a-zA-Z] --alphabet definition



tokens :-
	
  $white+                       ;
  "--".*						;
  \.							{ \s -> TokenDot}
  \λ							{ \s -> TokenLambda }
  \(                            { \s -> TokenLParen }
  \;                            { \s -> TokenSemiColon }
  \)                            { \s -> TokenRParen }
  $alpha [$alpha $digit \_ \']* { \s -> TokenVar s }

{

myLexer = alexScanTokens -- default function definition to String -> [Token]

}



