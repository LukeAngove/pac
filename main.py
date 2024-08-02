import yaml
from draw import drawGraph
from reachable import reachableFromStart
from page import makePdf

def main():
    with open("example.yml") as f:
        data = yaml.safe_load(f)

    nodes, paths = reachableFromStart(data["chapters"][0])

    drawGraph(nodes, paths)

    makePdf(data["chapters"][0], nodes, paths)

if __name__ == "__main__":
    main()

