import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Boxworld")
    # General arguments.
    parser.add_argument('--output_directory', type=str, default='output', help="Path to a folder in which all outputs should be stored.")
    # Dataset arguments.
    
    # World arguments.
    parser.add_argument('--')
    flags = vars(parser.parse_args())
    
    

if __name__ == "__main__":
    main()