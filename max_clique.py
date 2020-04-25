import snap
# G2 = snap.GenRndGnm(snap.PUNGraph, 10, 10)

G2 = snap.TUNGraph.New()

G2.AddNode(1)
G2.AddNode(2)
G2.AddNode(3)
G2.AddNode(4)
G2.AddNode(5)
G2.AddNode(6)
G2.AddNode(7)

G2.AddEdge(1,2)
G2.AddEdge(1,3)
G2.AddEdge(2,3)

G2.AddEdge(5,6)
G2.AddEdge(5,7)
G2.AddEdge(6,7)

def adj_deep(v):
	return [G2.GetNI(x) for x in v.GetOutEdges()]
def adj(v):
	return v.GetOutEdges()

def ID(v):
	if isinstance(v, int):
		return v
	return v.GetId()

def adj_lt(v):
	return [u for u in adj(v) if ID(u) < ID(v)]
def adj_gt(v):
	return [u for u in adj_deep(v) if ID(u) > ID(v)]

def assign_data_to_workers(G2):
	for v in G2.Nodes():
		print(v.GetId())
		worker((ID(v), (v, adj(v))))
		for u in adj_lt(v):
			worker((ID(u), (v, adj(v))))
			
def inter(a, b):
	x = set(a) 
	if isinstance(b, list):
		y = {z.GetId() for z in b}
	else:
		y = set(b)
	return x.intersection(y)

def worker(pair: tuple):
	v_id, (v, adj_v) = pair
	extra_set = {(u.GetId(), adj(u)) for u in adj_gt(v)}
	ADJ_gt_v = dict()
	ADJ_v = dict()
	for u, adj_u in extra_set:
		ADJ_gt_v[u] = inter(adj_u, adj_gt(v))
		ADJ_v[u] = inter(adj_u, adj(v))

	result = LocalMCE(
		{ID(v)}, 
		{x.GetId() for x in adj_gt(v)}, 
		set(adj_lt(v)), 
		ADJ_gt_v, 
		ADJ_v
	)
	print('worker ended:', result)

def LocalMCE(C: set, cand: set, prev: set, ADJ_gt_v: dict, ADJ_v: dict):
	if len(cand) == 0 and len(prev) == 0:
		print('finished', C)
	elif len(cand) > 0:
		u_p = max(cand, key=lambda u_p: len(cand.intersection(ADJ_gt_v[u_p])))
		U = cand - ADJ_gt_v[u_p]
		U = list(U)
		U.sort(key=lambda u: len(ADJ_gt_v[u]), reverse=True)
		for u in U:
			cand = cand - {u}
			cand_tonos = cand.intersection(ADJ_gt_v[u])
			ADJ_gt_v_tonos = dict()
			ADJ_v_tonos = dict()
			for w in cand_tonos:
				ADJ_gt_v_tonos[w] = ADJ_gt_v[w].intersection(cand_tonos)
				ADJ_v_tonos[w] = ADJ_v[w].intersection(prev)

			LocalMCE(C.union({u}), cand_tonos, prev.intersection(ADJ_v[u]), ADJ_gt_v_tonos, ADJ_v_tonos)
			prev = prev.union({u})

if __name__ == '__main__':
	assign_data_to_workers(G2)