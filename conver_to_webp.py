from PIL import Image

def convert_gif_to_webp(gif_file_path, output_file_path):
    # Open the GIF file
    with Image.open(gif_file_path) as im:
        # Get the duration of each frame
        durations = []
        try:
            while True:
                durations.append(im.info['duration'])
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        
        # Convert each frame to WebP format
        frames = []
        try:
            while True:
                frames.append(im.copy())
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        
        # Save frames as WebP with the corresponding durations
        im.save(output_file_path, lossless=False,method=5, quality=85, save_all=True, format='webp')
        
        print(f"Conversion completed. WebP file saved at {output_file_path}")

# Usage example
gif_file_path = 'input.gif'
output_file_path = 'converted_output.webp'
convert_gif_to_webp(gif_file_path, output_file_path) 