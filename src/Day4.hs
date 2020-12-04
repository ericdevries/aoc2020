module Day4 (day4) where

import Data.List.Split

import Text.Regex.TDFA

replace' :: (Eq a) => a -> a -> a -> a
replace' input m r 
    | input == m = r 
    | otherwise = input 

replace :: (Eq a) => [a] -> a -> a -> [a]
replace input m r = map (\x -> replace' x m r) input

isValid :: [String] -> Bool
isValid x
    | l == 2 = True
    | otherwise = False
    where l = (length x)

parse :: String -> [String]
parse x = map (\x -> x !! 0) (filter isValid (map (splitOn ":") (splitOn " " x)))

parseWithValues :: String -> [[String]]
parseWithValues x = filter isValid (map (splitOn ":") (splitOn " " x))

checkValid :: [String] -> [String] -> Bool
checkValid input required
    | x == 0 = True
    | otherwise = False
    where x = length [i | i <- required, not (i `elem` input)]

between :: Int -> Int -> Int -> Bool
between x y z
    | x <= y = y <= z
    | otherwise = False

getItemFromPair :: (a, b, c, d) -> d
getItemFromPair (_, _, _, x) =  x

getGroups :: String -> String -> [String]
getGroups input exp = getItemFromPair (input =~ exp :: (String, String, String, [String]))

validHeight :: String -> Bool
validHeight x
    | length r == 0 = False
    | (r !! 1)  == "cm" = between 150 (read (r !! 0)) 193
    | (r !! 1)  == "in" = between 59 (read (r !! 0)) 76
    where r = (getGroups x "([0-9]+)(cm|in)")

validEyeColor :: String -> Bool
validEyeColor x = x `elem` ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

validateField :: (String,String) -> Bool
validateField (k,v)
    | k == "byr" = between 1920 (read v :: Int) 2002
    | k == "iyr" = between 2010 (read v :: Int) 2020
    | k == "eyr" = between 2020 (read v :: Int) 2030
    | k == "hgt" = validHeight v
    | k == "hcl" = ((v =~ "^#([0-9a-f]+){6}$") :: Bool) && ((length v) == 7)
    | k == "ecl" = validEyeColor v
    | k == "pid" = ((v =~ "^([0-9]+){9}$" ) :: Bool) && ((length v) == 9)
    | otherwise = True

validateRecord :: [[String]] -> [Bool]
validateRecord input = map (\x -> validateField ((x !! 0), (x !! 1))) input

isValidRecord :: [Bool] -> Bool
isValidRecord x = not (False `elem` x)

day4 = do 
    contents <- readFile "data/day4.txt"
    let items = splitOn "\n\n" contents 
    let required = [
                    "byr",
                    "iyr",
                    "eyr" ,
                    "hgt",
                    "hcl",
                    "ecl",
                    "pid"
                    ]

    let proper = map (\x -> replace x '\n' ' ') items
    putStrLn ("Data: " ++ (show proper))
    
    let parsed = map parse proper
    putStrLn ("Data: " ++ (show parsed))
    
    let valid = map (\x -> checkValid x required) parsed
    putStrLn ("Answer1: " ++ (show (length (filter (\x -> x) valid))))

    let parsed2 = map parseWithValues proper
    let valid2 = filter (\x -> checkValid (map (\y -> y !! 0) x) required) parsed2
    let validated2 = map validateRecord valid2
    let filtered2 = filter isValidRecord validated2
    
    putStrLn ("Answer2: " ++ (show (length filtered2)))
