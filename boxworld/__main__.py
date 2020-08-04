import os
import json
import argparse

from world import World

def generate_demo(flags):
    """Generates demonstration examples."""
    print("Generating demo...")
    demo_worlds_file = flags["demo_worlds_file"]
    with open(demo_worlds_file) as f:
        demo_worlds = json.load(f)
    print(demo_worlds)
    
    # Generate random worlds. 
    for world_name in demo_worlds:
        world_params = demo_worlds[world_name]
        for i in range(flags["max_per_world_type"]):
            random_world = World(aisles=None)
            random_world.initialize(num_aisles=flags["num_aisles"],        
                                    aisle_size=world_params['aisle_size'], num_shelves_per_aisle=world_params['num_shelves_per_aisle'],
                                    box_sizes=world_params['box_sizes'],
                                    box_size_classes=world_params['box_size_classes'],
                                    num_box_per_aisles=world_params['num_box_per_aisles'],
                                    spacings=world_params['spacings'],
                                    deterministic_aisles=[])
        output_fn = os.path.join(flags["output_directory"], f"world_example_{world_name}_{i}.json")
        with open(output_fn, "w") as f:
            json.dump(random_world.to_representation(), f)
        
    
    # "big_small_cluttered" : {
    #     "box_sizes" : [((1, 0.5), (1, 0.5)), ((3, 0.1), (3, 0.1))],
    #     "box_size_classes" : [0.5, 0.5],
    #     "num_box_per_aisles" : (6, 1),
    #     "spacings" : (1, 0.5),
    # },
    #   "big_small_far" : {
    #     "box_sizes" :[((1, 0.5), (1, 0.5)), ((3, 0.1), (3, 0.1))],
    #     "box_size_classes":[0.7, 0.3],
    #     "num_box_per_aisles" : (3, 1),
    #     "spacings" : (3, 2),
    # },
    # 
    # "normal" : {
    #     "box_sizes" : [(2, 1)],
    #     "box_size_classes" : [1.0],
    #     "num_box_per_aisles" : (5, 1),
    #     "spacings" : (2, 1),
    # },
    # 
    # "mostly_small" : {
    #     "box_sizes" : [(1, 0.1)],
    #     "box_size_classes" :  [1.0],
    #     "num_box_per_aisles" : (5, 1),
    #     "spacings" : (2, 1),
    # },
    # 
    # "mostly_big" : {
    #     "box_sizes" : [((3.5, 0.1)],
    #     "box_size_classes" : [1.0],
    #     "num_box_per_aisles" : (5, 1),
    #     "spacings" : (2, 1),
    # }
    

def main():
    parser = argparse.ArgumentParser(description="Boxworld")
    # General arguments.
    parser.add_argument('--output_directory', type=str, default='boxworld/data/demo', help="Path to a folder in which all outputs should be stored.")
    
    # Dataset arguments.
    parser.add_argument('--demo_worlds_file', type=str, default='boxworld/data/demo_world_types.json', help="Path to a JSON file containing parameters for demo world parameters.")
    parser.add_argument("--num_aisles", type=int,
    default=10, help="Number of aisles in the world.")
    parser.add_argument("--max_per_world_type", type=int,
    default=1, help="Maximum number of examples to sample per world type.")
    flags = vars(parser.parse_args())
    
    generate_demo(flags)

if __name__ == "__main__":
    main()