module Day10 (day10, checkDiffs) where

import Data.List
import Data.List.Split
import Data.Sort
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

-- task 1, get a list of [1, 3, 1, etc]  
checkDiffs :: Int -> [Int] -> [Int]
checkDiffs _ [] = []
checkDiffs i xs@(c:r) = ((minimum xs) - i):(checkDiffs c r)

-- divide lists by groups, each group being 3 jolts away from the next
subLists :: [(Int, Int)] -> [[(Int, Int)]]
subLists [] = []
subLists xs = 
    let items       = (head xs):takeWhile (\(a,b) -> b == 1) (tail xs)
        len         = length items
        remainder   = drop len xs
    in items:(subLists remainder)

-- remove the relative position from the previous jolt, keep the actual values (jolts)
normalizeSublists :: [[(Int, Int)]] -> [[Int]]
normalizeSublists xs = map (\x -> map fst x) xs

-- check if it is valid; the biggest distance must be 3 between all values, including min and max
isValidSubsequence :: [Int] -> Int -> Int -> Bool
isValidSubsequence [] _ _ = False
isValidSubsequence xs min max =
    let diffs = checkDiffs min xs
    in ((maximum diffs) <= 3) && ((maximum xs + 3) >= max)

-- check how many valid subsequences we have in a sublist
checkSublist :: [Int] -> Int
checkSublist xs = length (filter (\x -> isValidSubsequence x (minimum xs - 3) (maximum xs + 3)) (subsequences xs))

-- same, but return the actual results
checkSublist' :: [Int] -> [[Int]]
checkSublist' xs = filter (\x -> isValidSubsequence x (minimum xs - 3) ((maximum xs) + 3)) (subsequences xs)

day10 = do 
    contents <- readFile "data/day10.txt"
    let lst = map (\x -> (read x) :: Int) (filter validLines (splitOn "\n" contents))
    let m = (maximum lst) + 3
    let items = sort ([m,0] ++ lst)
    putStrLn ("Items: " ++ (show items))

    -- get a list of [1, 3, ...]
    let task1 = checkDiffs 0 items
    let ones = filter (==1) task1
    let threes = filter (==3) task1
    let answer1 = (length ones) * (length threes)
    putStrLn ("Task1: " ++ (show answer1))
    
    let diffs = zip items task1 
    let subs = subLists diffs
    let normalized = normalizeSublists subs
    putStrLn("Task2: " ++ (show normalized))
    let checked = map checkSublist normalized
    putStrLn("Task2: " ++ (show checked))
    let checked' = map checkSublist' normalized
    putStrLn("Task2: " ++ (show checked'))

    putStrLn ("Answer 2: " ++ (show (product checked)))
