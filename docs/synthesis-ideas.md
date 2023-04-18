Synthesis Ideas
===============

The synthesized image has lots of *features*. A *feature* is some value that has some probability distribution (i.e. it's a random variable). Examples of features are:

- notehead-accidental offset (X and Y)
- notehead dimensions (X and Y)
- notehead shape itself (in, say 2D latent-space of an autoencoder)

Synthesizer first converts the input music to a set of such features. Then it tries to optimize feature values so that the probability of each feature is reasonable. This step reminds me of constraint solving.


Motivational example
--------------------

Try synthesizing a group of 4 beamed eight notes.

Objects:
- 4 noteheads
- 4 stems
- 1 beam

Constraints (features):
- each notehead
    - has vertical position based on its pitch
    - has image based on the writer
    - has "onset" contraint on its horizontal position (comes after its predecessor)
- each stem
    - is bound to the notehead
    - is bound to the beam
    - has reasonable height (this includes orientation based on pitch, etc...) **BIMODAL!**
    - has reasonable width
- the beam
    - is reasonably straight
    - has reasonable tilt
- the beamed group as a whole has onset constraints?


Step 1:
    Sample all the (constraint) values according to their distributions.
Step 2:
    Modify the sampled values so that the feature values become defined.