import argparse
import json
import os
import shutil

from jinja2 import Environment, FileSystemLoader

def parse_args():
    parser = argparse.ArgumentParser(description="Parse config file and output destination.")
    
    parser.add_argument(
        '--config', 
        type=str, 
        required=True, 
        help='Path to the input configuration file'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        required=True, 
        help='Path to the output destination file or directory'
    )
    
    args = parser.parse_args()
    
    return args

def load_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data
    except FileNotFoundError:
        print(f"Error: The config file '{config_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{config_path}' is not a valid JSON file.")
        return None

def main():
    args = parse_args()
    
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("template.html")
    
    data = load_config(args.config)

    if data:
        output = template.render(data)
        html_output_path = os.path.join(args.output, "index.html")
        css_output_path = os.path.join(args.output, "styles.css")

        #Generate HTML
        with open(html_output_path, "w") as f:
            f.write(output)

        #Copy CSS File 
        css_path = os.path.join("templates/", "styles.css")
        shutil.copy(css_path, css_output_path)

main()