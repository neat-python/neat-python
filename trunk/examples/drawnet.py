# Receives a chromosome and returns a graphical representation of its phenotype
# This is a draft solution - works only with linux
import os

def draw(chromosome):
    output = 'digraph G {\n node [shape = circle]'
    for cg in chromosome.conn_genes:
        output += '\n\t'+str(cg.innodeid)+' -> '+str(cg.outnodeid)
        if cg.enabled is False:
            output += ' [style=dotted, color=cornflowerblue]'
        
    output += '\n }'
    
    try:
        #os.system('dot -Tsvg output -o network.svg')
        os.system('echo "'+output+'" | dot -Tsvg > phenotype.svg')
        os.system('eog phenotype.svg')
    except OSError:
        print 'Can\'t find graphviz package'
    
    return output