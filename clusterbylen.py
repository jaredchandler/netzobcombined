from collections import defaultdict
import sys
dd = defaultdict(lambda:[])

data = sys.stdin.read().strip().split("\n")
for msg in data:
	dd[len(msg)].append(msg)

for i,lens in enumerate(sorted([length for length in dd])):
	for msg in dd[lens]:
		print(str(i)+"\t"+msg)
