from fpdf import FPDF

def checkOkay(start, size):
    if abs(start[0] + size[0]) > 1.0:
        print("x invalid", start, size)
        assert abs(start[0] + size[0]) <= 1.0

    if abs(start[1] + size[1]) > 1.0:
        print("y invalid", start, size)
        assert abs(start[1] + size[1]) <= 1.0

def drawText(canvas, text, pos, size):
    checkOkay(pos, size)
    (w,h) = canvas.w,canvas.h
    x = w*pos[0]
    y = h*pos[1]
    ww = w*size[0]
    hh = h*size[1]

    canvas.set_xy(x,y)
    canvas.multi_cell(ww, hh, text, align="C")


def makePage(canvas, scene, version):
    canvas.add_page()
    (w,h) = canvas.w,canvas.h

    for o in scene.get("objects", []):
        if o["type"] == "image":
            pass
        elif o["type"] == "text":
            drawText(canvas, o["text"], o["start"], o["size"])

    for o in version.get("objects", []):
        if o["type"] == "image":
            pass
        elif o["type"] == "text":
            drawText(canvas, o["text"], o["start"], o["size"])
    return canvas.add_link()

def addLinks(canvas, paths, chapter, page, link_targets, page_id):
    canvas.page = page
    (w,h) = canvas.w,canvas.h

    scene = page_id[0]
    s = chapter["scenes"][scene]
    v = s["versions"][page_id[1]]
    flags = page_id[2]

    for o in s.get("objects", []) + v.get("objects", []):
        target = None

        for tscene, tversion, tflags in paths[page_id]:
            if "link" in o:
                if tscene == o["link"]:
                    target = (tscene, tversion, tflags)
            elif "choice" in o:
                if tscene == scene and tversion == o["choice"]:
                    target = (tscene, tversion, tflags)

        if target:
            x = o["start"][0]
            y = o["start"][1]
            ww = o["size"][0]
            hh = o["size"][1]

            link = link_targets[target][1]
            canvas.link(x*w, y*h, ww*w, hh*h, link)

def addPages(result, chapter, nodes):
    page_index = {}

    # Add the first page first, so we start in the right spot.

    first_scene = chapter["start"]
    first_vers = chapter["scenes"][first_scene]["targets"]["default"]

    for scene, vers in nodes.items():
        s = chapter["scenes"][scene]
        for v in vers:
            # Set up first page
            if scene == first_scene and v[0] == first_vers and all(v[1]) == False:
                link = makePage(result, s, s["versions"][v[0]])
                page_index[(scene, *v)] = (result.page, link)
                break

    for scene, vers in nodes.items():
        s = chapter["scenes"][scene]
        for v in vers:
            # Skip the first page when we see it again.
            if scene == first_scene and v[0] == first_vers and all(v[1]) == False:
                continue
            link = makePage(result, s, s["versions"][v[0]])
            page_index[(scene, *v)] = (result.page, link)

    return page_index


def makePdf(chapter, nodes, paths):
    result = FPDF(orientation="P", unit="pt", format="A4")
    result.set_font(family="Times")

    page_index = addPages(result, chapter, nodes)

    for page_id, (page, link) in page_index.items():
        addLinks(result, paths, chapter, page, page_index, page_id)

    result.output("shapes.pdf")
    
if __name__ == "__main__":
    main()

