module Day9 (day9) where

import Data.List.Split
import Data.Sort
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

preamble = 25

makeList :: [Int] -> Int -> [Int]
makeList input index = 
    let p = splitAt (index - 1) input
        v = input !! index
        o = fst p
        l = drop (length o - 5) o
    in [a+b | a <- l, b <- l, not (a == b)]
    
validNumbers :: [Int] -> [Int]
validNumbers input = input

isValidNumber :: Int -> [Int] -> Bool
isValidNumber x xs = x `elem` [a+b | a <- xs, b <- xs, not (a == b)]

createSeries :: [Int] -> [([Int], [Int])]
createSeries xs = map (\(x, y) -> splitAt x xs) (zip [0..] xs)

filterSeries :: ([Int], [Int]) -> Bool
filterSeries (a, b)
    | null b = False
    | null a = False
    | (length a) < preamble = False
    | otherwise = True

formatSeries :: [([Int], [Int])] -> [([Int], Int)]
formatSeries input = map (\(x, y) -> (drop ((length x) - preamble) x, head y)) input

filterTask1 :: [([Int], Int)] -> [([Int], Int)] 
filterTask1 input = filter (\(xs, x) -> not (isValidNumber x xs)) input

-- generate records from [Int] up until it matches or exceeds match
generateSeq :: [Int] -> [Int] -> Int -> [Int]
generateSeq _ [] _ = []
generateSeq input output match
    | total == match = input
    | total > match = []
    | otherwise = generateSeq ((head output):input) (tail output) match
    where total = sum input

filterTask2 :: [Int] -> Int -> [Int]
filterTask2 input match = 
    let i = [0..(length input)]
        seq = map (\x -> generateSeq [] (drop x input) match) i
        res = filter (\x -> not (null x)) seq
    in head res
   
day9 = do 
    contents <- readFile "data/day9.txt"
    putStrLn ("Items: " ++ (show contents))
    let items = map (\x -> (read x) :: Int) (filter validLines (splitOn "\n" contents))
    putStrLn ("Items: " ++ (show items))
    
    let check = createSeries items
    -- putStrLn ("Items: " ++ (show check))
    let checkFiltered = filter filterSeries check
    -- putStrLn ("Items: " ++ (show checkFiltered))

    let formatted = formatSeries checkFiltered
    -- putStrLn ("Items: " ++ (show formatted))
    let task1 = filterTask1 formatted
    -- putStrLn ("Items: " ++ (show (head task1)))
    let answer1 = snd (head task1)
    putStrLn ("Answer1: " ++ (show answer1))
    let answer2 = filterTask2 items answer1
    putStrLn ("Answer2: " ++ (show answer2))
    let answer2_a = (minimum answer2) + (maximum answer2)
    putStrLn ("Answer2: " ++ (show answer2_a))
