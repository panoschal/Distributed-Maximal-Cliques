import snap
# G2 = snap.GenRndGnm(snap.PUNGraph, 10, 10)

G2 = snap.TNGraph.New()
G2.AddNode(1)
G2.AddNode(2)
G2.AddNode(3)
G2.AddNode(4)
G2.AddEdge(1,2)
G2.AddEdge(1,3)
G2.AddEdge(2,3)

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

def first(G2):
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
	ADJ_gt_v = {}
	ADJ_v = {}
	for u, adj_u in extra_set:
		ADJ_gt_v[u] = inter(adj_u, adj_gt(v))
		ADJ_v[u] = inter(adj_u, adj(v))

	set_of_v = set([ID(v)])
	result = LocalMCE(set_of_v, set(x.GetId() for x in adj_gt(v)), set(adj_lt(v)), ADJ_gt_v, ADJ_v)
	print('worker ended:', result)

def LocalMCE(C, cand, prev, ADJ_gt_v, ADJ_v):
	if len(cand) == 0 and len(prev) == 0:
		print('finished', C)
	elif len(cand) > 0:
		u_p = max(cand, key=lambda u_p: len(cand.intersection(ADJ_gt_v[u_p])))
		U = cand - ADJ_gt_v[u_p]
		U = list(U)
		U.sort(key=lambda u: len(ADJ_gt_v[u]), reverse=True)
		for u in U:
			set_of_u = set([u])

			cand = cand - set_of_u
			cand_tonos = cand.intersection(ADJ_gt_v[u])
			ADJ_gt_v_tonos = {}
			ADJ_v_tonos = {}
			for w in cand_tonos:
				ADJ_gt_v_tonos[w] = ADJ_gt_v[w].intersection(cand_tonos)
				ADJ_v_tonos[w] = ADJ_v[w].intersection(prev)

			LocalMCE(C.union(set_of_u), cand_tonos, prev.intersection(ADJ_v[u]), ADJ_gt_v_tonos, ADJ_v_tonos)
			prev = prev.union(set_of_u)

first(G2)