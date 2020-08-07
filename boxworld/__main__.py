import os
import json
import argparse

import dataset

def main():
    parser = argparse.ArgumentParser(description="Boxworld")
    # General arguments.
    parser.add_argument('--output_directory', type=str, default='boxworld/data/demo_dataset', help="Path to a folder in which all outputs should be stored.")
    
    # Dataset generation arguments.
    parser.add_argument("--num_aisles", type=int,
    default=10, help="Number of aisles in the world.")
    parser.add_argument("--max_per_world_type", type=int,
    default=1, help="Maximum number of examples to sample per world type.")
    parser.add_argument('--world_definitions_file', type=str, help="Path to a JSON file containing parameters for sampling random worlds.")
    
    # Miscellaneous.
    parser.add_argument('--generate_demo', action="store_true", help="Generate a handcrafted demonstration dataset.")
    
    flags = vars(parser.parse_args())
    
    if bool(flags['generate_demo']):
        dataset.generate_demo(flags)
    

if __name__ == "__main__":
    main()