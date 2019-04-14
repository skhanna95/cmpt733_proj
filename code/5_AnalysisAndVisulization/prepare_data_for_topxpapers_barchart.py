import pickle
with open('pmid_list', 'rb') as f:
    pmid_list = pickle.load(f)
with open('title_list', 'rb') as f:
    title_list = pickle.load(f)
with open('pmid2ind', 'rb') as f:
    pmid2ind = pickle.load(f)
with open('gbc_pmids', 'rb') as f:
    gbc_pmids=pickle.load(f)
with open('gbc_titles', 'rb') as f:
    gbc_titles=pickle.load(f)
with open('gbc_pmid2ind', 'rb') as f:
    gbc_pmid2ind=pickle.load(f)

depth_constrain = 5
with open(f'depth{depth_constrain}_nodes_visitedConstrain_entity_sixGroup', 'rb') as f:
    entity_sixGroup=pickle.load(f)

# here deal with the whole gbc papers 

# get the combines of six group, and the count of the six groups
for entity in entity_sixGroup:
    sixGroup_pmids = set()
    for i in range(1,7):
        sixGroup_pmids |= entity[i]
    entity.update({'combined':sixGroup_pmids, 'cnt':len(sixGroup_pmids)})

# get the cnt of every gbc paper
gbc_sixCnts = []
for i in range(len(gbc_pmids)):
    gbc_sixCnts.append({1:0, 2:0, 3:0, 4:0, 5:0, 6:0})
    
for entity in entity_sixGroup:
    for i in range(1,7):
        for pmid in entity[i]:
            gbc_sixCnts[gbc_pmid2ind[pmid]][i]+=1

# get how many gbc papers get at least one citation
gbc_cited_cnt = 0
for cnts in gbc_sixCnts:
    cntssum = sum([x for x in cnts])
    if cntssum>0:
        gbc_cited_cnt+=1

# get the top x gbc paper that got cited

import queue
PQ = queue.PriorityQueue()
for ind, item in enumerate(gbc_sixCnts):
    cnt = sum([item[x] for x in range(1,7)])
    PQ.put((-cnt, gbc_pmids[ind]))

top_x = 50#gbc_cited_cnt

topxgbc_pmids = []
topxgbc_pmid2cnt = {}
for _ in range(top_x):
    cnt, pmid = PQ.get()
    cnt = -cnt
    topxgbc_pmid2cnt.update({pmid:cnt})
    topxgbc_pmids.append(pmid)

topxgbc_pmids_set = set(topxgbc_pmids)

# Here deal with the top x gbc papers

# get rid of the other cited papers of entity_sixgroup that is not in topxgbc_pmids_set
for entity in entity_sixGroup:
    for i in range(1,7):
        entity[i] = entity[i]&topxgbc_pmids_set

# get the combined of sixGroup, and store the count in 'cnt'
for entity in entity_sixGroup:
    sixGroup_pmids = set()
    for i in range(1,7):
        sixGroup_pmids |= entity[i]
    entity.update({'combined':sixGroup_pmids, 'cnt':len(sixGroup_pmids)})




# now the entity_sixgroup only has references that is in topxgbc_pmids_set 
# get the data
titles_sixGroup = {'titles':[],
                   1:[0]*len(topxgbc_pmids),
                   2:[0]*len(topxgbc_pmids),
                   3:[0]*len(topxgbc_pmids),
                   4:[0]*len(topxgbc_pmids),
                   5:[0]*len(topxgbc_pmids),
                   6:[0]*len(topxgbc_pmids), }
pmid2sixGroupInd = {}
for i, pmid in enumerate(topxgbc_pmids):
    ind = gbc_pmid2ind[pmid]
    titles_sixGroup['titles'].append(gbc_titles[ind])
    pmid2sixGroupInd.update({pmid: i})


# get the entities that has at least one reference as the nodes
for ind, entity in enumerate(entity_sixGroup):

    if entity['cnt']>0:
        for i in range(1,7):
            for pmid in entity[i]:
                titles_sixGroup[i][ pmid2sixGroupInd[pmid]]+=1



import pickle
with open(f'depth{depth_constrain}_nodes_visitedConstrain_{top_x}_titles_sixGroup', 'wb') as f:
    print(f'saving depth{depth_constrain}_nodes_visitedConstrain_{top_x}_titles_sixGroup')
    pickle.dump(titles_sixGroup, f)
