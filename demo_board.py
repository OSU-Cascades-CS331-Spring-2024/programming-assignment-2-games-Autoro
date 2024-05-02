#This file exists to display some board functionality
#Erich Kramer 4/26/18
#
#
#


from board import Board


x = Board(15, 15)


x.set_cell( 4, 4, 'x')

x.set_cell( 1, 3, 'B')


x.display()

y = x.clone_board()
y.display()
