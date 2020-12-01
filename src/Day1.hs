module Day1 (day1) where

import Lib


readInt :: String -> Int
readInt = read

add :: Int -> Int -> Int
add a b = a + b

isgood :: Int -> Int -> (Int, Int, Int)
isgood a b
    | a + b == 2020 = (a, b, a * b)
    | otherwise = (a, b, fromInteger(-1))

findSum :: [Int] -> Int -> [(Int, Int, Int)]
findSum xs y = filter (\(a, b, x) -> x > 0) (map(\x -> isgood x y) xs)

findSums :: [Int] -> [(Int, Int, Int)]
findSums xs = concat (map(\x -> findSum xs x) xs)

day1Math :: [String] -> [(Int, Int, Int)]
day1Math n = findSums(map readInt n) 

day1 = do 
    contents <- readFile "data/day1.txt"
    putStrLn ("Data: " ++ (show (lines contents)))
    let result = day1Math(lines contents)
    putStrLn ("answer: " ++ (show result))


-- :: String -> Integer
-- day1 let list = []
-- day1 "" = 0
--

