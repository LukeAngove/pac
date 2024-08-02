from collections import namedtuple

def reachableFromStart(chapter):
    nodes = {}

    scene = chapter["start"]
    vers = chapter["scenes"][scene]["targets"]["default"]
    start = chapter["scenes"][scene]["versions"][vers]
    flagst = namedtuple("flagst", chapter["flags"])
    flags = flagst(*[False]*len(chapter["flags"]))

    current = (scene, vers, flags)

    parsed = set()
    toparse = set([current])

    paths = dict()

    while len(toparse):
        current = toparse.pop()
        reachable = getReachable(chapter, flagst, *current)
        #for r in reachable:
        #    paths[r] = paths.get(r, set()) | set([current])
        paths[current] = paths.get(current, set()) | set(reachable)
        parsed.add(current)
        new = reachable - parsed
        toparse.update(new)

    nodes = dict()
    for s, v, k in parsed:
        nodes[s] = nodes.get(s, set()) | set([(v,k)])

    return (nodes, paths)

def parseTargets(targets, flags):
    flags = flags._asdict()
    for k,v in targets.items():
        if k in flags and flags[k]:
            return v
    return targets["default"]

def getVersion(scene, flags):
    return parseTargets(scene["targets"], flags)


def setFlags(flagst, version, flags):
    this_flags = flags._asdict()
    for s in version.get("set", []):
        this_flags[s] = True
    for s in version.get("unset", []):
        this_flags[s] = False
    this_flags = flagst(**this_flags)
    return this_flags
 

def getTarget(chapter, this_flags, scene, t):
    if "link" in t:
        return t["link"], getVersion(chapter["scenes"][t["link"]], this_flags), this_flags
    elif "choice" in t:
        return scene, t["choice"], this_flags


def getReachable(chapter, flagst, scene, vers, flags):
    current = chapter["scenes"][scene]["versions"][vers]

    this_flags = setFlags(flagst, current, flags)

    reachable = set()

    for t in current.get("objects", []):
        target = getTarget(chapter, this_flags, scene, t)
        if target:
            reachable.add(target)

    return reachable


