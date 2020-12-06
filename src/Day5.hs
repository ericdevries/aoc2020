module Day5 (day5) where

import Data.List.Split
import Data.Sort

import Text.Regex.TDFA

-- converts B F R and L characters into 1's and 0's
convert :: String -> [Int]
convert [] = []
convert (x:xs) 
    | x == 'B' = (1:convert xs)
    | x == 'F' = (0:convert xs)
    | x == 'R' = (1:convert xs)
    | x == 'L' = (0:convert xs)

-- convert array of 0's and 1's into an int
bin2dec :: [Int] -> Int
bin2dec [] = 0
bin2dec (x:xs) = x + (2 * bin2dec xs)

processSeats :: String -> (Int,Int)
processSeats s = 
    let (r,c) = splitAt 7 s
        row = bin2dec (reverse (convert r)) -- reverse, because little/big endian
        col = bin2dec (reverse (convert c))
    in (row,col)

getSeatId :: (Int,Int) -> Int
getSeatId (a,b) = a*8 + b

maximum' :: Ord a => [a] -> a
maximum' = foldr1 (\x y ->if x >= y then x else y)

-- part 2, only return seats not present in list, but x+1 and x-1 exist
validSeat :: [Int] -> Int -> Bool
validSeat xs x = not (x `elem` xs) && (x-1) `elem` xs && (x+1) `elem` xs


day5 = do 
    contents <- readFile "data/day5.txt"
    let items = (lines contents)
    -- putStrLn ("Input: " ++ (show items))
    
    let test = map processSeats items
    -- putStrLn ("Input: " ++ (show test))

    let seatids = map getSeatId test
    let maxSeatId = maximum' seatids
    -- putStrLn ("Input: " ++ (show seatids))
    putStrLn ("Answer1: " ++ (show (maximum' seatids)))

    let allSeats = [0..maxSeatId]
    let validSeats = sort (filter (\x -> validSeat seatids x) allSeats)
    putStrLn ("Answer2: " ++ (show validSeats))
