import sys
import copy
import itertools

#MÅL: lav en algoritme som kan løse en sudoku, hvor jeg giver den start informationen, i fx en .txt fil.

#Ordbog: (alle variabler bliver kodet med små bogstaver)

#Grid:				Spille bræt som er inddelt i et 9x9 gitter format 			 
#Sub-Grid:			Et under gitter som er inddelt i 3x3 format
#Square:			En enkelt celle i et gitter
#Row:				En hel række af celler inden i et gitter
#Column:			En hel kolonne af celler inden i et gitter
#Sub-Row:			En række af af 3 celler inden i et under gitter
#Sub-Column:		En kolonne af af 3 celler inden i et under gitter
#Candidate:			En mulig løsning for en enkelt celle
#Solved:			En celle er løst når den har opnået den korrekte værdi
#Set 				At sætte eller fastholde en værdi

#------------------------------------------------------------------------
#Indenholder selve pudslespillet som en 2d liste. Blanke celler represænteres som et '0'
#Hver celle bliver et kordinat som 'settes' i et dobbelt array 
		#main_grid[x][y]
main_grid = [[] for x in range(9)]
#-----------------------------------------------------------------------------------
#-------------------------------------------------------------------------
#Holder alle potientielle kandidater for hver celle som et dobbelt array
#individuelle celler "settes" med adgang: candidates_grid[x][y]
candidates_grid = [[set()for y in range(9)] for x in range(9)]
#--------------------------------------------------------------------------
#---------------------------------------------------------------------------
#Skal holde alle 'solved' værdier i en/et individuelt row/col/sub_grid
col_set = [set() for x in range(9)] #adgang = col_set[x]
row_set = [set() for x in range(9)] #adgang = row_set[y]
sub_grid_set = [[set() for y in range(3)] for x in range(3)]
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Diverse 'sets' som skal bruges til at løse eller optimere
full_set = {1,2,3,4,5,6,7,8,9}
coordinates_set = {0,1,2,3,4,5,6,7,8}
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
# lav en metode som populere main_grid og cadidates_grid (row/col/block sættes fra en data fil.) 
def makeGrids():
	with open('path to data file') as puzzle
	for y in range(9):
		next_line = puzzle.readline()
		for x in range(9):
			main_grid[x].append(int(next_line[x]))
			if next_line[x] != '0':
				col_set[x].add(int(next_line[x]))
				row_set[y].add(int(next_line[x]))
				sub_grid_set[x // 3][y // 3].add(int(next_line[x]))

	for y in range(9):
		for x in range(9):
			if main_grid[x][y] == 0:
				candidatesSet 0 set.union(row_set[y], col_set[x],
					sub_grid_set[x//3][y//3])
				candidates_grid[x][y] = full_set.difference(candidatesSet)
#-----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#metoder til at printe gitter og lave iterationer over under gitteret og på en linje
def iterration_over_subgrids(func, *args):
	for sub_grid_y in range(3):
		for sub_grid_x in range(3):
			func(sub_grid_x, sub_grid_y, *args)

def iterration_over_line(func, *args):
	for square in range(9):
		func(square, *args)

def print_main_grid():
	for y in range(9):
		for x in range(9):
			print(main_grid[x][y], end="")
			if x % 3 == 2:
				print(" ", end="")
		print("")

def print_candidates_grid():
	for y in range(9):
		for x in range(9):
			print(candidates_grid[x][y], " ", end="")
		print("")

def is_solved():
	for y in range(9):
		if len(row_set[y]) != 9:
			return False
	return True
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#Skriver løsningen til main_grid og opdatere 'set' værdier og tabeller
def pencil_in_for_solution(solution, x, y, func):
	sub_grid_x = x//3
	sub_grid_y = y//3
	main_grid[x][y] = solution
	row_set[y].add(solution)
	col_set[x].add(solution)
	sub_grid_set[sub_grid_x][sub_grid_y].add(solution)
	candidates_grid[x][y].clear()

	for sub_g_y in range(sub_grid_y *3, sub_grid_y *3+3):
		for sub_g_x in range(sub_grid_x *3, sub_grid_x *3+3):
			candidates_grid[sub_g_x][sub_g_y].discard(solution)
	for i in range(9):
		candidates_grid[x][i].discard(solution)
		candidates_grid[i][y].discard(solution)
#------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#Metode som skal løse en celle som kun har én kandidat
def single_candidate_square(y):
	for x in range(9):
		if len(candidates_grid[x][y].pop(), x, y,
			single_candidate_square)
#------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#Metode som skal løse en celle hvor en kadidat kun er én løsning på en række
def single_candidate_square_row(y):
	for candidate in full_set.difference(row_set[y])#spring løste værdier over
	count = 0
	previous_row = 0
	for x in range(9):
		if candidate in cadidates_grid[x][y]:
			count += 1
			previous_row = x
	if count == 1:
		pencil_in_for_solution(candidate, previous_row, y, single_candidate_square_row)
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#Metode som skal løse en celle hvor en kadidat kun har én løsning på en kolonne
def single_candidate_square_column(x):
	for candidate in full_set.difference(col_set[x]):
		count = 0
		previous_col = 0
		for y in range(9):
			if candidate in cadidates_grid[x][y]:
				count += 1
				previous_col = y
		if count == 1:
			pencil_in_for_solution(candidate, previous_col, single_candidate_square_column)
#---------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#Metode for en celle som kun har en kadidat i et sub_grid
def single_square_candidate_subgrid(sub_grid_x, sub_grid_y):
	for candidate in full_set.difference(sub_grid_set[sub_grid_x][sub_grid_y]):
		count = 0
		previous_coordinates = [0,0]
		for y in range(sub_grid_y *3, sub_grid_y *3+3):
			for x in range(sub_grid_x *3, sub_grid_x *3+3):
				if candidate in candidates_grid[x][y]:
					count += 1
					previous_coordinates[0]=x
					previous_coordinates[1]=y
			if count == 1:
				pencil_in_for_solution(candidate, previous_coordinates[0], previous_coordinates[1],
					single_square_candidate_subgrid)
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#Metode som skal finde kadidater i en blok som kun ligger i én sub_row
#Derefter skal den fjerne kandidater fra resten af den row.
def claim_number_row(sub_grid_x, sub_grid_y):
	#få alle 'sette' kandidater for alle sub_rows
	subrow_sets = [set(), set(), set()]
	for y in range(sub_grid_y *3, sub_grid_y *3+3):
		for x in range(sub_grid_x *3, sub_grid_x *3+3):
			subrow_sets[y%%3] = subrow_sets[y%%3].union(candidates_grid[x][y])

	#få kandidater fra sub_rows i en forældre række
	claimed = [subrow_sets[0].difference(subrow_sets[1],subrow_sets[2])]
	claimed.append(subrow_sets[1].difference(subrow_sets[0],subrow_sets[2]))
	claimed.append(subrow_sets[2].difference(subrow_sets[0],subrow_sets[1]))
	#fjern kadidater fra andre sub_rows i forældre rækken
	for sub_row in range(3):
		for claimant in set(claimed[sub_row]):
			for x in range(9):
				if x//3 != sub_grid_x:
					candidates_grid[x][sub_grid_y *3 + sub_row].discard(claimant)
#-------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#metode som minder som claim number for rows bare for en kolonne.
def claim_number_col(sub_grid_x, sub_grid_y):
	subcol_sets = [set(), set(), set()]
	for x in range(sub_grid_x *3, sub_grid_x *3+3):		
		for y in range(sub_grid_y *3, sub_grid_y *3+3):
			subcol_set[x%%3] = subcol_sets[x%%3].union(candidates_grid[x][y])

	#få kandidater fra sub_col i en forældre kolonne
	claimed = [subcol_sets[0].difference(subcol_sets[1],subcol_sets[2])]
	claimed.append(subcol_sets[1].difference(subcol_sets[0],subcol_sets[2]))
	claimed.append(subcol_sets[2].difference(subcol_sets[0],subcol_sets[1]))

	#fjern kadidater fra andre sub_col i forældre kolonnen
	for sub_col in range(3):
		for claimant in set(claimed[sub_col]):
			for x in range(9):
				if y//3 != sub_grid_y:
					candidates_grid[sub_grid_x *3 + sub_col][y].discard(claimant)
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#nu kommer der en lidt mere juicy matematik 

#Problem stilling: 
	#Hvad gør man med felter hvor der er to eller flere kandidater? (rækker og kolonner)

#Find sæt af 'n' celler i en række hvor følgene gælder:
# - ingen celler indenholder mere end 'n' kandidater hver.
# - Kardinaltallet af sættet af alle kandidater i celler er 'n' 
# - Alle kandidater i det sæt kan antages at ligge i en af de celler.
#så det vil sige at de 'set' kandidater fra andre celler i den række kan fjernes.
#sudoku løsere kender måske allerede det fenomenet 'disjoint' eller at finde 'par' eller 'tripler' 
#i koden vil jeg referere til dette som disjoint

#Basis eksempel: Tre celler i en rækker indenholder kadidatsætne {2,4},{2,7},{4,7}. 
#Alle tre celler indenholder ikke flere end 3 kandidater.
#Det samlede sæt for alle kadidater er {2,4,7} som har et kardinaltal på 3.
#Det kan derfor konkluderes af disse celler MÅ indenholde 2, 4 eller 7 og INGEN andre. 
#Alle andre celler som ligger uden for dette set som også skulle indenholde en af kadidaterne kan nu fjernes.
#------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------- 
#metode som kan disjoint en række 
def disjoint_subsets_row(y,n):
	sets = []
	#find alle kandidatsæt i en række, hvor kardinaltallet ikke er større end 'n'
	for x in range(9):
		if 1 < len(cadidates_grid[x][y]) <= n:
			sets.append(candidates_grid[x][y])

	#For alle undersæt af disjoints fundet i andre celler kan nu fjernes.
	for d in get_disjoint_subsets(sets, n):
		for x in range(9):
			if not candidates_grid[x][y].issubset(d):
				candidates_grid[x][y] = candidates_grid[x][y].difference(d)
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#Metode som disjoint for en række bare for en kolonne
def disjoint_subsets_column(x,n):
	sets = []
	#find alle kandidatsæt i en kolonne, hvor kardinaltallet ikke er større end 'n'
	for y in range(9):
		if 1 < len(candidates_grid[x][y] <= n
			sets.append(candidates_grid[x][y]))

	#For alle undersæt af disjoints fundet i andre celler kan nu fjernes.
	for d in get_disjoint_subsets(sets, n):
		for y in range(9):
			if not candidates_grid[x][y].issubset(d):
				candidates_grid[x][y] = candidates_grid[x][y].difference(d)
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#Metode for a disjoint sub_grids
def disjoint_subsets_subgrids:
	sets = []
	for y in range(sub_grid_y *3, sub_grid_y*3+3):
		for x in range(sub_grid_x*3, sub_grid_x*3+3):
			if 1 < len(candidates_grid[x][y]) <= n:
				sets.append(candidates_grid[x][y])

	for d in get_disjoint_subsets(sets. n):
		for y in range(sub_grid_y*3, sub_grid_y*3+3):
			for x in range(sub_grid_x*3, sub_grid_x*3+3):
				if not candidates_grid[x][y].issubset(d):
					candidates_grid[x][y] = candidates_grid[x][y].difference(d)
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
def get_disjoint_subsets(sets, n):
	disjoint_subsets = set()
	for combination in itertools.combinations(sets, n):
		superset = set()
		for c in combination:
			superset = superset.union(c)
		if len(superset) == n:
			disjoint_subsets.add(frozenset(superset))
	return disjoint_subsets
#--------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
def solve():
	for x in range(100):
		iterration_over_line(single_candidate_square)
		iterration_over_line(single_candidate_square_row)
		iterration_over_line(single_candidate_square_column)
		iterration_over_subgrids(single_square_candidate_subgrid)
		iterration_over_subgrids(claim_number_row)
		iterration_over_subgrids(claim_number_col)
		for n in range(2,5):
			iterration_over_line(disjoint_subsets_row, n)
			iterration_over_line(disjoint_subsets_column, n)
			iterration_over_line(disjoint_subsets_subgrids, n)
		if is_solved == 1:
			print_main_grid()
			break
makeGrids()
solve()





























 
