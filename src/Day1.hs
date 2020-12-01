module Day1 (day1) where

import Lib
import Data.List

readInt :: String -> Int
readInt = read

convert :: String -> [Int]
convert s = map readInt (lines s)

matchesLength :: Int -> [Int] -> Bool
matchesLength depth xs = length xs == depth

calculate2 :: [Int] -> [[Int]]
calculate2 xs = [[x,y] | x <- xs, y <- xs]

calculate3 :: [Int] -> [[Int]]
calculate3 xs = [[x,y, z] | x <- xs, y <- xs, z <- xs]

is2020 :: [Int] -> Bool
is2020 xs = sum xs == 2020

calculateResult :: [Int] -> Int
calculateResult xs = product xs

findResults :: [[Int]] -> [([Int], Int)]
findResults xs = map (\x -> (x, calculateResult x)) (filter is2020 xs)


day1 = do 
    contents <- readFile "data/day1.txt"
    putStrLn ("Data: " ++ (show (lines contents)))
    -- let result1 = day1Math(lines contents)
    -- putStrLn ("answer: " ++ (show result1))
    let result2 = findResults (calculate2 (convert contents))
    putStrLn ("answer 1: " ++ (show result2))
    let result3 = findResults (calculate3 (convert contents))
    putStrLn ("answer 2: " ++ (show result3))

-- :: String -> Integer
-- day1 let list = []
-- day1 "" = 0
--

