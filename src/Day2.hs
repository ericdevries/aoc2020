module Day2 (day2) where

import Lib
import Data.List
import Text.Regex.TDFA

parse :: String -> (String, String, String, [String])
parse x = x =~"([0-9]+)-([0-9]+) ([a-z]): (.+)" :: (String, String, String, [String])

between :: Int -> Int -> Int -> Bool
between x y z
    | x <= y = y <= z
    | otherwise = False

processLine :: (String, String, String, [String]) -> (Int, Int, Char, String)
processLine (_,_,_,m) = (
    read (m !! 0) :: Int,
    read (m !! 1) :: Int,
    head (m !! 2),
    m !! 3)

checkLine :: (Int, Int, Char, String) -> Bool
checkLine (min, max, match, s) = between min (length [z | z <- s, z == match]) max

parseLines :: [String] -> [(Int, Int, Char, String)]
parseLines = (filter checkLine) . (map processLine) . (map parse)

checkLinePosition :: (Int, Int, Char, String) -> Bool
checkLinePosition (pos1, pos2, match, s) = ((s !! (pos1-1)) == match) `xor'''` ((s !! (pos2-1)) == match)

parseLines2 :: [String] -> [(Int, Int, Char, String)]
parseLines2 = (filter checkLinePosition) . (map processLine) . (map parse)

xor''' :: Bool -> Bool -> Bool
xor''' a b = (a || b) && not (a && b)

day2 = do 
    contents <- readFile "data/day2.txt"
    putStrLn ("Data: " ++ (show (lines contents)))
    putStrLn ("Result: " ++ (show (parseLines (lines contents))))
    putStrLn ("Result count: " ++ (show (length (parseLines (lines contents)))))
    
    putStrLn ("Result: " ++ (show (parseLines2 (lines contents))))
    putStrLn ("Result count: " ++ (show (length (parseLines2 (lines contents)))))

