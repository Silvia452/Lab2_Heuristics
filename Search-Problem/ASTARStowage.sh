#!/bin/sh
### BASH FILE IN CHARGE OF INVOKING THE MAIN PROGRAM ###

#argument in $1 = path
#argument in $2 = map file
#argument in $3 = container file
#argument in $4 = heuristic

python3 ASTARStowage.py $1 $2 $3 $4