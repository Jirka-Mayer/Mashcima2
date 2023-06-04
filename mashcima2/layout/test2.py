from typing import List, Tuple, Dict, Optional
import random


class FeatureDistribution:
    def sample(self) -> float:
        return 0
    
    def probability(self, value) -> float:
        return 0


class CategoricalDistribution(FeatureDistribution):
    def __init__(self, table: Dict[float, float]):
        self.table = table
    
    def sample(self):
        # TODO: this should NOT be uniform, but for now...
        return random.choice(list(self.table.keys()))
    
    def probability(self, value) -> float:
        if value in self.table:
            return self.table[value]
        else:
            return 0.0


class Feature:
    def __init__(self, label: str, distribution: Optional[FeatureDistribution]):
        self.label = label
        self.value = 0.0
        self.distribution = distribution
        if distribution is not None:
            self.value = distribution.sample()
    
    def probability(self):
        """Probability of this feature value"""
        if self.distribution is None:
            return 1.0
        return self.distribution.probability(self.value)
    
    def __repr__(self):
        return f"Feature[{self.label}] = {self.value:.2f}, prob: {self.probability():.4f}"


class Constraint:
    def __init__(self, label: str, features: List[Feature], weights: List[float]):
        self.label = label
        self.features = features
        self.weights = weights
        assert len(features) == len(weights)

    def error(self):
        e = 0.0
        for i in range(len(self.features)):
            e += self.features[i].value * self.weights[i]
        return e

    def minimize_error(self, learning_rate: float):
        gradient = [
            2 * self.error() * w # TODO: include probability gradient
            for w in self.weights
        ]
        for i in range(len(self.features)):
            f = self.features[i]
            f.value -= gradient[i] * learning_rate
    
    def __repr__(self):
        return f"Constraint[{self.label}], error: {self.error():.2f}"


class Scene:
    def __init__(self):
        self.features: List[Feature] = []
        self.constraints: List[Constraint] = []
    
    def probability(self):
        """Probability of this feature combination"""
        p = 1.0
        for f in self.features:
            p *= f.probability()
        return p
    
    def maximize_probability(self):
        # pick a feature and try to make it more probable (locally)
        f = random.choice(self.features)
        if f.distribution is None:
            return
        d = f.distribution

        best_value = f.value
        best_prob = f.probability()
        for _ in range(10):
            v = d.sample()
            p = d.probability(v)
            if p > best_prob:
                best_value = v
                best_prob = p
        f.value = best_value

    def minimize_error(self, learning_rate=0.01):
        for c in self.constraints:
            c.minimize_error(learning_rate)
    
    def error(self):
        """Total constraints error"""
        e = 0.0
        for c in self.constraints:
            e += c.error() ** 2
        return e
    
    def print(self):
        print("Features")
        for f in self.features:
            print("  ", f)
        print("Constraints")
        for c in self.constraints:
            print("  ", c)
        print("Total probability:", self.probability())
        print("Total error:", self.error())
        print()


# ================================

scene = Scene()

a = Feature("a", CategoricalDistribution({1: 0.5, -1: 0.5}))
b = Feature("b", CategoricalDistribution({1: 0.5, -1: 0.5}))
delta = Feature("delta", CategoricalDistribution({0: 1.0}))
scene.features += [a, b, delta]

scene.constraints.append(Constraint(
    "delta = b - a",
    [delta, b, a],
    [1, -1, 1] # delta - b + a = 0
))

for epoch in range(10):
    print(f"\n#### EPOCH {epoch} ####")
    scene.maximize_probability()
    scene.print()
    
    while abs(scene.error()) > 0.1:
        scene.minimize_error()
        scene.print()

print("\n#### DONE ####")
print()
scene.print()
