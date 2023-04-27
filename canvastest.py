from tkinter import*
#window = Tk()
#window.title("Canvas test")
#window.geometry("600x600")
#canvas = Canvas(window, width=600, height=600)
#canvas.pack()
#MIDDLE = canvas.winfo_reqheight()/2
height = 0
columns = 0
data = [["Main","aucun",0,0],["Opt","Main",0,1],["Sub1","Main",1,0],["Sub2","Main",1,0],["SS1","Sub1",1,0],["SS2","Sub1",1,0],["SS3","Sub2",1,0],["SS4","Sub2",1,0]]
weights=[]

def find_sub_by_name(data,name):
    inc=0
    for i in data:
        if i[0]==name:
            return data[inc][1]
        inc+=1

def table_to_weight(liste):
    for i in liste:
        prev_j = ''
        nb_w = 0
        w = []
        for j in i:
            if prev_j == j:
                w[nb_w]+=1
            if prev_j != j:
                if w==[]:
                    w.append(1)
                else:
                    nb_w += 1
                    w.append(1)
            prev_j=j
        weights.append(w)

def flat(liste):
    resultat = []
    for element in liste:
        if isinstance(element, list):
            resultat.extend(flat(element))
        else:
            resultat.append(element)
    return resultat

def find_subs(maintask,data):
    subs=[]
    for i in data:
        if i[1] == maintask:
            subs.append(i[0])
    return subs

def add_to_table(table,subs):
    if subs==[]:
        return 1
    else:
        table.append(subs)
        return 0
    
def add_to_level(table,level,subs):
    if level>len(table)-1:
        table.append(subs)
    else:
        table[level].append(subs)

def suivant_dans_liste(liste, element):
    index_element = liste.index(element)
    if index_element < len(liste) - 1:
        return liste[index_element + 1]
    else:
        return None

def check_len(table):
    prev_i = table[0]
    ind = 0
    for i in table:
        if len(i) > len(prev_i):
            new_list = []
            inc=0
            start=0
            precedent=0
            for j in i:
                if j == '|' and start==0:
                    new_list.append(prev_i[inc])
                    inc+=1
                elif j == '|' and start==1:
                    new_list.append(suivant_dans_liste(prev_i,precedent))
                else:
                    precedent = find_sub_by_name(data,j)
                    new_list.append(precedent)
                    start=1
            table[ind-1]=new_list
            
                
            #while len(i) > len(prev_i):
             #   table[ind-1].append(prev_i[-1])
              #  prev_i=table[ind-1]
        elif len(i) < len(prev_i):
            while len(i) < len(prev_i):
                table[ind].append(i[-1])
                i=table[ind]
        prev_i = i
        ind+=1
        
# def data_to_table(data):
#     out = []
#     add_to_table(out,find_subs("aucun",data))
#     add_to_table(out,find_subs(out[0][0],data))
#     check_len(out)
#     if add_to_table(out,find_subs(out[1][0],data)):
#         add_to_level(out,2,['|'])
#     add_to_level(out,2,find_subs(out[1][1],data))
#     out[2]=flat(out[2])
#     check_len(out)
#     check_len(out)
#     return(out)

def data_to_table(data):
    out = []
    level=0
    add_to_table(out,find_subs("aucun",data))
    add_to_table(out,find_subs(out[0][0],data))
    level+=1
    check_len(out)
    
    out.append([])
    for i in out[1]:
        if not find_subs(i,data):
            add_to_level(out,level+1,['|'])
        else:
            add_to_level(out,level+1,find_subs(i,data))
        out[level+1]=flat(out[level+1])
        
    for i in range(1,10):
        check_len(out)
    return out

print(data_to_table(data))
    
    

#window.mainloop()
