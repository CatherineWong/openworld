import numpy as np

MIN_BOX_SIZE = 0.1

# Utility functions for sampling distributions.
def sample_categorical(rng, params):
    pvals = np.array(params)
    pvals = pvals / np.sum(pvals)
    draw_array = rng.multinomial(n=1, pvals=pvals)
    return np.argmax(draw_array)

def sample_normal(rng, params):
    return rng.normal(loc=params[0], scale=params[1])
    
class Box(object):
    def __init__(self, id, pos, width, height):
        self.id = id
        self.pos = pos # Pos is in (shelf_id, x_distance on shelf)
        self.width = width
        self.height = height
        
    def to_representation(self):
        return {
            "id" : int(self.id),
            "pos": (int(self.pos[0]), float(self.pos[1])),
            "width" : float(self.width),
            "height" : float(self.height)
        }
        
class Aisle(object):
    def __init__(self, id, size, num_shelves, boxes):
        self.id = id
        self.size = size
        self.num_shelves = num_shelves
        self.boxes = boxes
    
    def to_representation(self):
        return {
            "id" : self.id,
            "size" : self.size,
            "num_shelves" : self.num_shelves,
            "boxes" : [box.to_representation() for box in self.boxes]
        }

class World(object):
    def __init__(self, aisles):
        self.aisles = aisles
    
    def to_representation(self):
        return {
            "num_aisles" : len(self.aisles),
            "aisle_size" : self.aisles[0].size,
            "num_shelves_per_aisle" : self.aisles[0].num_shelves,
            "aisles" : [aisle.to_representation() for aisle in self.aisles]
        }
    
    def initialize(self, num_aisles, aisle_size, num_shelves_per_aisle,
                    box_sizes,
                    box_size_classes,
                    num_box_per_aisles,
                    spacings,
                    deterministic_aisles):
        """Create a stockroom by placing any deterministic (handcrafted) aisles at the target locations and then randomly generating the remaining aisles by sampling boxes.
        Box sizes: List of n [(width_mean, width_sigma), (height_mean, height_sigma)]
        Box size classes: List of n weights over the box types, which defines a categorical.
        """
        rng = np.random.default_rng()
        num_aisles_to_generate = num_aisles - len(deterministic_aisles)
        shelf_height = int(aisle_size / num_shelves_per_aisle)
        generated_aisles = []
        for _aisle in range(num_aisles_to_generate):
            aisle = Aisle(id=None, size=aisle_size, num_shelves=num_shelves_per_aisle, boxes=[])
            remaining_shelf_space = [aisle_size for _ in range(num_shelves_per_aisle)]
            max_num_boxes = int(sample_normal(rng, params=num_box_per_aisles))
            boxes = [] 
            for _box in range(max_num_boxes):
                # Generate a box.
                box_size_class = sample_categorical(rng, params=box_size_classes)
                box_width = sample_normal(rng, params=box_sizes[box_size_class][0])
                box_height = sample_normal(rng, params=box_sizes[box_size_class][1])
                
                if ((box_width < MIN_BOX_SIZE) or (box_height < MIN_BOX_SIZE)): continue
                
                # Choose a spacing, then place the box.
                box_spacing = sample_normal(rng, params=spacings)
                free_shelves = [shelf for shelf in range(num_shelves_per_aisle) if remaining_shelf_space[shelf] >= (box_width + box_spacing)]
                if len(free_shelves) < 1: continue
                shelf = np.random.choice(free_shelves, 1)[0]
                box_x = (aisle_size - remaining_shelf_space[shelf]) + box_spacing
                box_pos = (shelf, box_x)
                boxes += [Box(id=None, pos=box_pos, width=box_width, height=box_height)]
                remaining_shelf_space[shelf] -= (box_spacing + box_width)
            aisle.boxes = boxes
            generated_aisles += [aisle]
        # Add in all of the handcrafted aisles
        box_id = 0
        for aisle in deterministic_aisles:
            generated_aisles.insert(aisle.id, aisle)
        for id, aisle in enumerate(generated_aisles):
            aisle.id = id
            aisle.boxes = sorted(aisle.boxes, key=lambda b: b.pos[0])
            for box in aisle.boxes:
                box.id = box_id
                box_id += 1
        self.aisles = generated_aisles

if __name__ == "__main__":
    aisles = []
    for aisle_id in range(2):
        aisle = Aisle(id=aisle_id, size=12, num_shelves=3, boxes=[])
        for id in range(3):
            box = Box(id=id, pos=(id, id+1), width=aisle_id+3, height=id + 0.5)
            aisle.boxes += [box]
        aisles += [aisle]
    
    # Generate a random world.
    random_world = World(aisles=None)
    random_world.initialize(num_aisles=3, aisle_size=12, num_shelves_per_aisle=3,
                            box_sizes=[((1, 0.1), (1, 0.1)), ((3, 0.1), (3, 0.1))],
                            box_size_classes=[0.7, 0.3],
                            num_box_per_aisles=(2,1),
                            spacings=(2, 1),
                            deterministic_aisles=aisles)
    print(random_world.to_representation())
    
    # Write out a random world.
    import json
    with open("data/demo/world_example_1.js", "w") as f:
        json.dump(random_world.to_representation(), f)