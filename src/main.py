import app
import os

# a function returning all paths of wav extension file inside of input directory
def get_all_file_paths(input_dir):
    file_paths = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".wav"):
                file_paths.append(os.path.join(root, file))
    return file_paths


if __name__ == "__main__":
    
    # source_dirs = ["/voices/chim-essay", "/voices/chim-AI", "/voices/chim-food", "/voices/chim-horror", "/voices/chim-news"]    
    # output_dir = "/voices/chims"

    # rename.merge_file_numberings(source_dirs, output_dir)

    paths = get_all_file_paths("voices")
    idx = 0
    for path in paths:
        idx = app.make_voice_segments(idx, path)
    
