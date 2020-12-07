module Day7 (day7) where

import Data.List.Split
import Data.Sort
import Text.Regex.TDFA

bagRe = "([0-9]+) ([a-z]+ [a-z]+) .*"

data Bag = Bag String Int
    deriving Show

data Record = Record String [Bag]
    deriving Show


parseBag :: String -> Bag 
parseBag s =
    let (_, _, _, m) = (s =~ "([0-9]+) ([a-z]+ [a-z]+) .*") :: (String, String, String, [String])
    in Bag (m !! 1) (read (m !! 0))

validBag :: String -> Bool
validBag s = (s =~ bagRe) :: Bool

parseBags :: String -> [Bag]
parseBags s = 
    let xs = splitOn ", " s
        b = filter validBag xs
        bags = map parseBag b
    in bags
        
        
parse :: String -> Record
parse s = 
    let (_, _, _, m) = (s =~ "^([a-z]+ [a-z]+) bags? contain (.*)$") :: (String, String, String, [String])
        bag = m !! 0
        bags = parseBags (m !! 1)
    in Record bag bags

validLines :: String -> Bool
validLines "" = False
validLines s = True

bagName :: Bag -> String
bagName (Bag name _) = name

bagCount :: Bag -> Int
bagCount (Bag _ count) = count

recordName :: Record -> String
recordName (Record name _) = name

recordBags :: Record -> [Bag]
recordBags (Record _ bags) = bags

getRecord :: [Record] -> String -> Record
getRecord xs s = (filter (\x -> (recordName x) == s) xs) !! 0

getRecordBags :: [Record] -> Bag -> [Bag]
getRecordBags records bag = concat (map recordBags (filter (\x -> (recordName x == (bagName bag))) records))

findBagPath' :: [Record] -> String -> Bag -> Bool
findBagPath' records s bag 
    | s == bname = True
    | otherwise = True `elem` (map (\x -> findBagPath' records s x) (getRecordBags records bag))
    where bname = (bagName bag)
   
-- recursive check if path leads to s  
findBagPaths :: [Record] -> String -> Record -> Bool
findBagPaths records s record = True `elem` (map (\x -> findBagPath' records s x) (recordBags record))


-- return nodes that have a path to s 
findBags :: String -> [Record] -> [Record]
findBags s xs = filter (\x -> findBagPaths xs s x) xs
--
-- part 2, count total amount of bags (1 + node.count * (recusrive node.children))
findBagCount :: [Record] -> String -> Int
findBagCount records s = 
    let record = getRecord records s
        bags = recordBags record
    in 1 + sum (map (\x -> (bagCount x) * (findBagCount records (bagName x))) bags)


day7 = do 
    contents <- readFile "data/day7.txt"
    let items = filter validLines (splitOn "\n" contents )
    putStrLn ("Items: " ++ (show items))
    let parsed = map parse items
    let filtered = findBags "shiny gold" parsed 
    putStrLn ("Filtered count: " ++ (show (length filtered)))

    let sum2 = (findBagCount parsed "shiny gold") - 1
    putStrLn ("Part 2: " ++ (show sum2))
