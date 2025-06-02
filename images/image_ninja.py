import os
from PIL import Image

def create_thumbnail(image_path, thumb_path, max_size=300):
    """Generate a thumbnail with max dimension of 300px, preserving aspect ratio."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            # Convert to RGB if necessary (e.g., for PNG with transparency or RGBA)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(thumb_path, 'JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return False

def get_image_info():
    """Scan current directory for images, generate thumbnails, and collect metadata."""
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    image_data = []

    # Use current directory
    directory = '.'
    if not os.path.exists(directory):
        print(f"Current directory does not exist.")
        return image_data

    for filename in os.listdir(directory):
        if filename.lower().endswith(image_extensions):
            filepath = os.path.join(directory, filename)
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                    # Generate thumbnail filename (always jpg for consistency)
                    thumb_filename = f"{os.path.splitext(filename)[0]}_thumb.jpg"
                    thumb_path = os.path.join(directory, thumb_filename)
                    # Create thumbnail if it doesn't exist
                    if not os.path.exists(thumb_path):
                        if not create_thumbnail(filepath, thumb_path):
                            continue  # Skip if thumbnail creation fails
                    # Assign a default tag
                    tag = "art"
                    image_data.append({
                        'filename': filename,
                        'thumb_filename': thumb_filename,
                        'width': width,
                        'height': height,
                        'tag': tag,
                        'alt': f"{os.path.splitext(filename)[0]} artwork"
                    })
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    return image_data

def generate_html_grid(image_data):
    """Generate HTML grid items from image data with /images/ URLs."""
    html_output = ""
    for img in image_data:
        html_output += f"""        <div class="grid-item" data-tags="{img['tag']}">
            <a href="/images/{img['filename']}" data-pswp-width="{img['width']}" data-pswp-height="{img['height']}">
                <img src="/images/{img['thumb_filename']}" alt="{img['alt']}">
            </a>
        </div>\n"""
    return html_output

def main():
    """Main function to run the script in the current directory."""
    image_data = get_image_info()
    if image_data:
        html_grid = generate_html_grid(image_data)
        print(html_grid)
    else:
        print("No images found or an error occurred.")

if __name__ == "__main__":
    main()