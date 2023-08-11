Handwriting serialization
=========================

How is music notation written (in what order and how). Because at the end of the day, there is only one pen-tip and one time-axis. The writer has to serialize it somehow.


## Videos of people writing music

- Handwriting pianoform: https://www.youtube.com/watch?v=MQgDEg4z4fI
- Timelapse, 3-instrument score: https://www.youtube.com/watch?v=vyTyNZn6FD4
- Simple short monophonic: https://youtu.be/zAscL8vT8ck?t=95
- Eh..., artist, not a musician: https://www.youtube.com/watch?v=4KnIwJtvymk
- Talks about page setup: https://www.youtube.com/watch?v=nXN-LLewyRM


## The setup

There is a graph-structure of all the symbols that need to be placed and what their relative position is most likely to be. These symbols are placed in a certain order, until all of them are on the paper. The placement of new symbols may depend on the position of already placed symbols (measure end, other simultaneous voice, accidental's notehead).

*Serialization* is the process of ordering these symbols (in what order they are drawn).

> **Note:** When a well-known combination of symbols is drawn in succession, their drawing operation may be replaced by a *ligature* drawing operation (eighth note in one pen stroke).

Everyone serializes notes differently! Some draw noteheads first, then stems. Some interleave measures from multiple isntruments on a per-beat basis, some don't. Some draw in temporal groups (rest, beamed group, half note). With beamed groups, some draw notes with stems immediately, some draw noteheads, first and last stem, then beam and then middle stems. There are MANY combinations! But there are still combinations that do not occur (like writing stems first and then noteheads, or drawing from right to left, or drwaing randomly).

It almost makes sense to evolve (genetic algorithms) a group of these algorithms and use them, rater then to code them manually, since there are so many of them.

Let's think about the serialization algorithm framing:

- you traverse the abstract notation graph
- when you are in a node that hasn't been drawn yet, you can choose to draw it
- you can also choose to move some other node
- repeat until all nodes are drawn

To evaluate:

- run it together with the drawing system and compute the distance from the ground-truth layout
- minimize "jumps", i.e. minimize the total runtime (so that we don't draw randomly)
- ...something else?


## Drawing system (placing system)

During serialization, each time "draw this node" is called, the drawing subsystem is invoked. Its goal is to place the symbol in the best possible way, given all the already placed *relevant* symbols. This again is a learned system that optimizes *fit* with the gold data. What *relevant symbols* means depends on each symbol and manual analysis is needed for this.


### Placing a ledger line

TODO...


### Placing a notehead

We need to determine two things:

- horizontal position (other symbols and rhythm)
- vertical position (ledger lines)

Spatial relationships, when it comes to noteheads:

- precedent symbol position (notehead, reast, barline, time-signature, key-signature)
- position of other notes with the same onset that have already been placed
- note duration

ALSO:
- ledger lines!?
- chords!?
- chords with too-close notedeads!?
- two voices with too-close noteheads!?
