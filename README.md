# Maximal Clique Enumerator

I implemented the distributed algorithm described in http://www.cs.cuhk.hk/~adafu/Pub/distMaxClique_bigdata14.pdf for finding the maximal cliques in an undirected graph.

I wanted to explore the difficulty of unwrapping the complex ideas in a scientific paper and implementing the algorithms for a practical use. I showed that it is possible -by taking the right scheduling approach- to digest the key facts that allow one to use the scientific results in a matter of hours.

I chose Python due to my familiarity with it and the expressiveness of the resulting implementation.

I used the [SNAP package](http://snap.stanford.edu/snappy/index.html) by Stanford University that allows for easy scalability in graph problems.

# How to use

- Install snap.py `pip3 install snap-stanford`
- Run the script `python3 max_clique.py`