
Pseudocode for the ideal, complete synthesis pipeline.

A page may have non-musical content, like text paragraphs and some musical content regions. The page composition is about putting these regions next to each other on a page.

```

Determine the DPI used for all raster generation (i.e. 150 dpi)

Determine the physical size of the synthesized document
    - staff count
    - staff length (i.e. page content "width") (in milimeters)
    - staff proportions and curvature
    - staff vertical spacing
    - viewport gutter (distance from the edge of "content"
        to the edge of the image) (in milimeters)

Synthesize image background
    - color-less
    - then colorize

Synthesize background degradations
    - background seep-through, stains, vignette, ...
    - edge of the paper

Synthesize stafflines

Synthesize text in stafflines (instrument names, title, notes)

Synthesize measure lines if this is a multi-instrument score

Synthesize staff braces

Synthesize music notation

```
