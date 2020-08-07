import os
import json
import numpy as np
from world import Situation, World, Aisle, Box
from helpers import sample_normal, sample_categorical, clamp_min_max

def build_default_situation(aisles, instruction):
    # Utility function to generate box IDs 
    box_id = 0
    target = None
    for aisle in aisles:
        for box in aisle.boxes:
            if box.id == "target":
                target = box_id
            box.id = box_id
            box_id += 1
    situation = Situation(world=World(aisles), location=0, instruction=instruction, target=target, meaning=None)
    situation_name = "_".join(instruction.split())
    return situation_name, situation

def generate_many_boxes(shelf_size, shelf_height, shelf_id, box_sizes, num_boxes, min_spacing, max_spacing, starting_spacing):
    boxes = []
    current_spacing = starting_spacing
    rng = np.random.default_rng()
    for _ in range(num_boxes):
        box_type = sample_categorical(rng, [1] * len(box_sizes))
        box  = Box.initialize_random(id=None, pos=(shelf_id, current_spacing),
                widths=box_sizes[box_type][0], heights=box_sizes[box_type][1])
        if (current_spacing + box.width) >= shelf_size: break
        boxes.append(box)
        
        spacing = sample_normal(rng, ((max_spacing - min_spacing) * 0.5, 0.1))
        spacing = clamp_min_max(spacing, min_spacing, max_spacing)
        current_spacing += (box.width + spacing)
    return boxes
    
def generate_demo(flags):
    """Generates demonstration dataset."""
    print("Generating demo...")
    
    situations = []
    situation_id = 0
    num_aisles = 6
    aisle_size = 16
    num_shelves = 4
    shelf_height = aisle_size / num_shelves
    # Tall box that's far from a little box.
    instruction = "a tall box far from a little box"
    tall_sizes = [[shelf_height * 0.33, 0.1], [shelf_height * 0.9, 0.5]]
    big_sizes = [[shelf_height * 0.8, 0.1], [shelf_height * 0.7, 0.1]]
    medium_sizes = [[shelf_height * 0.7, 0.1], [shelf_height * 0.5, 0.1]]
    little_sizes = [[shelf_height * 0.3, 0.2], [shelf_height * 0.15, 0.2]]
    aisles = []
    for aisle_id in range(num_aisles):
        boxes = []
        if aisle_id == 0:
            boxes = [Box.initialize_random(id=None, pos=(0, 1), widths=tall_sizes[0], heights=tall_sizes[1]),
            Box.initialize_random(id=None, pos=(1, 10), widths=medium_sizes[0], heights=medium_sizes[1]),
            Box.initialize_random(id=None, pos=(2, 2), widths=big_sizes[0], heights=big_sizes[1]),
            Box.initialize_random(id=None, pos=(2, 7), widths=medium_sizes[0], heights=medium_sizes[1]),
            Box.initialize_random(id=None, pos=(3, 3), widths=little_sizes[0], heights=little_sizes[1]),
            Box.initialize_random(id=None, pos=(3, 7), widths=little_sizes[0], heights=little_sizes[1]),
            Box.initialize_random(id=None, pos=(3, 11), widths=little_sizes[0], heights=little_sizes[1]),
            ]
        elif aisle_id == 1:
            boxes = [Box.initialize_random(id=None, pos=(0, 4), widths=tall_sizes[0], heights=tall_sizes[1]),
            Box.initialize_random(id=None, pos=(1, 8), widths=medium_sizes[0], heights=medium_sizes[1]),
            Box.initialize_random(id=None, pos=(2, 2), widths=big_sizes[0], heights=big_sizes[1]),
            Box.initialize_random(id=None, pos=(2, 7), widths=medium_sizes[0], heights=medium_sizes[1]),
            Box.initialize_random(id=None, pos=(3, 5), widths=little_sizes[0], heights=little_sizes[1]),]
        elif aisle_id == 2:
            boxes = [Box.initialize_random(id=None, pos=(1, 0.5), widths=tall_sizes[0], heights=tall_sizes[1]),
            Box.initialize_random(id=None, pos=(1, 4), widths=little_sizes[0], heights=little_sizes[1]),
            Box.initialize_random(id=None, pos=(2, 5), widths=big_sizes[0], heights=big_sizes[1]),
            Box.initialize_random(id=None, pos=(2, 10), widths=medium_sizes[0], heights=medium_sizes[1]),
            Box.initialize_random(id=None, pos=(3, 12), widths=medium_sizes[0], heights=medium_sizes[1]),
            ]
        elif aisle_id == 3:
            boxes = [
                Box.initialize_random(id="target", pos=(1, 0.2), widths=tall_sizes[0], heights=tall_sizes[1]),
                Box.initialize_random(id=None, pos=(1, 12), widths=little_sizes[0], heights=little_sizes[1]),
                Box.initialize_random(id=None, pos=(3, 9), widths=big_sizes[0], heights=big_sizes[1]),
                Box.initialize_random(id=None, pos=(3, 13), widths=medium_sizes[0], heights=medium_sizes[1]),
            ]
        elif aisle_id == 4:
            boxes = [
                Box.initialize_random(id=None, pos=(0, 6), widths=tall_sizes[0], heights=tall_sizes[1]),
                Box.initialize_random(id=None, pos=(1, 3), widths=big_sizes[0], heights=big_sizes[1]),
                Box.initialize_random(id=None, pos=(1, 9), widths=little_sizes[0], heights=little_sizes[1]),
                Box.initialize_random(id=None, pos=(2, 7), widths=medium_sizes[0], heights=medium_sizes[1]),
                Box.initialize_random(id=None, pos=(3, 5), widths=little_sizes[0], heights=little_sizes[1]),
                Box.initialize_random(id=None, pos=(3, 8), widths=little_sizes[0], heights=little_sizes[1]),
            ]
        elif aisle_id == 5:
            boxes = [
                Box.initialize_random(id=None, pos=(1, 3), widths=medium_sizes[0], heights=medium_sizes[1]),
                Box.initialize_random(id=None, pos=(1, 12), widths=little_sizes[0], heights=little_sizes[1]),
                Box.initialize_random(id=None, pos=(2, 1), widths=big_sizes[0], heights=big_sizes[1]),
                Box.initialize_random(id=None, pos=(2, 8), widths=big_sizes[0], heights=big_sizes[1]),
                
                Box.initialize_random(id=None, pos=(3, 5), widths=medium_sizes[0], heights=medium_sizes[1]),
                Box.initialize_random(id=None, pos=(3, 11), widths=little_sizes[0], heights=little_sizes[1]),
            ]
            
        aisles.append(Aisle(id=aisle_id, size=aisle_size, num_shelves=num_shelves, boxes=boxes))
    situation_name, situation = build_default_situation(aisles, instruction)
    problem_name = f"demo_{situation_name}_{situation_id}_0.json"
    situations.append((problem_name, situation))
    
    # Tall box that's far from a little box.
    instruction = "a tall box far from a little box"
    tall_sizes = [[shelf_height * 0.2, 0.1], [shelf_height * 0.95, 0.5]]
    big_sizes = [[shelf_height * 0.9, 0.1], [shelf_height * 0.6, 0.1]]
    little_sizes = [[shelf_height * 0.4, 0.2], [shelf_height * 0.2, 0.2]]
    aisles = []
    for aisle_id in range(num_aisles):
        boxes = []
        if aisle_id == 0:
            boxes += generate_many_boxes(aisle_size, shelf_height, 0, [tall_sizes], num_boxes=6, min_spacing=0.5, max_spacing=1, starting_spacing=2)
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [little_sizes], num_boxes=5, min_spacing=0.7, max_spacing=1, starting_spacing=1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [little_sizes, big_sizes], num_boxes=3, min_spacing=0.5, max_spacing=1, starting_spacing=0.5)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes], num_boxes=3, min_spacing=1, max_spacing=1.5, starting_spacing=5)
        if aisle_id == 1:
            boxes += generate_many_boxes(aisle_size, shelf_height, 0, [tall_sizes, little_sizes, big_sizes], num_boxes=4, min_spacing=0.5, max_spacing=1, starting_spacing=1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [little_sizes, big_sizes], num_boxes=4, min_spacing=0.7, max_spacing=1, starting_spacing=0.1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [little_sizes, big_sizes, tall_sizes], num_boxes=6, min_spacing=0.5, max_spacing=1, starting_spacing=0.5)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes], num_boxes=2, min_spacing=5, max_spacing=7, starting_spacing=3)
        if aisle_id == 2:
            boxes += generate_many_boxes(aisle_size, shelf_height, 0, [tall_sizes, little_sizes, big_sizes], num_boxes=4, min_spacing=1, max_spacing=1.5, starting_spacing=2)
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [little_sizes, big_sizes], num_boxes=3, min_spacing=0.7, max_spacing=1, starting_spacing=4)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [ big_sizes], num_boxes=2, min_spacing=1, max_spacing=2, starting_spacing=5)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes, big_sizes, tall_sizes], num_boxes=4, min_spacing=1, max_spacing=1.5, starting_spacing=1)
        if aisle_id == 3:
            boxes += generate_many_boxes(aisle_size, shelf_height, 0, [tall_sizes, little_sizes], num_boxes=4, min_spacing=0.5, max_spacing=1, starting_spacing=8)
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [little_sizes, big_sizes], num_boxes=3, min_spacing=3, max_spacing=5, starting_spacing=1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [ big_sizes, tall_sizes], num_boxes=5, min_spacing=1, max_spacing=1.2, starting_spacing=0.5)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes, tall_sizes], num_boxes=3, min_spacing=0.5, max_spacing=1, starting_spacing=10)
        if aisle_id == 4:
            boxes = [Box.initialize_random(id="target", pos=(0, 0.3), widths=tall_sizes[0], heights=tall_sizes[1]),
            Box.initialize_random(id=None, pos=(0, 8), widths=little_sizes[0], heights=little_sizes[1]),]
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [tall_sizes], num_boxes=9, min_spacing=0.5, max_spacing=1, starting_spacing=1.5)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [ big_sizes, tall_sizes, little_sizes], num_boxes=6, min_spacing=0.8, max_spacing=1.5, starting_spacing=0.9)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes, tall_sizes], num_boxes=8, min_spacing=0.5, max_spacing=1.5, starting_spacing=0.8)
        if aisle_id == 5:
            boxes += generate_many_boxes(aisle_size, shelf_height, 0, [big_sizes, little_sizes], num_boxes=4, min_spacing=0.5, max_spacing=1, starting_spacing=8)
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [little_sizes, big_sizes], num_boxes=3, min_spacing=3, max_spacing=5, starting_spacing=1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [ big_sizes, tall_sizes], num_boxes=5, min_spacing=1, max_spacing=1.2, starting_spacing=0.5)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes, tall_sizes], num_boxes=3, min_spacing=0.5, max_spacing=1, starting_spacing=10)
        
        aisles.append(Aisle(id=aisle_id, size=aisle_size, num_shelves=num_shelves, boxes=boxes))
    situation_name, situation = build_default_situation(aisles, instruction)
    problem_name = f"demo_{situation_name}_{situation_id}_1.json"
    situations.append((problem_name, situation))
    
    # Tall box that's far from a little box.
    instruction = "a tall box far from a little box"
    tall_sizes = [[shelf_height * 0.2, 0.1], [shelf_height * 0.7, 0.3]]
    big_sizes = [[shelf_height * 0.7, 0.1], [shelf_height * 0.5, 0.1]]
    little_sizes = [[shelf_height * 0.35, 0.2], [shelf_height * 0.4, 0.2]]
    aisles = []
    for aisle_id in range(num_aisles):
        boxes = []
        if aisle_id == 0:
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [big_sizes], num_boxes=1, min_spacing=0.5, max_spacing=1, starting_spacing=7)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes], num_boxes=3, min_spacing=0.7, max_spacing=1, starting_spacing=4)
        if aisle_id == 1:
            boxes += generate_many_boxes(aisle_size, shelf_height, 0, [little_sizes], num_boxes=3, min_spacing=1, max_spacing=1.5, starting_spacing=1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [ big_sizes], num_boxes=1, min_spacing=5, max_spacing=1, starting_spacing=0.1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes], num_boxes=1, min_spacing=10, max_spacing=11, starting_spacing=10)
        if aisle_id == 2:
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [little_sizes], num_boxes=2, min_spacing=1, max_spacing=1.5, starting_spacing=1)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [little_sizes, big_sizes], num_boxes=2, min_spacing=0.7, max_spacing=1, starting_spacing=4)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [ little_sizes], num_boxes=2, min_spacing=1, max_spacing=2, starting_spacing=10)
        if aisle_id == 3:
            boxes = [Box.initialize_random(id="target", pos=(1, 10), widths=tall_sizes[0], heights=tall_sizes[1]),
            Box.initialize_random(id=None, pos=(3, 8), widths=little_sizes[0], heights=little_sizes[1]),]
            boxes += generate_many_boxes(aisle_size, shelf_height, 0, [big_sizes], num_boxes=2, min_spacing=0.5, max_spacing=1, starting_spacing=0.5)
        if aisle_id == 4:
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [little_sizes], num_boxes=2, min_spacing=0.5, max_spacing=1, starting_spacing=0.5)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [  tall_sizes, little_sizes], num_boxes=2, min_spacing=2, max_spacing=3, starting_spacing=0.9)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes], num_boxes=1, min_spacing=0.5, max_spacing=1.5, starting_spacing=11)
        if aisle_id == 5:
            boxes += generate_many_boxes(aisle_size, shelf_height, 1, [big_sizes, little_sizes], num_boxes=2, min_spacing=5, max_spacing=6, starting_spacing=4)
            boxes += generate_many_boxes(aisle_size, shelf_height, 2, [big_sizes, little_sizes], num_boxes=2, min_spacing=2, max_spacing=3, starting_spacing=0.9)
            boxes += generate_many_boxes(aisle_size, shelf_height, 3, [little_sizes], num_boxes=1, min_spacing=0.5, max_spacing=1.5, starting_spacing=11)
        
        aisles.append(Aisle(id=aisle_id, size=aisle_size, num_shelves=num_shelves, boxes=boxes))
    situation_name, situation = build_default_situation(aisles, instruction)
    problem_name = f"demo_{situation_name}_{situation_id}_2.json"
    situations.append((problem_name, situation))
    
    
    for situation_name, situation in situations:
        filename = os.path.join(flags["output_directory"], situation_name)
        with open(filename, "w") as f:
            json.dump(situation.to_representation(), f)
