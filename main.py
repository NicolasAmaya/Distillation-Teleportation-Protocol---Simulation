import random
#import numpy as np

def main():
    qubits = 3
    

    originalTable = genTable(qubits)
    currTable = originalTable.copy()
    count = 0
    while not isCorrect(currTable):
        
        print(f"Iteration {count}:")
        m = genM(qubits)
        st = shiftTable(currTable,m)
        nextTable = correctionTable(currTable,m)
        print(f"error m = {m}")
        print(f"{currTable} - Current Table")
        print(f"{st} - Shifted Table")
        print(f"{nextTable} - Next Table")
        currTable = nextTable
        count += 1
    
    print("Final Table: {}".format(currTable))
    
'''generates the initial table with random values'''
def genTable(qubits: int):
    table = list()
    
    for i in range(2 ** qubits):
        #integer to binary formatting
        bitstr = format(i, f"0{qubits}b")
        #populate table with random bits
        table.append(random.randint(0, 1))

    return table

''' Simulates the error introduced after teleportation'''
def genM(qubits: int):
    for i in range(0,qubits):
        bit = random.randint(0,1)
        if i > 0:
            m = (m << 1) | bit
        else: 
            m = bit
        
    return m 
'''Generates the correct Vf table, this will be used to test correctness'''
def genVf(table: list):
    return [(-1)**entry for entry in table]    

    #return np.diag(diagonal)
'''shifts teh table by some error m'''      
def shiftTable(table:list, m):
    return [table[x ^ m] for x in range(len(table))]
'''generates the table required to correct the previous error'''
def correctionTable(table:list, m):
    #f(x xor m)
    st = shiftTable(table,m)
    # x = f(x) y = f(x xor m) then f'(x) = x xor m =  f(x) xor f(x xor m)
    return [x ^ y for x,y in zip(table,st)]

'''test for degree 0 found/ base case'''
def isCorrect(table:list):
    
    return all([value == table[0] for value in table])

        

if __name__ == "__main__":
    main()

