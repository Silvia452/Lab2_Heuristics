from constraint import *

problem = Problem()

""" 
From file map: (stack, depth)
    N N N N     (0,0) (1,0) (2,0) (3,0)
    N N N N     (0,1) (1,1) (2,1) (3,1)
    E N N E     (0,2) (1,2) (2,2) (3,2)       
    X E E X     (0,3) (1,3) (2,3) (3,3)
    X X X X     

    Read output: 
        => map =  [ [N,N,N,N], [N,N,N,N], [E,N,N,E], [X,E,E,X], [X,X,X,X]] 
        (0,0) = N / E / X / c

From file containers: 
        1 S 1
        2 S 1
        3 S 1
        4 R 2
        5 R 2
        
    Read output: 
        => containers = [(S,1), (S,1), (S,1), (R,2), (R,2)]
        containers[i] = "i"   
        

Output File <map>-<containers>.output.          
        Number of solutions: <n>
        {3: (3, 2), 1: (3, 1), 4: (2, 3), 0: (3, 0), 2: (2, 2)}
        {3: (3, 2), 1: (3, 1), 4: (2, 3), 0: (3, 0), 2: (1, 3)}    
        
    Write content: 
        =>   container-id: (stack, depth)
 """

#   Option 1
#   x = [ containers ] | Ds = [cells]
# Constraint 1: There cannot be a container in a cell whose 'below' cells are empty
# Constraint 2: There cannot be a container 'Port2' over container 'Port1'

"""Option 1: 

- The variables will be our containers c : [1, 2, 3, 4, 5, 6, ... , n]
- Domains will be our cells: [(0,0), (0,1), (0,2), (1,0) ...]

(i,j) : map[stack][depth]      => (0,0) = N; (0,2)=E; (0,3)=X
var c : container[c-1] 


- Contraint: In normal cell only standard containers

        if map[i][j] == N and container[c-1] == (S, - ):
            c = (i,j)
            map[i][j] = c

- Contraint: In energy cell only standard refrigerated

        if map[i][j] == E and container[c-1] == (R, -): 
            c = (i,j)
            map[i][j] = c

- Constraint: There cannot be a container in a cell whose 'below' cells are empty

 k is the cells with more depth (below) j of (i,j) in stack (column) i

        To assign to the position (i,j), container c : for all k>j
           (i, k) != empty OR (i,k) == X  
                --> map[i][j] != N OR map[i][j] != E
           

- Constraint: There cannot be a container 'Port2' over container 'Port1'

***        You cannot assign container c where container[c-1] == (-, 2) to position (i,j) :
            if any 
                c' = (i,k) and container[c' - 1] = (-, 1)  for all k>j 
                
                
        

"""
problem.addVariables(x, domain)

# constraints
# -------------------------------------------------------------------------
