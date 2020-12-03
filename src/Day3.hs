module Day3 (day3) where

import Lib
import Data.List

checkLine :: (String, Int) -> Bool
checkLine (s, i)
    | s !! x == '#' = True
    | otherwise = False
    where x = i `mod` (length s)

getRightLine :: [String] -> Int -> [String]
getRightLine l offset = map fst (filter (\(x, i) -> i `mod` offset == 0) (zip l [0..]))

processPattern :: [String] -> (Int, Int) -> [Bool]
processPattern field (x, y) = map checkLine (zip (tail (getRightLine field y)) [x,x*2..])

processPatterns :: [String] -> [(Int, Int)] -> [[Bool]]
processPatterns field p = map (\z -> processPattern field z) p

getCounts :: [[Bool]] -> [Int]
getCounts xs = map length (map (filter (\x -> x)) xs)

day3 = do 
    contents <- readFile "data/day3.txt"
    let field = (lines contents)

    let patterns = [ (1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    let zipped = zip (tail field) [3,6..]
    putStrLn ("Data: " ++ (show (lines contents)))
    putStrLn ("Zipped: " ++ (show zipped))

    let results = map checkLine zipped
    putStrLn ("Output: " ++ (show results))
    let count = filter (\x -> x) results
    putStrLn ("Anser1: " ++ (show (length count)))

    let result2 = processPatterns (lines contents) patterns
    putStrLn ("Result2: " ++ (show (result2)))
    let count1 = getCounts result2
    putStrLn ("Answer2: " ++ (show (count1)) ++ " " ++ (show (product count1)))
    
