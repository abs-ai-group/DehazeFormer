import os
import shutil
import subprocess
from pathlib import Path


def move_images_and_remove_directory(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate through files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the file is an image file (you can adjust this condition according to your requirements)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Construct the absolute paths for source and destination files
            source_file = os.path.join(source_dir, filename)
            destination_file = os.path.join(destination_dir, filename)
            # Move the image file to the destination directory
            shutil.move(source_file, destination_file)
    # After moving all image files, remove the source directory
    shutil.rmtree(source_dir)


def execute_python_file(*args):
    command = ['python', "test.py"] + list(*args)
    subprocess.run(command)


def create_symlink(original_path, symlink_path):
    try:
        if os.path.islink(symlink_path):
            os.remove(symlink_path)
        # Creating symbolic link
        os.symlink(original_path, symlink_path)
        print(f"Symbolic link created at: {symlink_path}")
    except:
        print(f"Failed to create symbolic link")


def write_file_names_to_txt():
    with open('data/test/test/hazy/test1.txt', 'w') as f:
        for file_name in os.listdir("data/test/test/hazy"):
            f.write(file_name + '\n')


def process_dataset(dataset_path):
    os.makedirs("data/test/test", exist_ok=True)
    create_symlink("hazy", "data/test/test/GT")
    for split in ["train", "val", "test"]:
        split_path = os.path.join(dataset_path, split)
        image_path = os.path.join(split_path, 'images')
        os.makedirs(image_path.replace("Fisheye_contrast", "Fisheye_dehaze"), exist_ok=True)
        create_symlink(image_path, "data/test/test/hazy")
        write_file_names_to_txt()
        execute_python_file(["--model", "dehazeformer-b", "--dataset", "test", "--exp", "outdoor"])
        source_directory = "results/test/dehazeformer-b/imgs"
        destination_directory = Path(str(image_path).replace("Fisheye_contrast", "Fisheye_dehaze"))
        move_images_and_remove_directory(source_directory, destination_directory)


if __name__ == "__main__":
    process_dataset("/srv/aic/Fisheye_contrast")
