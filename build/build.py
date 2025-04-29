import subprocess
import os

dir = os.path.dirname(os.path.abspath(__file__))
dir = os.path.dirname(dir)
print("Workspace: "+dir)
out = os.path.join(dir, "out\\script.lua")
print("Output: "+out)
src = os.path.join(dir, "src\\CompilerTest\\Main\\main.lua")
print("Source: "+src)
config = os.path.join(dir, "config\\config.lua")
print("Config: "+config)
addon = os.path.join(dir, "src\\CompilerTest\\Main\\Addons")

# Command to execute
command = (
    f"python -m tumfl -d {out} "
    f"{src} "
    f"-c {config}"
)
# Search for Lua scripts in the addon folder
lua_scripts = []

# Function to remove a specific substring from the script paths
def clean_script_path(script_path, to_remove="src/CompilerTest/Main/"):
    cleaned_path = script_path.replace(to_remove, "").replace(".lua", "")
    print(f"Cleaned script path: {cleaned_path}")
    return cleaned_path

# Preserve existing configurations and replace or add the 'addons' table
for root, _, files in os.walk(addon):
    print(f"Scanning directory: {root}")
    for file in files:
        if file.endswith(".lua"):
            relative_path = os.path.relpath(os.path.join(root, file), dir)
            print(f"Found Lua script: {relative_path}")
            relative_path = clean_script_path(relative_path.replace("\\", "/"))
            lua_scripts.append(relative_path)
            print(f"Added script to list: {relative_path}")

# Read the existing config file
print(f"Reading config file: {config}")
with open(config, "r") as config_file:
    lines = config_file.readlines()

# Write back the config file, always overwriting the 'addons' table
print(f"Writing updated config file: {config}")
with open(config, "w") as config_file:
    for line in lines:
        if not line.strip().startswith("addons = {"):
            config_file.write(line)
        else:
            print(f"Skipping existing 'addons' line: {line.strip()}")

    # Check if 'addons' table exists in the config file
    addons_found = any("addons =" in line for line in lines)
    addons_line_index = next((i for i, line in enumerate(lines) if "addons =" in line), None)
    if addons_line_index is not None and addons_line_index + 1 < len(lines):
        next_line = lines[addons_line_index + 1].strip()
        if next_line:
            print("Overwriting existing 'addons' table.")
            config_file.write("\naddons = {")
            for i, script in enumerate(lua_scripts):
                config_file.write(f'"{script}"')
                if i < len(lua_scripts) - 1:  # Add a comma if it's not the last script
                    config_file.write(",")
            config_file.write("}")
    else:
        if not addons_found:  # If no addon line is found, add it
            print("Adding new 'addons' table.")
            config_file.write("\naddons = {")
        else:
            print("Appending to existing 'addons' table.")
            config_file.write("addons = {")
        for i, script in enumerate(lua_scripts):
            config_file.write(f'"{script}"')
            if i < len(lua_scripts) - 1:  # Add a comma if it's not the last script
                config_file.write(",")
        config_file.write("}")
print("Config file updated successfully.")
try:
    subprocess.run(command, shell=True, check=True)
    print("Command executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"An error occurred while executing the command: {e}")