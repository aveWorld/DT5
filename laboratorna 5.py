import numpy as np
from tabulate import tabulate
from pulp import *

def delete(mat):
    delete_row = [] 
    for i in range(0, len(mat)):
        mat1 = mat[0:i,:]
        mat2 = mat[i+1:len(mat),:]
        mat3 = np.concatenate((mat1, mat2), axis=0)
        for j in range(0, len(mat3)):
            if all(np.greater_equal(mat[i], mat3[j])) == True:
                delete_row.append(j)    
    mat = np.delete(mat, delete_row, 0)
    
    mat = mat.transpose()    
    delete_col = []
    for i in range(0, len(mat)):
        mat1 = mat[0:i,:]
        mat2 = mat[i+1:len(mat),:]
        mat3 = np.concatenate((mat1, mat2), axis=0)
        for j in range(0, len(mat3)):
            if all(np.greater_equal(mat[i], mat3[j])) == True:
                delete_col.append(i)    
    mat = np.delete(mat, delete_col, 0)
    
    mat = mat.transpose()    
    delete_col = []
    for i in range(0, len(mat)):
        mat1 = mat[0:i,:]
        mat2 = mat[i+1:len(mat),:]
        mat3 = np.concatenate((mat1, mat2), axis=0)
        for j in range(0, len(mat3)):
            if all(np.greater_equal(mat[i], mat3[j])) == True:
                delete_col.append(j)    
    mat = np.delete(mat, delete_col, 0)
    
    delete_row = [] 
    for i in range(0, len(mat)):
        mat1 = mat[0:i,:]
        mat2 = mat[i+1:len(mat),:]
        mat3 = np.concatenate((mat1, mat2), axis=0)
        for j in range(0, len(mat3)):
            if all(np.greater_equal(mat[i], mat3[j])) == True:
                delete_row.append(i)
    mat = np.delete(mat, delete_row, 0)

    return mat

def show(table):
    show = tabulate(table, tablefmt='fancy_grid', stralign='center',)
    print(show)

mat = np.loadtxt("laboratorna 5.txt", dtype=int)
print("Платіжна матриця:")
show(mat)
print()

min_in_row = mat.min(axis=1)
print("Мінімальні значення кожного рядка:", min_in_row)
max_in_col = mat.max(axis=0)
print("Максимальні значення кожного стовпця:", max_in_col)

max_min_in_row = max(min_in_row)
min_max_in_col = min(max_in_col)

if max_min_in_row == min_max_in_col:
    print("У вас верхня і нижня ціни гри співпадають.")
    print("Значить гра має сідлову точку:", max_min_in_row)
else:
    print("Сідлова точка відсутня так, як " + str(max_min_in_row) + " ≠ " + str(min_max_in_col))
    print("Отже знаходимо рішення гри у змішаних стратегіях.")
    print()
    
    mat = delete(mat)
    print("Платіжна матриця після видалення домінуючих рядків та стовпчиків:")
    show(mat)

    matrix_for_x = np.transpose(mat)
    
    x = []
    for i in range(0, len(matrix_for_x[0])):
        x.append(LpVariable("x" + str(i + 1), lowBound=0))
    problem_x = LpProblem("Simple Problem", LpMinimize)     
    
    problem_x += sum(x)
    
    for i in range(0, len(matrix_for_x)):
        problem_x += sum(matrix_for_x[i] * x) >= 1
        
    problem_x.solve()
    X = []
    for variable in problem_x.variables():
        X.append(variable.varValue)
    F_x = value(problem_x.objective)
    
    V_x = 1 / sum(X)
    p = []
    for element in X:
        p.append(element * V_x)
    p.append(V_x)
    str_p = []
    for i in range(0, len(matrix_for_x[0])):
        str_p.append("p" + str(i + 1))
    str_p.append("Ціна гри")
    
    y = []
    for i in range(0, len(mat[0])):
        y.append(LpVariable("y" + str(i + 1), lowBound=0))
    problem_y = LpProblem("Simple Problem", LpMaximize)        
        
    problem_y += sum(y)
    
    for i in range(0, len(mat)):
        problem_y += sum(mat[i] * y) <= 1
    
    problem_y.solve()
    Y = []
    for variable in problem_y.variables():
        Y.append(variable.varValue)
    F_y = value(problem_y.objective)
    
    V_y = 1 / sum(Y)
    q = []
    for element in Y:
        q.append(element * V_y)
    q.append(V_y)
    str_q = []
    for i in range(0, len(mat[0])):
        str_q.append("q" + str(i + 1))
    str_q.append("Ціна гри")
    
    x.append("f(x)")
    X.append(F_x)
    table_x = []
    table_x.append(x)
    table_x.append(X)
    print("Таблиця для x:")
    show(table_x)
    
    y.append("f(y)")
    Y.append(F_y)
    table_y = []
    table_y.append(y)
    table_y.append(Y)
    print("Таблиця для y:")
    show(table_y)
    
    table_p = []
    table_p.append(str_p)
    table_p.append(p)
    print("Ціна гри і ймовірності застосування стратегій гравця А:")
    show(table_p)
    
    table_q = []
    table_q.append(str_q)
    table_q.append(q)
    print("Ціна гри і ймовірності застосування стратегій гравця B:")
    show(table_q)
    
    