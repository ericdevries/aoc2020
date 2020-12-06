module Day6 (day6) where

import Data.List.Split
import Data.Sort

import Text.Regex.TDFA

validCharacters :: String -> String
validCharacters = filter (\x -> x `elem` ['a'..'z'])

deduplicate :: String -> String
deduplicate s = filter (\x -> x `elem` s) ['a'..'z']

isInAllItems :: [String] -> Char -> Bool
isInAllItems xs c = not (False `elem`  (map (\x -> c `elem` x) xs))

allMatches :: [String] -> String
allMatches xs = filter (\x -> isInAllItems xs x) ['a'..'z']

isValidString :: String -> Bool
isValidString [] = False
isValidString xs = True

split' :: String -> [String]
split' s = filter isValidString (splitOn "\n" s)


day6 = do 
    contents <- readFile "data/day6.txt"
    let items = splitOn "\n\n" contents 

    let filtered = map validCharacters items
    putStrLn ("Filtered: " ++ (show filtered))

    let unique = map deduplicate filtered
    putStrLn ("Unique: " ++ (show unique))

    let sizes = map length unique

    putStrLn ("Answer1: " ++ (show (sum sizes)))
    
    let records = map split' items
    putStrLn ("Records: " ++ (show records))

    let andMatches = map allMatches records
    putStrLn ("Records: " ++ (show andMatches))

    let sizes2 = map length andMatches
    putStrLn ("Sizes2: " ++ (show sizes2))

    let answer2 = sum sizes2
    putStrLn ("Answer2: " ++ (show answer2))
