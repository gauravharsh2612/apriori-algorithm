# imports 
import random 
import itertools
import json
import numpy

# assumed dataset - this is avaialable products to be bought
data = ["xbox", "ps5", "neon-lights", "table-lights", "keyboard", "laptop", "mouse", "tv", "fifa21", "gta"]

transactions  = []
# this is to generate random data - max purchase you can do at once 
maxPurachase = 5
c = 0.4 # this is confidence 
def generateData(data, n = 60):
  output = []
  for _ in range(n):
    k = set()
    for i in range(random.randint(1,maxPurachase)):
      k.add(data[random.randint(0,len(data)-1)])
    output.append(list(k))
  return output

transactions = generateData(data)

# generate random transactions 
def generateItemset(itemset, size):
  data = set()
  for p in itemset:
    for k in p:
      data.add(k)
  data = list(data)
  output = []
  p = list(itertools.combinations(data, size))
  for data in p:
    output.append(list(data))
  return output

# filtering out the transactions from support 
def filterItemset(itemset, transactions, minSupport = 2):
  count = {}
  for p in itemset:
    for t in transactions:
      ans = True
      for i in numpy.in1d(numpy.array(p), numpy.array(t)):
        ans &= i
      if ans:
        try:
          count[json.dumps(p)] += 1
        except:
          count[json.dumps(p)] = 1
  updatedCount = {}
  for i in count:
    if count[i] >= minSupport:
      updatedCount[i] = count[i]
  # print(updatedCount)
  return updatedCount


# filter associations from confidence 
def filterSet(data):
  output = []
  for i in range(1, len(data)):
    for k in data[i]:
      v = data[i][k]
      for t in json.loads(k):
        # print(k, t,  v / p[0][json.dumps([t])])
        if v / data[0][json.dumps([t])] >= c:
          print(k)
          output.append([k, t,  v / data[0][json.dumps([t])]])
  return output


# core apriori logic 
def apriori(data, transactions):
  size = 1
  itemset = []
  sizeset = [] 
  while size <= 5:
    if size == 1:
      p = filterItemset(generateItemset(transactions, size), transactions)
      itemset = [json.loads(x) for x in p.keys()]
      size += 1
      print(p)
      sizeset.append(p)
    else:
      p = filterItemset(generateItemset(itemset, size), transactions)
      itemset = [json.loads(x) for x in p.keys()]
      size += 1
      print(p)
      sizeset.append(p)
  print(sizeset)
  output = filterSet(sizeset)
  return output  

output = apriori(data, transactions)
print(output)
