import xlrd
import json
import pickle as pkl
all_attributes = pkl.load(open('gqa_attributes.pkl', 'rb'))
loc = ("attribute_clusters.xlsx")

wb = xlrd.open_workbook(loc)
sheet  = wb.sheet_by_index(0)
clusters = {}
all_values = set([])
for i in range(sheet.ncols):
    values = sheet.col_values(i)
    property_type = values[0].strip()
    property_values = set([x.strip() for x in values[1:]])
    if '' in property_values:
        property_values.remove('')
    clusters[property_type] = list(property_values)
    all_values.update(property_values)
print ('Number of clusters ', len(clusters))
print ('Number of values ', len(all_values))    
for k,v in clusters.items():
    print (k, '::', v)     
print ('\n\n')
for i,k in enumerate(set(all_attributes)-(all_values)):
    print ('Unclustered ::', k)
    clusters['unclustered_'+str(i)] = [k]
clusters_inv = {}
for k, vs in clusters.items():
    for v in vs:
        if v not in clusters_inv:
            clusters_inv[v] = []
        clusters_inv[v].append(k)
        
print ('\n\n')
for k,v in clusters_inv.items():
    if len(v)>1:
        print (k, '::', v)     
json.dump(clusters, open('attribute_clusters.json', 'w'))
        
loc = ("attribute_synonymy_clusters.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
attribute_clusters = json.load(open('attribute_clusters.json', 'rb'))
attribute_synonym_clusters = {}
for i in range(sheet.ncols):
    values = sheet.col_values(i)
    property_type = values[0].strip()
    property_values_clusters = []
    all_values = set([])
    current_cluster =[]
    for v in [x.strip() for x in values[1:]]:
        if len(v)==0:
            if len(current_cluster)>0:
                property_values_clusters.append(current_cluster)
                current_cluster = []
        else:
            current_cluster.append(v)
            all_values.add(v)
    for v in set(clusters[property_type])-set(all_values):
         property_values_clusters.append([v])       
    if len(current_cluster)>0:
       property_values_clusters.append(current_cluster)
    if property_type not in attribute_synonym_clusters:
        attribute_synonym_clusters[property_type] = property_values_clusters

json.dump(attribute_synonym_clusters, open('attribute_synonymy_clusters.json', 'w'))    