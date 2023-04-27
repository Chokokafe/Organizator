"""A (big) module used to draw graphs for the Organizator."""
# IMPORTS
from tkinter import*

Test window here
window = Tk()
window.title("Canvas test")
window.geometry("600x600")
canvas = Canvas(window, width=600, height=600)
canvas.pack()
MIDDLE = canvas.winfo_reqheight()/2
height = 0
columns = 0
data = [["Main","aucun",0,0],["Opt","Main",0,1],["Sub0","Main",1,0],["Sub1","Main",1,0],["SS1","Sub1",1,0],["SS2","Sub1",1,0],["SS3","Sub2",1,0],["SSS1","SS1",1,0],["SSS2","SS1",1,0]]

window = Tk()
window.title("Canvas test")
window.geometry("600x600")
canvas = Canvas(window, width=600, height=600)
canvas.pack()
MIDDLE = canvas.winfo_reqheight()/2
height = 0
columns = 0
data = [["Main","aucun",0,0],["Opt","Main",0,1],["Sub1","Main",1,0],["Sub2","Main",1,0],["SS1","Sub1",1,0],["SS2","Sub1",1,0],["SSS1","SS1",1,0],["SSS2","SS1",1,0],["Sub3","Main",1,0],["S3","Sub3",1,0]]

def find_sub_by_name(data,name):
	"""Finds the name of the task above a subtask with its name.
	Parameters :
		data(list) : the list containing the tasks from a project
		name(str) : the name of the subtask
	Returns : 
		str : the name of the task above"""
    inc=0
    for i in data:
        if i[0]==name:
            return data[inc][1]
        inc+=1

def find_subs(maintask,data):
	"""Finds the subtasks for a given task.
	Parameters : 
		maintask(str) : the name of the task
		data(list) : the list containing the tasks from a project
	Returns :
		subs(list) : the list containing the names of al the subtasks"""
    subs=[]
    for i in data:
        if i[1] == maintask:
            subs.append(i[0])
    return subs

def flat(liste):
	"""Flats a list containing other lists. Ex : flat(['A',['B','C']]) returns ['A','B','C']
	
	Parameters : 
		liste(list) : The list to flat
	Returns : 
		resultat(list) : The list flattened
	"""aplati
    resultat = []
    for element in liste:
        if isinstance(element, list):
            resultat.extend(flat(element))
        else:
            resultat.append(element)
    return resultat

def suivant_dans_liste(liste, element):
	"""Return the following element on a list according to a particular element
	
	Parameters : 
		liste(list) : The list for searching
		element(str) : The element where to search the following element
	Returns : 
		str : the following element
	"""
    index_element = liste.index(element)
    if index_element < len(liste) - 1:
        return liste[index_element + 1]
    else:
        return None

def add_to_table(table,subs):
	"""Adds list to a list. If the list is empty, returns 1.
	
	Parameters : 
		table(list) : The list where to add other list
		subs(list) : The other list to add in the first
	Returns : 
		int : 1 if the list to add is empty, 0 else.
	"""
    if subs==[]:
        return 1
    else:
        table.append(subs)
        return 0
    
def add_to_level(table,level,subs):
	"""In a 2d-list, add elements to a list located at a certain index.
	
	Parameters : 
		table(list) : The 2d-list where to add elements
		level(list) : The index of the list where to add elements
		subs(list) : The elements to add.
	"""
    if level>len(table)-1:
        table.append(subs)
    else:
        table[level].append(subs)

def check_len(table,data):
	"""Checks the length of a 2d-list. Every list in the 2-dimensional list needs to be the same length for the program to works, this function adds the missing elements.
	
	Parameters : 
		table(list) : The 2d-list where to add elements
		data(list) : The list where to verify subs of elements
	"""
    ind = len(table)-2
    saw = []
    while ind > 1:
        for i in table[ind]:
            if i != '|':
                sub = find_sub_by_name(data,i)
                if not sub in saw:
                    saw.append(sub)
                else:
                    table[ind-1].insert(table[ind-1].index(sub),sub)
                
        ind-=1

def somme_avant(liste, nombre):
	"""Makes the sum of all the elements located before a certain element.
	
	Parameters : 
		liste(list) : the list where to make the sum
		nombre(int) : the number where to stop the sum
	Returns : 
		somme(int) : the sum itself
	"""
    index_nombre = liste.index(nombre)
    elements_avant = liste[:index_nombre]
    somme = sum(elements_avant)
    return somme

def file_to_data(file):
    pass

def data_to_table(data):
	"""Converts a 2d-list containing the tasks to a 2d-list readable by the draw function.
	
	Parameters : 
		data(list) : the first list containing the tasks
	Returns : 
		out(list) : the 2d-list to draw
	"""
    out = []
    level=0
    add_to_table(out,find_subs("aucun",data))
    add_to_table(out,find_subs(out[0][0],data))
    level+=1
    for loop in range(1,3):
        out.append([])
        for i in out[loop]:
            if not find_subs(i,data):
                add_to_level(out,level+1,['|'])
            else:
                add_to_level(out,level+1,find_subs(i,data))
            out[level+1]=flat(out[level+1])
        level+=1
    out.append(["End"])
    check_len(out,data)
    return out

def table_to_weight(liste):
	"""Converts a table readable by the draw function to a list of "weights", the number of rows a cell occupies on the drawing.
	
	Parameters : 
		liste(list) : the table
	Returns : 
		weights(list) : the weights
	"""
    weights=[]
    for i in liste:
        prev_j = ''
        w = []
        nb_w = len(w)-1
        for j in i:
            if j == '|':
                w.append(1)
            else:
                if prev_j == j:
                    w[nb_w]+=1
                if prev_j != j:
                    if w==[]:
                        w.append(1)
                    else:
                        w.append(1)
            prev_j=j
        weights.append(w)
    return weights

def calc_coords(columns,weights,width):
	"""Calculates the coords where to draw text on a specific row."
	
	Parameters : 
		columns(int) : number of columns in a specific row
		weights(list) : weights given by the table_to_weight() function
		width(int) : width of the canvas
	Returns : 
		coords(list) : list of coords
	"""
    width_row = width/columns
    coords = []
    prev_coord = 0
    for i in weights:
        cur_coord = (prev_coord+width_row*i)
        coords.append((prev_coord+cur_coord)/2)
        prev_coord = cur_coord
        
    return coords

def draw(table,weights):
	"""Draws the table on the canvas.
	
	Parameters : 
		table(list) : the table generated by the function data_to_table()
		weights(list) : the list generated by the function table_to_weight()
	"""
    level=0
    for i in weights:
        inc=0
        pointer=0
        coos=calc_coords(sum(i),i,canvas.winfo_reqwidth())
        width_row = canvas.winfo_reqwidth()/sum(i)
        for j in i:
            if level==0:
                canvas.create_text(coos[inc],level*100+40,text=table[level][pointer])
                canvas.create_line((coos[inc]-(int(width_row/2))*j)+20,level*100+60,(coos[inc]+(int(width_row/2))*j)-20,level*100+60)
            elif level==len(table)-2:
                canvas.create_text(coos[inc],level*100+40,text=table[level][pointer])
                canvas.create_line((coos[inc]-(int(width_row/2))*j)+20,level*100+60,(coos[inc]+(int(width_row/2))*j)-20,level*100+60)
                canvas.create_line(coos[inc],level*100-20,coos[inc],level*100+30,arrow=LAST)
                canvas.create_line(coos[inc],level*100+70,coos[inc],level*100+140,arrow=LAST)
            elif level == len(table)-1:
                canvas.create_text(coos[inc],level*100+80,text=table[level][pointer])
                canvas.create_line((coos[inc]-(int(width_row/2))*j)+20,level*100+50,(coos[inc]+(int(width_row/2))*j)-20,level*100+50)
            else:
                canvas.create_text(coos[inc],level*100+40,text=table[level][pointer])
                canvas.create_line((coos[inc]-(int(width_row/2))*j)+20,level*100+60,(coos[inc]+(int(width_row/2))*j)-20,level*100+60)
                canvas.create_line(coos[inc],level*100-20,coos[inc],level*100+30,arrow=LAST)
            pointer+=j
            inc+=1
        level+=1

table = data_to_table(data)
print(table)
weights = table_to_weight(table)
print(weights)
draw(table,weights)
window.mainloop()
