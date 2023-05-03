# Make a function merging file numberings
# ex./chim-essay/chim-essay-0.wav , /chim-AI/chim-AI-0.wav -> /chims/chim-0.wav, /chims/chim-1.wav
import os

def merge_file_numberings(source_dirs, output_dir):
    """
    Merges file numberings of multiple source directories into a single output directory.
    
    Args:
        source_dirs (list): A list of strings representing the source directories.
        output_dir (str): A string representing the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for source_dir in source_dirs:
        files = os.listdir(source_dir)
        for i, file in enumerate(files):
            if file.endswith('.wav'):
                new_filename = f"chim-{i}.wav"
                output_path = os.path.join(output_dir, new_filename)
                input_path = os.path.join(source_dir, file)
                os.rename(input_path, output_path)