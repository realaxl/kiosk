from flask import Flask, render_template, send_from_directory
import sqlite3
from pathlib import Path
from PIL import Image
import os

app = Flask(__name__, template_folder='../templates')

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect('../db/db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def generate_thumbnail(image_path, cache_path, max_size=1024):
    """Generate a thumbnail with max dimensions of 1024x1024 while keeping proportions"""
    try:
        # Open the original image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for PNG with transparency, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            
            # Calculate new dimensions while maintaining aspect ratio
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Save the thumbnail
            img.save(cache_path, 'JPEG', quality=85, optimize=True)
            return True
    except Exception as e:
        print(f"Error generating thumbnail for {image_path}: {e}")
        return False

@app.route('/')
def index():
    """Main page showing all products"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE active = 1').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve cached thumbnail or generate it if it doesn't exist"""
    # Define paths
    images_dir = Path('../images')
    original_path = images_dir / filename
    cache_dir = images_dir / 'cache'
    
    # Create cache filename (change extension to .jpg)
    cache_filename = Path(filename).stem + '.jpg'
    cache_path = cache_dir / cache_filename
    
    # Check if images directory exists
    if not images_dir.exists():
        return "Images directory not found", 404
    
    # Check if original image exists
    if not original_path.exists():
        return "Image not found", 404
    
    # Check if cached thumbnail exists
    if not cache_path.exists():
        # Generate thumbnail
        cache_dir.mkdir(parents=True, exist_ok=True)
        if not generate_thumbnail(original_path, cache_path):
            # If thumbnail generation fails, serve original
            return send_from_directory(str(images_dir), filename)
    
    # Serve the cached thumbnail
    return send_from_directory(str(cache_dir), cache_filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob