module Day15 (day15) where

import Data.List
import Data.List.Split
import Data.Sort
import Data.Maybe
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

numberSpoken :: [Int] -> Int -> Int -> [Int] -> Int
numberSpoken input turn previous history 
    | (length input) > 0 = head input 
    | (length indices > 1) = 
        let x1 = (last indices) + 1
            x2 = (last (init indices) + 1)
        in x1 - x2
    | otherwise = 0
    where indices = findIndices (==previous) (reverse history)

    

proc :: [Int] -> Int -> Int -> [Int] -> Int
proc input turn val history 
    -- end condition
    | turn == 2020 = val
    -- still have something in the initial data
    | (length input) > 0 = proc (tail input) (turn+1) (head input) ((head input):history)
    | otherwise = let num = numberSpoken [] turn val history 
                  in proc [] (turn+1) num (num:history)
        

day15 = do 
    contents <- readFile "data/day15.txt"
    let items = map (\x -> read x :: Int) (splitOn "," (head (filter validLines (splitOn "\n" contents))))
    putStrLn ("Lines: " ++ (show items))
   
    let result = proc (tail items) 1 (head items) [(head items)]
    putStrLn ("Result: " ++ (show result))
