import sys
import re
from collections import defaultdict
from typing import List, Tuple, Optional
import copy


class Flower:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __hash__(self):
        return (self.size, self.name).__hash__()

    def __eq__(self, other: 'Flower'):
        return other.size == self.size and other.name == self.name

    def __repr__(self):
        return self.name


class BouqetDesign:
    def __init__(self, name, size, flowers, total):
        self.name = name
        self.size = size
        self.flowers = flowers
        self.total = total


class Bouqet:
    def __init__(self, name, size, flowers):
        self.name = name
        self.size = size
        self.flowers = flowers

    def __repr__(self):
        return self.name + self.size + str(self.flowers)


class Flowers:
    def __init__(self, **kwargs):
        self._instances = kwargs.get('flowers', defaultdict(int))

    def __iadd__(self, flower: Flower):
        self._instances[flower] += 1
        return self

    def __getitem__(self, flower: Flower):
        return self._instances[flower]

    def __setitem__(self, key, value):
        self._instances[key] = value

    def total(self, size):
        acc = 0
        for k, v in self._instances.items():
            if k.size == size:
                acc += v
        return acc

    def isEmpty(self):
        return not self._instances

    def __repr__(self):
        return ''.join([str(v) + str(k) for k, v in self._instances.items()])

    def makeBouqet(self, bouqetDesign: BouqetDesign) -> Tuple[Bouqet, 'Flowers']:
        bouqet = Bouqet(name=bouqetDesign.name, size=bouqetDesign.size, flowers=Flowers())
        flowers = copy.deepcopy(self)
        for f, n in bouqetDesign.flowers._instances.items():  # sorry, hurrying
            flowers._instances[f] -= n
            bouqet.flowers._instances[f] += n
        more: int = bouqetDesign.total - bouqetDesign.flowers.total(size=bouqetDesign.size)
        if more:
            for f, n in flowers._instances.items():
                if n == 0 or more == 0 or not f.size == bouqetDesign.size:
                    continue
                if more >= n:
                    bouqet.flowers._instances[f] += flowers._instances[f]
                    flowers._instances[f] = 0
                else:
                    bouqet.flowers._instances[f] = more
                    flowers._instances[f] = flowers._instances[f] - more
        return (bouqet, flowers)


def parse(line):
    if line == "\n":
        return ()
    if line[0].isupper():
        try:
            name = line[0]
            size = line[1]
            m = re.match('^..(.*?)(\d+)$', line)
            total = int(m.group(2))
            flowers = m.group(1)
            flowers = re.split('(\d+)', flowers)[1:]
            flowers = list(zip(map(lambda i: int(i), flowers[::2]), flowers[1::2]))
            flowers = Flowers(flowers=defaultdict(int, {Flower(name=f, size=size): n for n, f in flowers}))
            return BouqetDesign(name=name, size=size, flowers=flowers, total=total)
        except Exception as e:
            raise Exception("parse bouquet design error", e)
    if line[0].islower():
        name = line[0]
        size = line[1]
        return Flower(name=name, size=size)
    else:
        raise Exception("parse error")


def flush(bouqet_designs: BouqetDesign, flowers: Flowers) -> Tuple[Optional[Bouqet], Flowers]:
    make_bouqet = None
    for b in bouqet_designs:
        flag_pass = False
        for f, n in b.flowers._instances.items():  # sorry, hurrying up
            if flowers[f] < n:
                flag_pass = True
                break
        if flag_pass:
            break
        if flowers.total(size=b.size) < b.total:
            break
        make_bouqet = b
    if not make_bouqet:
        return (None, flowers)

    return flowers.makeBouqet(make_bouqet)


def process(stream):
    bouqet_designs: List[BouqetDesign] = []
    flowers_available = Flowers()

    print("Please enter bouquet design first:\n")
    line = stream.readline()
    bouqet1 = parse(line)
    bouqet_designs.append(bouqet1)
    if not isinstance(bouqet1, BouqetDesign):
        raise Exception("1st line is not bouquet design")
    for line in stream:
        entity = parse(line)
        if isinstance(entity, BouqetDesign):
            bouqet_designs.append(entity)
        else:
            if entity is ():
                break
            else:
                raise Exception("wrong input")
    for line in stream:
        entity = parse(line)
        if isinstance(entity, Flower):
            flowers_available += entity
            bouqet_out, flowers_available = flush(bouqet_designs, flowers_available)
            if bouqet_out:
                print(f"out: {bouqet_out}")
        else:
            raise Exception("that`s not a flower")


process(sys.stdin)

# inp = \
#     "AS2a1b3k8\n" \
#     "AL4d1r1t7\n\n" \
#     "aS\n" \
#     "aS\n" \
#     "bS\n" \
#     "kS\n" \
#     "kS\n" \
#     "rL\n" \
#     "kS\n" \
#     "tS\n" \
#     "tS"
#
# import io
#
# stream = io.StringIO(inp)
# process(stream)
