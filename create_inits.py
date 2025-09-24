import os

base_dir = "src"  # or wherever your own code lives
for root, dirs, files in os.walk(base_dir):
    init_path = os.path.join(root, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w"):  # create empty file
            pass