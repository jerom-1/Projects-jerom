{
module Parser where
import Lexer -- import tokens 
import Syntax -- import neccesary things


}

-- Second part of a brief contruction of a lambda calculus parser using happy.
-- Syntax and construction taken from https://www.haskell.org/happy/doc/html/ and Lab1.pdf


%name myParser -- Name of the function that will parse
%tokentype { Token } 
%error { parseError }  -- name of the error parser function


%token --  declarations of the different tokens to use.

	var             		{TokenVar $$}
	lam				{TokenLambda}
	Dot				{TokenDot}
	';'				{TokenSemiColon}
	LP				{TokenLParen}
	RP				{TokenRParen}

%%

-- Recursive definitions taken from lab requirements 

Terms :: { [Term] }
Terms :                { [] }
	  | Term ';' Terms { $1:$3 } -- first production rule to separate the list of terms in the test file.



Var :: { Term }
Var :  var { Var $1 } -- production rule to stablish the variables.

-- Constuction of terms 

Term :: { Term }
Term :   AppTerm	    {$1}
     | lam var Dot Term {Lam $2 $4} -- production rule for the lamda-abstraction

-- Construction of the application 

AppTerm :: {Term }
AppTerm	: ATerm			{$1}
	| AppTerm ATerm {App $1 $2} -- production rule for the lamda-abstraction

-- Construction of atomic term

ATerm :: {Term}
	  : LP Term RP {$2} --construction for the atomic term, that is the one closed by parenthesis.
	  | Var	       {$1}
{


parseError :: [Token] -> a
parseError x = error "Parse error!"  --error function, it is made to warn about the error when parsing.

}
