parent_chromosomes=['Tt','tt']
offspings=[]
for father_c in parent_chromosomes[0]:
    for mother_c in parent_chromosomes[1]:
        offsping_gene=father_c+mother_c
        offspings.append(offsping_gene)
print(offspings)