import itertools
import os
from collections import Counter, defaultdict
import copy

class SudokuError(Exception):
    def __init__(self,message):
        self.message = message


class Sudoku:
    def __init__(self,file_name):
        self.file_name = file_name
        self.file = open(file_name, 'r')
        file = self.file
        
        
        lines = self.file.read().split("\n")
        rows = 0
        matrix = []
        
        for i in lines:
            non_space_line = False
            numbers_in_line = []
            for n in i:
                if n.isdigit():
                    numbers_in_line.append(int(n))

            if numbers_in_line:
                if len(numbers_in_line) == 9:
                    rows += 1
                    matrix.append(numbers_in_line)

        if rows == 9:
            self.matrix = matrix
            
        file = file_name    
        self._get_input(file)    
              
    
    def _get_input(self,file):
        
        self.file_name = file
        self.file = open(file, 'r')
        file = self.file
        
        lines = self.file.read().split("\n")
        rows = 0
        matrix = []
        for i in lines:
            non_space_line = False
            numbers_in_line = []
            for n in i:
                if n.isdigit():
                    numbers_in_line.append(int(n))

            if numbers_in_line:
                if len(numbers_in_line) != 9:
                    raise SudokuError('Incorrect input')
                rows += 1
                matrix.append(numbers_in_line) 
        if rows!= 9:
            raise SudokuError('Incorrect input')
        
        
    def preassess(self):
        matrix = self.matrix
        clear_solution = True
        
        # Checking each row
        for row in matrix:
            row_seen = []
            for col in matrix:
                if col in row_seen:
                    clear_solution = False
                    break
                elif col != 0:
                    row_seen.append(col)
                    
        # Checking each column            
        for i in range(9):
            col_seen = []
            for j in range(9):
                if matrix[j][i] in col_seen:
                    clear_solution = False
                    break
                elif matrix[j][i] != 0:
                    col_seen.append(matrix[j][i])
        
        # getBlocks return list of number in each 3*3 cell in a list. Use 1/3*i, 1/3*j then to find each individual row number            
        cells = Sudoku.getBlocks(matrix)
                    
        for c in cells:
            if not Sudoku.square_seen(c):
                clear_solution = False
                break                
            
        if not clear_solution:
            print('There is clearly no solution.')
        else:
            print('There might be a solution.')
        
    # square_seen checks if there is repeated number in a list
    def square_seen(mat):
        seen = []
        valid = True
        for i in mat:
            if i in seen and i != 0:
                valid = False
                break
            else:
                seen.append(i)
                    
        return valid
    
    # getBlocks return list of number in each 3*3 cell in a list. Use 1/3*i, 1/3*j then to find each individual row number   
    def getBlocks(mat):
        cells = []
        for r in range(3):
            for c in range(3):
                block = []
                for i in range(3):
                    for j in range(3):
                        block.append(mat[3*r + i][3*c + j])
                cells.append(block)
                
        return cells
    
    # Produce a tex file of unsolved Sudoku
    def bare_tex_output(self):
        mat = self.matrix
        file_name = self.file_name
        file = self.file
        tex_file_name = file_name.split('.')
        tex_file_name = tex_file_name[0]+str('_bare.tex')
        Line_count = 1
        
        with open(tex_file_name,'w') as tex_file:

            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage[left=0pt,right=0pt]{geometry}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{positioning}\n'
                  '\\usepackage{cancel}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n                               label=above right:{\\tiny #2},\n                               label=below left:{\\tiny #3},\n                               label=below right:{\\tiny #4}]{#5};}}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\tikzset{every node/.style={minimum size=.5cm}}\n'
                  '\n'
                  '\\begin{center}\n'
                  '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline', file = tex_file
                  )
            
            for i in mat:
                line_tex = []
                if Line_count != 1:
                    print('', file = tex_file)                
                print(f'% Line {Line_count}',file = tex_file)
                
                for n in i:
                    if n == 0:
                        n = ''
                    line_tex.append(str('{}{}{}{}{'+str(n)+'}'))
                if Line_count %3:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline', file = tex_file)
                else:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline\hline', file = tex_file)
                Line_count += 1
                            
            print('\\end{tabular}\n'
                  '\\end{center}\n'
                  '\n'
                  '\\end{document}', file = tex_file
                  )
            
    def finding_highes_freq(mat,remain_num):
        
        total_form = []
        # Finding highest frequency number
        for lines in mat:
            for val in lines:
                if val and val in remain_num:
                    total_form.append(val)
                   
        highest_freq_number, freq = Counter(total_form).most_common(1)[0]

        return highest_freq_number
    
    def check_numbers(row):
        valid_nums = set(range(1,10))
        for i in row:
            if i in valid_nums:
                valid_nums.remove(i)
                
        return valid_nums
    
    def check_remain_numbers(alist,valid_nums):
        for i in alist:
            if i in valid_nums:
                valid_nums.remove(i)
                
        return valid_nums
    
    def get_columns(matrix):
        list_cols = []
        for i in range(9):
            cols = []
            for j in range(9):
                cols.append(matrix[j][i])
            list_cols.append(cols)
            
        return list_cols
    
    def crossing_out(cells_dictionary,highest_freq_num):
        to_be_forced = []
        super_cells = []
        unique_set = []
        for i in cells_dictionary:
            super_cells.append([i,cells_dictionary[i]])
        
        for the_set in super_cells:
            if highest_freq_num in the_set[1][0]:
                unique_set.append(the_set)
                
        if len(unique_set) == 1:
            unique_set = unique_set[0]
            cell_to_analyse = unique_set[1][0]
            for the_sets in super_cells:
                
                if the_sets is not unique_set:
                    cell_to_analyse -= the_sets[1][0]
            
            if len(cell_to_analyse) == 1:
                to_be_forced.append([unique_set[0],[cell_to_analyse]])
        
        return to_be_forced
        
    def forced_tex_output(self):
        mat = self.matrix
        cells = Sudoku.getBlocks(mat)
        cols = Sudoku.get_columns(mat)    
        
        remain = set(range(1,10))
        while remain:
            highest_freq_num = Sudoku.finding_highes_freq(mat,remain)
            mat = Sudoku.force_values(mat,highest_freq_num)
            remain.remove(highest_freq_num)
            
        file_name = self.file_name
        file = self.file
        tex_file_name = file_name.split('.')
        tex_file_name = tex_file_name[0]+str('_forced.tex')
        Line_count = 1
        
        with open(tex_file_name,'w') as tex_file:

            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage[left=0pt,right=0pt]{geometry}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{positioning}\n'
                  '\\usepackage{cancel}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n                               label=above right:{\\tiny #2},\n                               label=below left:{\\tiny #3},\n                               label=below right:{\\tiny #4}]{#5};}}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\tikzset{every node/.style={minimum size=.5cm}}\n'
                  '\n'
                  '\\begin{center}\n'
                  '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline', file = tex_file
                  )
            
            for i in mat:
                line_tex = []
                if Line_count != 1:
                    print('', file = tex_file)                
                print(f'% Line {Line_count}',file = tex_file)
                
                for n in i:
                    if n == 0:
                        n = ''
                    line_tex.append(str('{}{}{}{}{'+str(n)+'}'))
                if Line_count %3:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline', file = tex_file)
                else:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline\hline', file = tex_file)
                Line_count += 1
                            
            print('\\end{tabular}\n'
                  '\\end{center}\n'
                  '\n'
                  '\\end{document}', file = tex_file
                  )        
       
    def force_values(mat,highest_freq_num):
        try:
            cells = Sudoku.getBlocks(mat)
            cols = Sudoku.get_columns(mat)        
            temp_cell_made = False
            value_was_forced = False
            for block in cells:
                if highest_freq_num not in set(block):
                    temp_cell_dict = defaultdict(list)
                    for pos, val in enumerate(block):
                        if not val:
                            cell_num = cells.index(block)
                            if cell_num<=2:
                                row_num = pos//3
                            if cell_num>=3 and cell_num<=5:
                                row_num = pos//3 + 3
                            if cell_num>=6:
                                row_num = pos//3 + 6
                            
                            # check remaining numbers in rows
                            current_row = mat[row_num]
                            current_cell_valid_num = Sudoku.check_numbers(current_row)
                            
                            # check remaining numbers in cols
                            if cell_num == 0 or cell_num == 3 or cell_num == 6:
                                col_num = pos%3
                            if cell_num == 1 or cell_num == 4 or cell_num == 7:
                                col_num = pos%3 + 3
                            if cell_num == 2 or cell_num == 5 or cell_num == 8:
                                col_num = pos%3 + 6                        
                            current_column = cols[col_num]
                            current_cell_valid_num = Sudoku.check_remain_numbers(current_column,current_cell_valid_num)
                            
                            # check blocks
                            current_cell = block
                            current_cell_valid_num = Sudoku.check_remain_numbers(current_cell,current_cell_valid_num)
                                                        
                            temp_cell_dict[(row_num,col_num)].append(current_cell_valid_num)
                            temp_cell_made = True
                            
                if temp_cell_made:
                    to_be_forced = Sudoku.crossing_out(temp_cell_dict,highest_freq_num)                    
                    temp_cell_made = False
                    if to_be_forced:
                        for i in to_be_forced:
                            if highest_freq_num in i[1][0]:
                                mat[i[0][0]][i[0][1]] = highest_freq_num
                                value_was_forced = True
                                if value_was_forced:
                                    mat = Sudoku.force_values(mat,highest_freq_num)
                                    if mat:
                                        cells = Sudoku.getBlocks(mat)
                                        cols = Sudoku.get_columns(mat)                                
                
            return mat
        except:
            return mat
                
    def marked_tex_output(self):
        mat = self.matrix
        cells = Sudoku.getBlocks(mat)
        cols = Sudoku.get_columns(mat)   
        
        remain = set(range(1,10))
        while remain:
            highest_freq_num = Sudoku.finding_highes_freq(mat,remain)
            mat = Sudoku.force_values(mat,highest_freq_num)
            remain.remove(highest_freq_num)
        
        mat = Sudoku.mark_sudoku(mat)
                                
        file_name = self.file_name
        file = self.file
        tex_file_name = file_name.split('.')
        tex_file_name = tex_file_name[0]+str('_marked.tex')
        Line_count = 1
        
        with open(tex_file_name,'w') as tex_file:

            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage[left=0pt,right=0pt]{geometry}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{positioning}\n'
                  '\\usepackage{cancel}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n                               label=above right:{\\tiny #2},\n                               label=below left:{\\tiny #3},\n                               label=below right:{\\tiny #4}]{#5};}}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\tikzset{every node/.style={minimum size=.5cm}}\n'
                  '\n'
                  '\\begin{center}\n'
                  '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline', file = tex_file
                  )
            
            for i in mat:
                line_tex = []
                if Line_count != 1:
                    print('', file = tex_file)                
                print(f'% Line {Line_count}',file = tex_file)
                
                for n in i:
                    if n == 0:
                        n = ''
                    if type(n) == type(set()):
                        possible_numbers_1_2 = []
                        possible_numbers_3_4 = []
                        possible_numbers_5_6 = []
                        possible_numbers_7_8_9 = []
                        for number in n:
                            if number <= 2:
                                possible_numbers_1_2.append(number)
                            if number > 2 and number <= 4:
                                possible_numbers_3_4.append(number)
                            if number > 4 and number <= 6:
                                possible_numbers_5_6.append(number)
                            if number > 6:
                                possible_numbers_7_8_9.append(number)
                        
                        possible_1 = " ".join(str(x) for x in possible_numbers_1_2)
                        possible_2 = " ".join(str(x) for x in possible_numbers_3_4)
                        possible_3 = " ".join(str(x) for x in possible_numbers_5_6)
                        possible_4 = " ".join(str(x) for x in possible_numbers_7_8_9)
                        line_tex.append(str('{')+str(possible_1)+str('}{')+str(possible_2)+str('}{')+str(possible_3)+str('}{')+str(possible_4)+str('}{}'))
                    else:    
                        line_tex.append(str('{}{}{}{}{'+str(n)+'}'))
                    
                if Line_count %3:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline', file = tex_file)
                else:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline\hline', file = tex_file)
                Line_count += 1
                            
            print('\\end{tabular}\n'
                  '\\end{center}\n'
                  '\n'
                  '\\end{document}', file = tex_file
                  )        
       
        
        
    def mark_sudoku(mat):
        
        cells = Sudoku.getBlocks(mat)
        cols = Sudoku.get_columns(mat)        
        temp_cell_made = False
        temp_cell_dict = defaultdict(list)
        for block in cells:
            #if highest_freq_num not in set(block):
            
            for pos, val in enumerate(block):
                if not val:
                    cell_num = cells.index(block)
                    if cell_num<=2:
                        row_num = pos//3
                    if cell_num>=3 and cell_num<=5:
                        row_num = pos//3 + 3
                    if cell_num>=6:
                        row_num = pos//3 + 6
                    
                    # check remaining numbers in rows
                    current_row = mat[row_num]
                    current_cell_valid_num = Sudoku.check_numbers(current_row)
                    
                    # check remaining numbers in rows
                    if cell_num == 0 or cell_num == 3 or cell_num == 6:
                        col_num = pos%3
                    if cell_num == 1 or cell_num == 4 or cell_num == 7:
                        col_num = pos%3 + 3
                    if cell_num == 2 or cell_num == 5 or cell_num == 8:
                        col_num = pos%3 + 6                        
                    current_column = cols[col_num]
                    current_cell_valid_num = Sudoku.check_remain_numbers(current_column,current_cell_valid_num)
                    
                    # check blocks
                    current_cell = block
                    current_cell_valid_num = Sudoku.check_remain_numbers(current_cell,current_cell_valid_num)
                    
                    temp_cell_dict[(row_num,col_num)].append(current_cell_valid_num)
                    temp_cell_made = True                        
        
        if temp_cell_made:
            for cell in temp_cell_dict:
                position = cell
                possible_numbers = temp_cell_dict[cell]
                x, y = position
                mat[x][y] = possible_numbers[0]
                
        return mat
    
    def split_grid_to_blocks():
        block1 = []
        block2 = []
        block3 = []
        block4 = []
        block5 = []
        block6 = []
        block7 = []
        block8 = []
        block9 = []
        for i in range(9):
            for j in range(9):
                if not i//3 and not j//3:
                    block1.append((i,j))
                if not i//3 and j//3 == 1:
                    block2.append((i,j))
                if not i//3 and j//3 == 2:
                    block3.append((i,j))
                if i//3 == 1 and not j//3:
                    block4.append((i,j))
                if i//3 == 1 and j//3 == 1:
                    block5.append((i,j))
                if i//3 == 1 and j//3 == 2:
                    block6.append((i,j))
                if i//3 == 2 and not j//3:
                    block7.append((i,j))
                if i//3 == 2 and j//3 == 1:
                    block8.append((i,j))
                if i//3 == 2 and j//3 == 2:
                    block9.append((i,j))
        return [block1,block2,block3,block4,block5,block6,block7,block8,block9]
    
    def split_grid_to_blocks_with_setsOnly(mat):
        block1 = []
        block2 = []
        block3 = []
        block4 = []
        block5 = []
        block6 = []
        block7 = []
        block8 = []
        block9 = []
        for i in range(9):
            for j in range(9):
                if type(mat[i][j]) == type(set()):
                    if not i//3 and not j//3:
                        block1.append((i,j))
                    if not i//3 and j//3 == 1:
                        block2.append((i,j))
                    if not i//3 and j//3 == 2:
                        block3.append((i,j))
                    if i//3 == 1 and not j//3:
                        block4.append((i,j))
                    if i//3 == 1 and j//3 == 1:
                        block5.append((i,j))
                    if i//3 == 1 and j//3 == 2:
                        block6.append((i,j))
                    if i//3 == 2 and not j//3:
                        block7.append((i,j))
                    if i//3 == 2 and j//3 == 1:
                        block8.append((i,j))
                    if i//3 == 2 and j//3 == 2:
                        block9.append((i,j))
        return [block1,block2,block3,block4,block5,block6,block7,block8,block9]    
    
    def worked_tex_output(self):
        mat = self.matrix
        cells = Sudoku.getBlocks(mat)
        cols = Sudoku.get_columns(mat)             
        remain = set(range(1,10))
        while remain:
            highest_freq_num = Sudoku.finding_highes_freq(mat,remain)
            mat = Sudoku.force_values(mat,highest_freq_num)
            remain.remove(highest_freq_num)
        
        mat = Sudoku.mark_sudoku(mat)
        oldmat = copy.deepcopy(mat)
        
            
        sudoku_dictionary = {}
        for row in range(9):
            for col in range(9):
                sudoku_dictionary[(row,col)] = mat[row][col]
        
        mat, sudoku_dictionary = Sudoku.preemptive_find(mat,sudoku_dictionary)

        for row_number, row_val in enumerate(mat):
            for col_number, val in enumerate(row_val):
                if type(val) == type(set()) and len(val) == 1:
                    mat[row_number][col_number] = list(val)[0]
                    sudoku_dictionary[(row_number,col_number)] = list(val)[0]
        
        mat, sudoku_dictionary = Sudoku.update_marks(mat,sudoku_dictionary)
        
        for row_number, row_val in enumerate(mat):
            for col_number, val in enumerate(row_val):
                if type(val) == type(set()) and len(val) == 1:
                    mat[row_number][col_number] = list(val)[0]
                    sudoku_dictionary[(row_number,col_number)] = list(val)[0]
                    
        file_name = self.file_name
        file = self.file
        tex_file_name = file_name.split('.')
        tex_file_name = tex_file_name[0]+str('_worked.tex')
        Line_count = 1
        
        with open(tex_file_name,'w') as tex_file:

            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage[left=0pt,right=0pt]{geometry}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{positioning}\n'
                  '\\usepackage{cancel}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n                               label=above right:{\\tiny #2},\n                               label=below left:{\\tiny #3},\n                               label=below right:{\\tiny #4}]{#5};}}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\tikzset{every node/.style={minimum size=.5cm}}\n'
                  '\n'
                  '\\begin{center}\n'
                  '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline', file = tex_file
                  )        
        
            for row_num, row in enumerate(mat):    
                line_tex = []
                if Line_count != 1:
                    print('', file = tex_file)                
                print(f'% Line {Line_count}',file = tex_file)
                
                for col_num, n in enumerate(row):
                    if n == 0:
                        n = ''
                    if type(n) == type(int(1)) and type(oldmat[row_num][col_num]) == type(int(1)):
                        if n == oldmat[row_num][col_num]:
                            line_tex.append(str('{}{}{}{}{'+str(n)+'}'))
                    else:
                        solution = ''
                        if type(n) == type(int(1)):
                            solution = str(n)
                            n = set([n,-1])
                        possible_numbers_1_2 = []
                        possible_numbers_3_4 = []
                        crossedout2 = ''
                        possible_numbers_5_6 = []
                        possible_numbers_7_8_9 = []
    
                        # If the number in n is in original_set it means it is not solved so should not be crossed out
                        original_set = list(oldmat[row_num][col_num])
                        original_set.sort()
  
                        for number in original_set:
                            if number <= 2:
                                if number in n and str(number) != solution:
                                    possible_numbers_1_2.append(number)
                                else:
                                    crossedout2 = str('\\cancel')+str('{')+str(number)+str('}')
                                    possible_numbers_1_2.append(crossedout2)
                            if number > 2 and number <= 4:
                                if number in n and str(number) != solution:
                                    possible_numbers_3_4.append(number)
                                else:
                                    crossedout2 = str('\\cancel')+str('{')+str(number)+str('}')
                                    possible_numbers_3_4.append(crossedout2)
                            if number > 4 and number <= 6:
                                if number in n and str(number) != solution:
                                    possible_numbers_5_6.append(number)
                                else:
                                    crossedout2 = str('\\cancel')+str('{')+str(number)+str('}')
                                    possible_numbers_5_6.append(crossedout2)
                            if number > 6:
                                if number in n and str(number) != solution:
                                    possible_numbers_7_8_9.append(number)
                                else:
                                    crossedout2 = str('\\cancel')+str('{')+str(number)+str('}')
                                    possible_numbers_7_8_9.append(crossedout2)
                                    
                        possible_1 = " ".join(str(x) for x in possible_numbers_1_2)
                        possible_2 = " ".join(str(x) for x in possible_numbers_3_4)
                        possible_3 = " ".join(str(x) for x in possible_numbers_5_6)
                        possible_4 = " ".join(str(x) for x in possible_numbers_7_8_9)                    
                        line_tex.append(str('{')+str(possible_1)+str('}{')+str(possible_2)+str('}{')+str(possible_3)+str('}{')+str(possible_4)+str('}{'+solution+str('}')))
                    
                if Line_count %3:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline', file = tex_file)
                else:
                    print(f'\\N{line_tex[0]} & \\N{line_tex[1]} & \\N{line_tex[2]} &\n\\N{line_tex[3]} & \\N{line_tex[4]} & \\N{line_tex[5]} &\n\\N{line_tex[6]} & \\N{line_tex[7]} & \\N{line_tex[8]} \\\ \hline\hline', file = tex_file)
                Line_count += 1
                            
            print('\\end{tabular}\n'
                  '\\end{center}\n'
                  '\n'
                  '\\end{document}', file = tex_file
                  )                    
    
    def update_marks(mat,sudoku_dictionary):
                
        for row in mat:
            number_range = set(range(1,10))
            for val in row:
                if type(val) == type(int(1)):
                    number_range.remove(val)
            for sets in row:
                if type(sets) == type(set()):
                    set_to_check = sets.copy()
                    for num in set_to_check:
                        if num not in number_range:
                            sets.remove(num)
       
        cols = Sudoku.get_columns(mat)
        for columns in cols:
            number_range = set(range(1,10))
            for val in columns:
                if type(val) == type(int(1)):
                    number_range.remove(val)
            for sets in columns:
                if type(sets) == type(set()):
                    set_to_check = sets.copy()
                    for num in set_to_check:
                        if num not in number_range:
                            sets.remove(num)   
                            
        cells = Sudoku.getBlocks(mat)
        for block in cells:
            number_range = set(range(1,10))
            for val in block:
                if type(val) == type(int(1)):
                    number_range.remove(val)
            for sets in block:
                if type(sets) == type(set()):
                    set_to_check = sets.copy()
                    for num in set_to_check:
                        if num not in number_range:
                            sets.remove(num)           
                            
        for row_number, row_val in enumerate(mat):
            for column_number, col_val in enumerate(row_val):
                sudoku_dictionary[(row_number,column_number)] = col_val
       
        return mat, sudoku_dictionary    
        
    def preemptive_find(mat,sudoku_dictionary):
        try:
            sorted_blocks = Sudoku.split_grid_to_blocks_with_setsOnly(mat)
            
            for block_number in sorted_blocks:
                for combo_length in range(2,len(block_number)):
                    for combines in itertools.combinations(block_number,combo_length):
                        combine_set = set()
    
                        for possible_cells in combines:
                            combine_set = combine_set.union(sudoku_dictionary[possible_cells])
                        
                        if len(combines) == len(combine_set):
                            pre_emptive = [combines, combine_set]
                            if pre_emptive:
                                original_block = block_number
                                not_in_preemptive = (x for x in original_block if x not in combines)
                                cross = False
                                for to_cross_out in not_in_preemptive:
                                    to_be_crossed_out_set = sudoku_dictionary[to_cross_out]
                                    set_after_crossed_out = [n for n in to_be_crossed_out_set if n not in combine_set]
                                    
                                    if set_after_crossed_out:
                                        sudoku_dictionary[to_cross_out] = set(set_after_crossed_out)
                                        mat[to_cross_out[0]][to_cross_out[1]] = set(set_after_crossed_out)
                                        
                                        if len(set_after_crossed_out) == 1:
                                            sudoku_dictionary[to_cross_out] = set_after_crossed_out[0]
                                            mat[to_cross_out[0]][to_cross_out[1]] = set_after_crossed_out[0]
                                            cross = True

                                if cross:
                                    mat, sudoku_dictionary = Sudoku.update_marks(mat,sudoku_dictionary)
                                    mat, sudoku_dictionary = Sudoku.preemptive_find(mat,sudoku_dictionary)
            
            for row_num, row_val in enumerate(mat):
                sets_cells = []
                for col_num, val in enumerate(row_val):
                    if type(val) == type(set()):
                        sets_cells.append((row_num, col_num))
                
                if sets_cells:
                    for set_length in range(2,len(sets_cells)):
                        for combines in itertools.combinations(sets_cells,set_length):
                            combine_set = set()
        
                            for possible_cells in combines:
                                combine_set = combine_set.union(sudoku_dictionary[possible_cells])
                            
                            if len(combines) == len(combine_set):
                                pre_emptive = [combines, combine_set]
                                if pre_emptive:
                                    not_in_preemptive = (x for x in sets_cells if x not in combines)
                                    cross = False
                                    for to_cross_out in not_in_preemptive:
                                        
                                        to_be_crossed_out_set = sudoku_dictionary[to_cross_out]
                                        set_after_crossed_out = [n for n in to_be_crossed_out_set if n not in combine_set]
                                        if set_after_crossed_out:
                                            sudoku_dictionary[to_cross_out] = set(set_after_crossed_out)
                                            mat[to_cross_out[0]][to_cross_out[1]] = set(set_after_crossed_out)
                                            
                                            if len(set_after_crossed_out) == 1:
                                                sudoku_dictionary[to_cross_out] = set_after_crossed_out[0]
                                                mat[to_cross_out[0]][to_cross_out[1]] = set_after_crossed_out[0]
                                                cross = True
                                    if cross:
                                        mat, sudoku_dictionary = Sudoku.update_marks(mat,sudoku_dictionary)
                                        mat, sudoku_dictionary = Sudoku.preemptive_find(mat,sudoku_dictionary)                                    
                    
            cols = Sudoku.get_columns(mat)
            for col_num, col_val in enumerate(cols):
                sets_cells = []
                for row_num, val in enumerate(col_val):
                    if type(val) == type(set()):
                        sets_cells.append((row_num, col_num))
                
                if sets_cells:
                    for set_length in range(2,len(sets_cells)):
                        for combines in itertools.combinations(sets_cells,set_length):
                            combine_set = set()
        
                            for possible_cells in combines:
                                combine_set = combine_set.union(sudoku_dictionary[possible_cells])
                            
                            if len(combines) == len(combine_set):
                                pre_emptive = [combines, combine_set]
                                if pre_emptive:
                                    not_in_preemptive = (x for x in sets_cells if x not in combines)
                                    cross = False
                                    for to_cross_out in not_in_preemptive:
                                        
                                        to_be_crossed_out_set = sudoku_dictionary[to_cross_out]
                                        set_after_crossed_out = [n for n in to_be_crossed_out_set if n not in combine_set]
                                        if set_after_crossed_out:
                                            sudoku_dictionary[to_cross_out] = set(set_after_crossed_out)
                                            mat[to_cross_out[0]][to_cross_out[1]] = set(set_after_crossed_out)
                                            
                                            if len(set_after_crossed_out) == 1:
                                                sudoku_dictionary[to_cross_out] = set_after_crossed_out[0]
                                                mat[to_cross_out[0]][to_cross_out[1]] = set_after_crossed_out[0]
                                                cross = True
                                    if cross:
                                        mat, sudoku_dictionary = Sudoku.update_marks(mat,sudoku_dictionary)
                                        mat, sudoku_dictionary = Sudoku.preemptive_find(mat,sudoku_dictionary)  
                                        
            return  mat, sudoku_dictionary
        except:
            return  mat, sudoku_dictionary
    
