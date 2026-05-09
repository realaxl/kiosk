from flask import Flask, render_template, send_from_directory
import sqlite3
from pathlib import Path
from PIL import Image
import os

app = Flask(__name__, template_folder='../templates')

# Get the project root directory (parent of src directory)
PROJECT_ROOT = Path(__file__).parent.parent

def get_db_connection():
    """Create a database connection"""
    db_path = PROJECT_ROOT / 'db' / 'db.sqlite'
    conn = sqlite3.connect(str(db_path))
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
    """Serve cached thumbnail, generate if it doesn't exist, then always serve from cache"""
    # Define paths using project root
    images_dir = PROJECT_ROOT / 'images'
    cache_dir = images_dir / 'cache'
    
    # Determine cache filename: PNG files are converted to JPG in cache
    file_ext = Path(filename).suffix.lower()
    if file_ext == '.png':
        cache_filename = Path(filename).stem + '.jpg'
    else:
        cache_filename = filename
    
    cache_path = cache_dir / cache_filename
    
    print(f"[IMAGE REQUEST] Requested: {filename}")
    
    # Check if cache directory exists
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True, exist_ok=True)
    
    # If cached thumbnail doesn't exist, generate it
    if not cache_path.exists():
        original_path = images_dir / filename
        
        # Check if original image exists
        if not original_path.exists():
            return f"Original image not found: {filename}", 404
        
        # Generate thumbnail
        if not generate_thumbnail(original_path, cache_path):
            return "Failed to generate thumbnail", 500
    
    # Always serve from cache directory (never the original)
    return send_from_directory(str(cache_dir), cache_filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob