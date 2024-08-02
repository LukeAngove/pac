import graphviz

def flags_str(flags):
    return "_".join([k+"_"+("T" if v else "F") for k,v in flags._asdict().items()])

def page_id(scene, vers, flags):
    return scene + "_" + vers + "_" + flags_str(flags)

def drawGraph(nodes, edges):
    dot = graphviz.Digraph()

    all_nodes = []

    for k,v in nodes.items():
        for p in v:
            all_nodes.append((k, *p))

    by_flags = {}

    for s,v,f in all_nodes:
        current = by_flags.get(f, {})
        new = current.get(s, [])
        new.append(v)
        current[s] = new
        by_flags[f] = current


    for f,v in by_flags.items():
        fstr = flags_str(f)
        with dot.subgraph(name="cluster_"+fstr) as g:
            g.attr(label=fstr)
            for s,vers in v.items():
                with g.subgraph(name="cluster_"+fstr+"_"+s) as g2:
                    g2.attr(label=s)
                    for p in vers:
                        g2.node(page_id(s, p, f))

    for target, sources in edges.items():
        for s in sources:
            dot.edge(page_id(*target), page_id(*s))

    print(dot.source)


