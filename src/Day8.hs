module Day8 (day8) where

import Data.List.Split
import Data.Sort
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

parseNumber :: String -> Int
parseNumber ('-':xs) = -1 * (read xs)
parseNumber ('+':xs) =  (read xs)

parseLine :: String -> (String, Int) 
parseLine s = 
    let p = splitOn " " s
    in (p !! 0, parseNumber (p !! 1))


exec :: [(String, Int)] -> Int -> [Int] -> Int
exec lines index seen 
    | index `elem` seen = 0
    | op == "nop" = exec lines (index + 1) (index:seen)
    | op == "acc" = n + exec lines (index + 1) (index:seen)
    | op == "jmp" = exec lines (index + n) (index:seen)
    | op == "end" = 0
    where (op, n) = if index < (length lines) then lines !! index else ("end", 0)

isInfiniteLoop :: [(String, Int)] -> Int -> [Int] -> Bool
isInfiniteLoop lines index seen
    | index `elem` seen = True
    | op == "nop" = isInfiniteLoop lines (index + 1) (index:seen)
    | op == "acc" = isInfiniteLoop lines (index + 1) (index:seen)
    | op == "jmp" = isInfiniteLoop lines (index + n) (index:seen)
    | op == "end" = False
    where (op, n) = if index < (length lines) then lines !! index else ("end", 0)


swap :: (String, Int) -> (String, Int) 
swap (op, n) 
    | op == "jmp" = ("nop", n)
    | op == "nop" = ("jmp", n)
    | otherwise = (op, n)


swapInstructionOn :: [(String, Int)] -> Int -> [(String, Int)]
swapInstructionOn lines index = map (\(x, l) -> if l == index then (swap x) else x) (zip lines [0..])
   

swapInstructions :: [(String, Int)] -> [[(String, Int)]]
swapInstructions lines = filter (\x -> not (isInfiniteLoop x 0 [])) (map (swapInstructionOn lines) [0..(length lines)])


day8 = do 
    contents <- readFile "data/day8.txt"
    let items = filter validLines (splitOn "\n" contents )
    putStrLn ("Items: " ++ (show items))
    let parsed = map parseLine items
    putStrLn ("Parsed: " ++ (show parsed))

    let result = exec parsed 0 []
    putStrLn ("Result: " ++ (show result))

    let isInfinite = isInfiniteLoop parsed 0 []
    putStrLn ("Result: " ++ (show isInfinite))

    let swapped = swapInstructions parsed 
    putStrLn ("Result: " ++ (show swapped))
    let res = map (\x -> exec x 0 []) swapped
    putStrLn ("Result2: " ++ (show res))
