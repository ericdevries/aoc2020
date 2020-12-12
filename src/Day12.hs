module Day12 (day12) where

import Data.List
import Data.List.Split
import Data.Sort
import Data.Maybe
import Text.Regex.TDFA

validLines :: String -> Bool
validLines "" = False
validLines s = True

d2i :: Int -> Int
d2i i = round ((fromIntegral i) / 90)

changeDirection :: Char -> Int -> String -> Char
changeDirection c d ord =
    let rel = d2i d
        index = fromJust (elemIndex c ord)
    in ord !! ((index + rel) `mod` 4)

movePart :: String -> Char -> (Char, Int, Int)
movePart xs d 
    | i == 'N' = (d, 0, n)
    | i == 'S' = (d, 0, -n)
    | i == 'E' = (d, -n, 0)
    | i == 'W' = (d, n, 0)
    | i == 'F' = movePart (d:(tail xs)) d
    | i == 'R' = (changeDirection d n "NESW", 0, 0)
    | i == 'L' = (changeDirection d n "NWSE", 0, 0)
    where i = head xs
          n = (read (tail xs))

move :: [String] -> Char -> (Int, Int) 
move input direction
    | null input = (0, 0)
    | otherwise = let
        (nd, nx, ny) = movePart (head input) direction
        (rx, ry) = move (tail input) nd
        in (rx + nx, ry + ny)

rotateWP :: Int -> (Int, Int) -> (Int, Int) 
rotateWP r (a, b)
    | d == 0 = (a, b)
    | d == 1 = (b, -a)
    | d == 2 = (-a, -b)
    | d == 3 = (-b, a)
    where d = (round ((fromIntegral r) / 90))

moveWPPart :: String -> ((Int, Int), (Int, Int)) -> ((Int, Int), (Int, Int)) 
moveWPPart xs ((sx, sy), (wx, wy))
    | i == 'N' = ((sx, sy), (wx, wy + n))
    | i == 'S' = ((sx, sy), (wx, wy - n))
    | i == 'E' = ((sx, sy), (wx + n, wy))
    | i == 'W' = ((sx, sy), (wx - n, wy))
    | i == 'R' = ((sx, sy), (rotateWP n (wx, wy)))
    | i == 'L' = ((sx, sy), (rotateWP (360 - n) (wx, wy)))
    | i == 'F' = ((sx + (wx*n), sy + (wy*n)), (wx, wy)) 
    where i = head xs
          n = (read (tail xs))

moveWP :: [String] -> ((Int, Int), (Int, Int)) -> ((Int, Int), (Int, Int)) 
moveWP input a@((sx, sy), (wx, wy))
    | null input = a
    | otherwise = moveWP (tail input) (moveWPPart (head input) a) 

day12 = do 
    contents <- readFile "data/day12.txt"
    let items = (filter validLines (splitOn "\n" contents))
    putStrLn ("Items: " ++ (show items))

    let answer = move items 'E'
    putStrLn ("Answer input: " ++ (show answer))
    let answer' = (abs (fst answer)) + (abs (snd answer))
    putStrLn ("Answer: " ++ (show answer'))
    
    let tmp1 = moveWP ["F10"] ((0, 0), (10, 1))
    putStrLn ("Answer: " ++ (show tmp1))

    let task2 = moveWP items ((0, 0), (10, 1))
    putStrLn ("Answer: " ++ (show task2))

    let answer2' = (abs (fst (fst task2)) + (abs (snd (fst task2))))
    putStrLn ("Answer2: " ++ (show answer2'))
