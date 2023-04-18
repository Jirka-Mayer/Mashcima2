from typing import List, Tuple, Dict, Optional
import random


ONSET_ORIGIN = (2, 7)
ONSET_SPACING = 3
NOTEHEAD_RADIUS = 0.45
STEM_HEIGHT = 2.5


class Feature:
    def __init__(self):
        self.value = random.uniform(0, 1)
        self.force = 0 # same as gradient
    
    def reset_force(self):
        self.force = 0

    def apply_force(self, rate: float):
        self.value += self.force * rate


class Constraint:
    def compute_force(self):
        raise Exception("Not overriden")


class DesiredValue(Constraint):
    def __init__(self, feature, target):
        self.feature = feature
        self.target = target

    def compute_force(self):
        force = self._resolve_target_value() - self.feature.value
        self.feature.force += force
    
    def _resolve_target_value(self):
        if type(self.target) is Feature:
            return self.target.value

        if callable(self.target):
            return self.target()
        
        return self.target


class Notehead:
    def __init__(self, pitch_position):
        # notehead center
        self.x = Feature()
        self.y = Feature()

        # 0 = center line, even are lines, odd are spaces
        self.pitch_position = pitch_position
    
    def generate_features(self):
        yield self.x
        yield self.y
    
    def generate_constraints(self, predecessor):
        # pitch
        yield DesiredValue(n.y, ONSET_ORIGIN[1] - self.pitch_position / 2)
        
        # onset
        if predecessor is None:
            yield DesiredValue(self.x, ONSET_ORIGIN[0])
        else:
            yield DesiredValue(
                self.x,
                lambda predecessor=predecessor: \
                    predecessor.x.value + ONSET_SPACING
            )
    
    def svg(self):
        x = self.x.value
        y = self.y.value
        return f'<circle cx="{x}" cy="{y}" r="{NOTEHEAD_RADIUS}" fill="black" />'


class Stem:
    def __init__(self, notehead: Notehead):
        self.notehead = notehead

        self.x = Feature()
        self.y = Feature()
        self.height = Feature()
    
    def generate_features(self):
        yield self.x
        yield self.y
        yield self.height
    
    def generate_constraints(self):
        yield DesiredValue(
            self.x,
            lambda n=self.notehead: n.x.value + NOTEHEAD_RADIUS
        )
        yield DesiredValue(self.y, self.notehead.y)
        yield DesiredValue(self.height, STEM_HEIGHT)

    def svg(self):
        x1 = self.x.value
        y1 = self.y.value
        x2 = x1
        y2 = y1 - self.height.value
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="0.1" />'


# ==================


features: List[Feature] = []
constraints: List[Constraint] = []


noteheads = [Notehead(-4), Notehead(-2), Notehead(-1), Notehead(-2)]

p = None
for n in noteheads:
    features.extend(n.generate_features())
    constraints.extend(n.generate_constraints(p))
    p = n


stems = [Stem(n) for n in noteheads]

for s in stems:
    features.extend(s.generate_features())
    constraints.extend(s.generate_constraints())

# ===================

def render_frame(index):
    nl = "\n        "
    svg = f"""
    <svg viewBox="0 0 24 12" width="600" height="300" preserveAspectRatio="xMinYMin meet" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="100%" height="100%" fill="white" />

        <line x1="1" y1="5" x2="23" y2="5" stroke="black" stroke-width="0.1" />
        <line x1="1" y1="6" x2="23" y2="6" stroke="black" stroke-width="0.1" />
        <line x1="1" y1="7" x2="23" y2="7" stroke="black" stroke-width="0.1" />
        <line x1="1" y1="8" x2="23" y2="8" stroke="black" stroke-width="0.1" />
        <line x1="1" y1="9" x2="23" y2="9" stroke="black" stroke-width="0.1" />
        
        {nl.join(n.svg() for n in noteheads)}
        {nl.join(s.svg() for s in stems)}
    </svg>
    """
    # print(svg)

    with open(f"/home/jirka/Downloads/layout-{str(index).zfill(3)}.svg", "w") as f:
        f.write(svg)


# ===================


for i in range(10):
    render_frame(i)
    rate = 1
    for f in features:
        f.reset_force()
    for c in constraints:
        c.compute_force()
    for f in features:
        f.apply_force(rate)
