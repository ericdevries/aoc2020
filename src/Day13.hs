module Day13 (day13) where

import Data.List
import Data.List.Split
import Data.Sort
import Data.Maybe
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

parseSchedules :: String -> [Int]
parseSchedules input = map read (filter (\x -> not (x == "x")) (splitOn "," input))

getDelays :: [Int] -> Int -> [Int]
getDelays input ts = map (\x -> x - (ts `mod` x)) input

parseSchedules2 :: String -> [(Int, Int)]
parseSchedules2 input = map (\(x, i) -> (read x, i)) (filter (\(x,i) -> not (x == "x")) (zip (splitOn "," input) [0..]))

calculateTS :: Int -> Int -> (Int, Int) -> (Int, Int)
calculateTS pos offset a@(x, i) 
    | (pos + i) `mod` x == 0 = (pos, offset * x)
    | otherwise = calculateTS (pos + offset) offset a

-- note: all numbers are assumed to be prime numbers based on observations
-- find a position where the first item in the list matches the conditions
-- start looking at pos, and increase by offset every next check
-- the idea is that on every position, the offset is the product of previous values
-- eg, 7,19,3 -> if you want to find the ones where 3 matches, 
-- the pos is currently at a position where both 7 and 19 match their condition
-- so the first other place where this is true is going to be 7*19 steps ahead
-- after finding the position where 7, 19 and 3 are in the right position, 
-- the next number can be found by adding (7*19*3) to the offset until you find 
-- the next match. 
-- Returns a pair of (position, multiple), where position is the final answer
findTS' :: [(Int, Int)] -> Int -> Int -> (Int, Int)
findTS' [] pos offset = (pos, offset)
findTS' input pos offset = 
    let (npos, noff) = calculateTS pos offset (head input)
    in findTS' (tail input) npos noff 

findTS :: [(Int, Int)] -> (Int, Int)
findTS input = findTS' input 0 1

day13 = do 
    contents <- readFile "data/day13.txt"
    let items = (filter validLines (splitOn "\n" contents))
    putStrLn ("Lines: " ++ (show items))
    let ts = read (head items) :: Int
    let ss = head (tail items)

    putStrLn ("Items: " ++ (show ts))
    putStrLn ("Items: " ++ (show ss))
    
    let schedules = parseSchedules ss
    let ps = getDelays schedules ts
    putStrLn ("PS: " ++ (show ps))
    
    let data1 = sortOn (\x -> snd x) (zip schedules ps)
    putStrLn ("Answer: " ++ (show data1))
    
    let a1 = data1 !! 0
    let answer1 = (fst a1) * (snd a1)
    putStrLn ("Answer: " ++ (show answer1))

    let d2 = parseSchedules2 ss
    putStrLn ("D2: " ++ (show d2))

    let tsx1 = calculateTS 0 1 (7, 0)
    putStrLn ("D2tmp: " ++ (show tsx1))
    let tsx2 = calculateTS (fst tsx1) (snd tsx1) (13, 1)
    putStrLn ("D2tmp: " ++ (show tsx2))
    let tsx3 = calculateTS (fst tsx2) (snd tsx2) (59, 4)
    putStrLn ("D2tmp: " ++ (show tsx3))
    let tsx4 = calculateTS (fst tsx3) (snd tsx3) (31, 6)
    putStrLn ("D2tmp: " ++ (show tsx4))
    let tsx5 = calculateTS (fst tsx4) (snd tsx4) (19, 7)
    putStrLn ("D2tmp: " ++ (show tsx5))
    -- this should print (1068781, something)
    
    -- now in loop form
    let ts1 = findTS d2
    putStrLn ("D2: " ++ (show ts1))

