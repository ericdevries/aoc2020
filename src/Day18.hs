module Day18 (day18) where

import Data.List
import Data.List.Split
import Data.Sort
import Data.Maybe
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

stripSpaces :: String -> String
stripSpaces s = filter (not . (== ' ')) s

data Expr = Operation Char Int Int (Maybe Expr)
    deriving (Show)
 

readToken :: String -> String
readToken "" = ""
readToken s
    | h `elem` ['0'..'9'] = (h:readToken (tail s))
    | otherwise = ""
    where h = head s

parse :: String -> Expr
parse s = Operation '+' 5 3 Nothing

day18 = do 
    contents <- readFile "data/day18.txt"
    let items = map (stripSpaces) (filter validLines (splitOn "\n" contents))
    putStrLn ("Lines: " ++ (show items))


    let token = readToken (items !! 0)
    putStrLn ("Token: " ++ (show token))
   
