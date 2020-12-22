module Day22 (day22) where

import Data.List
import Data.List.Split
import Data.Sort
import Data.Maybe
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

intArray :: [String] -> [Int]
intArray xs = map read xs

play :: [Int] -> [Int] -> ([Int], [Int])
play [] ys = ([], ys) 
play xs [] = (xs, [])
play xs ys = let
    x = (head xs)
    y = (head ys)
    in if x > y 
        then play ((tail xs) ++ [x, y]) (tail ys) 
        else play (tail xs) ((tail ys) ++ [y, x])

play2 :: [(String, String)] -> [Int] -> [Int] -> ([Int], [Int])
play2 _ [] ys = ([], ys) 
play2 _ xs [] = (xs, [])
play2 h xs ys = let
    x = (head xs)
    y = (head ys)
    in if x > y 
        then play ((tail xs) ++ [x, y]) (tail ys) 
        else play (tail xs) ((tail ys) ++ [y, x])


score' :: [Int] -> Int
score' input = sum (map (\(x, y) -> x * y) (zip ([1..]::[Int]) (reverse input) ))

score :: ([Int], [Int]) -> Int
score ([], ys) = score' ys
score (xs, []) = score' xs

day22 = do 
    contents <- readFile "data/day22.txt"
    let items = map (splitOn "\n") (map concat (map tail (map (splitOn ":") (splitOn "\n\n" contents))))
    let lines = map (\x -> intArray (filter validLines x)) items

    putStrLn ("Lines: " ++ (show lines))

    let result = play (lines !! 0) (lines !! 1)
    putStrLn ("Result: " ++ (show result))

    let answer1 = score result
    putStrLn ("Answer1: " ++ (show answer1))
   
