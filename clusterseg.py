from netzob.all import *
from netzob.Inference.Vocabulary.FormatOperations.ClusterByAlignment import ClusterByAlignment
from netzob.Inference.Vocabulary.FormatOperations.FieldSplitAligned.FieldSplitAligned import FieldSplitAligned
from collections import defaultdict
# print(ClusterByAlignment())
# print(FieldSplitAligned())

def nzclustering(data):
  
  messages = [RawMessage(bytes.fromhex(line)) for line in data]

  clustering = ClusterByAlignment()
  symbols = clustering.cluster(messages)

  res = [[m.data.hex() for m in symbols[i].messages] for i in range(len(symbols))]

  return res

import sys
data = sys.stdin.read()

data = data.upper().strip().split("\n")

# r = nzclustering(data)


# Given a list of messages, segment into fields
def nzsegmentMsgs(data):

  messages = [RawMessage(bytes.fromhex(line)) for line in data]
  symbol = Symbol(messages=messages)
  symbol.addEncodingFunction(TypeEncodingFunction(HexaString))
  # print(symbol)
  # print(symbol.fields)
  # for f in symbol.fields:
  #   print(type(f),f.getValues())
  # print("---")

  # NEED AN IMPORT 

  fs = FieldSplitAligned()
  fs.execute(symbol,useSemantic=False)
  
  # print(type(symbol))
  dd = defaultdict(lambda:[])

  for j,f in enumerate(symbol.fields):
    #print(type(f),f.getCells())
    for i,v in enumerate(f.getValues()):
      dd[i]+=[v]
  #print("HARNESSSTART")
  RES_MSGS = []
  for k in sorted(dd):
    RES_MSGS.append(str(b' '.join([v for v in dd[k] if v != b'']))[2:-1])
  #print("HARNESSEND")
  return RES_MSGS







# Given a list of clusters, with each cluster being a list of messages
# Desegment each message in the cluster and add the cluster id to a lookup. 

  
def desegmentmsg(msg):
    return msg.replace(" ","").upper()

def normalizeResults(origmsgs,clusters):
  assert(len(origmsgs)==sum([len(c) for c in clusters]))


  msgs2clusters = defaultdict(lambda:[])
  for i,cluster in enumerate(clusters):
    #s = segmentMsgs(cluster)
    for m in cluster:
      # Use the desegmented message as a key
      msgs2clusters[desegmentmsg(m)].append((i,m.upper()))
      

  # Reverse the indexes,such that we will pop the first ones added
  
  for m in msgs2clusters:
    msgs2clusters[m] = msgs2clusters[m][::-1]


  res = []
  # Extract
  for msg in origmsgs:
    i,segmsg = msgs2clusters[msg.upper()].pop()


    res.append((i,segmsg))

  return res


def nzClusterSeg(origmsgs):
  # Make clusters
  clusters = nzclustering(origmsgs)
  # Segment each clusters
  res = [nzsegmentMsgs(cluster) for cluster in clusters]
  return res



# --------------------------------------------------------------------------

# Create clusters and segment each message within the cluster
segclusters = nzClusterSeg(data)
# Given the original order of the data, create the 

for i,v in enumerate(segclusters):
  for m in v:
    print(str(i)+"\t"+m)

if False:
  nr = normalizeResults(data,segclusters)

  for i,v in nr:
    print(i,"\t",v)

# What should the universal resule be?

# Messages in original order as pairs with cluster ID and segmented message




#print(segmentMsgs(data.strip().split("\n")))
