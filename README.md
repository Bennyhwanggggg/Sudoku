# Sudoku

This project aims to solve sudoku using the forced digits and preemptive sets method described in the paper Pencil-and-Paper Algorithm for Solving Sudoku Puzzles by
J. F. Crook. However, the implementation stops after preemptive set technique can no longer be applied. Therefore, some difficult Sudokus cannot be solved.  

sudoku.py is a class object that has each part of the implementation inside it. The file will read XXXX.txt file (as seen in the given example sudoku.txt file)
and can do the following:

- preassess: shows whether the given txt file gives a correctly set sudoku. (e.g No same number on the same line)
- bare_tex_output: outputs the given sudoku into a Latex code file.
- forced_tex_output: outputs a Latex code file that will show what the sudoku look like after forced digit technique has been applied.
- marked_tex_output: outputs a Latex code file that will show what the sudoku look like after forced digit technique has been applied and then marked.
- worked_tex_output: outputs a Latex code file that showsshow what the sudoku look like after forced digit technique has been applied and then marked and then the preemptive set technique is applied until it can't be applied anymore.

The Latex code can then be converted into pdf files by compiling with pdflatex to give images provided in the example pdf files. Other method of compiling is using an online Latex comiler called ShareLaTeX at https://www.sharelatex.com/