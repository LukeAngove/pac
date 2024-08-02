# Point and Click (PaC)

## Introduction

Simple engine for point and click games, initially targeting PDFs.

## Overview

Games are built using YAML. The layout is as follows:

- Chapters
  - Flags
  - Scenes
    - Choices
      - Text
      - Locations
    - Links
      - Text
      - Images

### Chapters

A chapter is a segment of the game/book with a single entry and a single exit.
Flags can only be set within a chapter. All flags are reset in the next chapter.
If different paths are needed across chapters, this can be hacked by making
two exits from one chapter into two "alternate" chapters. All flags will be
reset in the new chapter.

This is because 'flags' are implemented by making multiple copies of every
page within a chapter, using links to store the information of which flags
are set, and which are not. The more flags present in a chapter, the larger
the resulting file will be, as every scene will be replicated for each
feasible combination of flags.

### Scenes

A scene is a single display. Scenes have choices, and moved between using links.
A scene has configuration that is shared by every choice in the 'choices'.

### Choices

Choices move within pages in a scene. They may not link to other scenes. When a
scene is left and returned to, the choices are not remembered, unless they result
in setting a flag that changes where a link to the scene, and the scene is revisited.

### Links

Links move to other scenes. These do not target a particular page, they only target
a scene. Which page in a scene is chosen depends on the flags that are currently set.

## YAML

Example:

```yaml
- title: "Chapter 1: The Beginning"
  flags:
    - key
    - apple
  start:
    - home
    - init
  scenes:
    home:
      image: "house.jpg"
      versions:
        init:
          text: "This is your house."
          choices:
            - text: "Go left"
              link: ["tree", "first"]
            - text: "Go right"
              link: ["gate", "first"]
            - text: "inspect"
              link: ["inspect"]
        inspect:
          text: "There's nothing here."
            - text: "Go left"
              link: ["tree", "first"]
            - text: "Go right"
              link: ["gate", "first"]
            - text: "inspect"
              link: ["inspect"]
    tree:
      image: "tree.jpg"
       first:
          text: "You see a tree."
          choices:
            - text: "Go left"
              link: ["gate", "first"]
            - text: "Go right"
              link: ["home", "inspect"]
            - text: "inspect"
              link: ["inspect"]
        inspect:
          text: "You find a key!"
            - text: "Go left"
              link: ["gate", "first"]
            - text: "Go right"
              link: ["home", "inspect"]
            - text: "inspect"
              link: ["inspect"]
    gate:
      image: "tree.jpg"
      first:
          text: "This is a gate."
          choices:
            - text: "Go right"
              link: ["tree", "first"]
            - text: "Go left"
              link: ["home", "inspect"]
            - text: "inspect"
              link: ["inspect"]
        inspect:
          text: "There's nothing here."
            - text: "Go right"
              link: ["tree", "first"]
            - text: "Go left"
              link: ["home", "inspect"]
            - text: "inspect"
              link: ["inspect"]
```

