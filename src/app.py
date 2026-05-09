from flask import Flask, render_template, send_from_directory, jsonify, request
import sqlite3
from pathlib import Path
from PIL import Image
import os
import time

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

@app.route('/api/product/<int:product_id>')
def get_product(product_id):
    """Get product details by ID"""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE productId = ?', (product_id,)).fetchone()
    conn.close()
    
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(dict(product))

@app.route('/api/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product details"""
    data = request.get_json()
    
    conn = get_db_connection()
    
    # Check if product exists
    product = conn.execute('SELECT * FROM products WHERE productId = ?', (product_id,)).fetchone()
    if product is None:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    
    # Update product
    try:
        # Use current timestamp if not provided
        timestamp = data.get('timestamp', int(time.time()))
        
        # Use 0 as default price if not provided or empty
        purchase_price = data.get('purchasePrice')
        if purchase_price is None or purchase_price == '':
            purchase_price = 0
        else:
            purchase_price = float(purchase_price)
        
        conn.execute('''
            UPDATE products
            SET name = ?,
                timestamp = ?,
                purchasePrice = ?,
                description = ?,
                imageUrl = ?,
                manualUrl = ?,
                note = ?,
                active = ?
            WHERE productId = ?
        ''', (
            data.get('name'),
            timestamp,
            purchase_price,
            data.get('description'),
            data.get('imageUrl'),
            data.get('manualUrl'),
            data.get('note'),
            1 if data.get('active') else 0,
            product_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Product updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob