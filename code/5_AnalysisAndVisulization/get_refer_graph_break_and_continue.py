import pickle
import requests
import time
import json
import queue
import time

with open('pmid_list', 'rb') as f:
    pmid_list = pickle.load(f)
with open('title_list', 'rb') as f:
    title_list = pickle.load(f)
with open('pmid2ind', 'rb') as f:
    pmid2ind = pickle.load(f)

# 19934212,6704287
def pmids2pmids(pmids_):
    pmids_ = ','.join(list(map(str,pmids_)))
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pubmed_refs&'+\
          f'id={pmids_}' + '&format=json&api_key=b9056d083d23b60058ea9dc7f9a802b2db08'
    try:
        rs = requests.get(url)
        #print(url)
        time.sleep(0.1)
        try:
            rs_dict = json.loads(rs.text)
        except json.decoder.JSONDecodeError as e:
            print(f'json decode error, ulr={url}')
            print(e)
            return None
        if 'linksets' in rs_dict:
            item = rs_dict['linksets'][0]
            if 'linksetdbs' in item:
                pmids = item['linksetdbs'][0]['links']
                return pmids

    except requests.exceptions.RequestException as e:
        print(f'requests.get({url}) results in this error:')
        print(e)

    return None






class Node(object):
    def __init__(self, **kv):

        if 'depth' in kv:
            self.depth = kv['depth']
        else:
            self.depth = 0

        if 'entity_pmid' in kv:
            self.entity_pmid = kv['entity_pmid']
        else:
            self.entity_pmid = None

        if 'pmids' in kv:
            self.pmids = kv['pmids']
        else:
            self.pmids = []

        if 'id' in kv:
            self.id = kv['id']
        else:
            self.id = None

        self.children = []







#只要不为0即可，大于lst长度也可以
def list_segs(length, l):
    for i in range(0,len(l),length):
        yield l[i:i+length]
        
# lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1] #lst可为空
# for l in list_segs(5, lst):
#     print(l)
# [1, 2, 3, 4, 5]
# [6, 7, 8, 9, 8]
# [7, 6, 5, 4, 3]
# [2, 1]


pre_depth_constrain = 4
with open(f'depth{pre_depth_constrain}_nodes_visitedConstrain', 'rb') as f:
    nodes=pickle.load(f)
premax_depth = pre_depth_constrain + 1


Q = queue.Queue()

entity_visited = []
for i in pmid_list:
    entity_visited.append(set())

node_id = 0
for node in nodes:
    if node.entity_pmid is not None:
        entity_visited[pmid2ind[node.entity_pmid]].update(node.pmids)
    if node.depth==premax_depth:
        Q.put(node)
    node_id+=1


start_time = time.time()
depth_constraint = 5
while not Q.empty():
    node = Q.get()
    entity_pmid = node.entity_pmid
    entity_ind = pmid2ind[entity_pmid]
    if node.depth <= depth_constraint:
        ref_pmids = pmids2pmids(node.pmids)
        if ref_pmids is not None:
            ref_pmids = list(set(ref_pmids) - entity_visited[entity_ind])
            if ref_pmids is not None:
                for ref_pmids_seg in list_segs(99, ref_pmids):
                    ref_node = Node(pmids=ref_pmids_seg,
                                    depth=node.depth+1,
                                    entity_pmid=entity_pmid,
                                    id=node_id)
                    node_id+=1
                    nodes.append(ref_node)
                    node.children.append(ref_node)
                    Q.put(ref_node)
                    entity_visited[entity_ind].update(ref_pmids_seg)

            print(node_id, ' depth=', node.depth)

print(f'When depth constraint={depth_constraint}, the run time is {time.time()-start_time} seconds.')

# store the nodes
with open(f'depth{depth_constraint}_nodes_visitedConstrain', 'wb') as f:
    pickle.dump(nodes, f)

