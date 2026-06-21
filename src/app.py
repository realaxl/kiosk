# -*- coding: utf-8 -*-
import sys
import os

# Set environment variable to ensure UTF-8 encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Force UTF-8 encoding for stdout/stderr
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, render_template, send_from_directory, jsonify, request, session, redirect, url_for
import sqlite3
from pathlib import Path
from PIL import Image
import os
import time
import uuid
from dotenv import load_dotenv
from functools import wraps

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Get the project root directory (parent of src directory)
PROJECT_ROOT = Path(__file__).parent.parent

# Configuration from .env
DB_NAME = os.getenv('DB_NAME', 'db.sqlite')
PORT = int(os.getenv('PORT', 5000))
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
EVENT_NAME = os.getenv('EVENT')
FULL_WIDTH = os.getenv('FULL_WIDTH', 'false').lower() in ('true', '1', 'yes')
ALLOW_ADMIN = os.getenv('ALLOW_ADMIN', 'true').lower() in ('true', '1', 'yes')
SLIDESHOW_DELAY = int(os.getenv('SLIDESHOW_DELAY', 7))
SLIDESHOW_ORDER_RANDOM = os.getenv('SLIDESHOW_ORDER_RANDOM', 'false').lower() in ('true', '1', 'yes')

@app.context_processor
def inject_config():
    """Inject configuration variables into all templates"""
    return {
        'full_width': FULL_WIDTH,
        'allow_admin': ALLOW_ADMIN,
        'slideshow_delay': SLIDESHOW_DELAY,
        'slideshow_order_random': SLIDESHOW_ORDER_RANDOM
    }

def get_db_connection():
    """Create a database connection"""
    db_path = PROJECT_ROOT / 'db' / DB_NAME
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def require_admin(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def init_app():
    """Initialize application on startup"""
    print("\n=== Application Initialization ===")
    
    # Check DB_NAME
    if DB_NAME:
        print(f"✓ Database name is set: {DB_NAME}")
    else:
        print("✗ Database name is not set")
    
    # Check ADMIN_PASSWORD
    if ADMIN_PASSWORD:
        print("✓ Admin password is set")
    else:
        print("✗ Admin password is not set")
    
    # Check if database file exists
    db_path = PROJECT_ROOT / 'db' / DB_NAME
    if not db_path.exists():
        print(f"✗ ERROR: Database file not found at {db_path}")
        print("Please run create_database.py first")
        exit(1)
    else:
        print(f"✓ Database file exists at {db_path}")
    
    # Check/Create EVENT if specified
    if EVENT_NAME:
        conn = get_db_connection()
        existing_event = conn.execute(
            'SELECT * FROM events WHERE name = ?', (EVENT_NAME,)
        ).fetchone()
        
        if existing_event:
            print(f"✓ Event already exists: {EVENT_NAME}")
        else:
            # Create new event
            timestamp = int(time.time())
            event_uuid = str(uuid.uuid4())
            conn.execute('''
                INSERT INTO events (uuid, name, timestamp, description, note, active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (event_uuid, EVENT_NAME, timestamp, '', '', 1))
            conn.commit()
            print(f"✓ Created new event: {EVENT_NAME}")
        
        conn.close()
    
    print("=== Initialization Complete ===\n")

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
    
    # Get current event (active event or the one specified in .env)
    current_event = None
    if EVENT_NAME:
        current_event = conn.execute(
            'SELECT * FROM events WHERE name = ? AND active = 1', (EVENT_NAME,)
        ).fetchone()
    
    if not current_event:
        # Get any active event
        current_event = conn.execute(
            'SELECT * FROM events WHERE active = 1 ORDER BY timestamp DESC LIMIT 1'
        ).fetchone()
    
    # Get products that have stock for the current event
    if current_event:
        products = conn.execute('''
            SELECT DISTINCT p.*, s.salePrice as eventSalePrice
            FROM products p
            INNER JOIN stocks s ON p.productId = s.productId
            WHERE p.active = 1
            AND s.eventId = ?
            AND s.active = 1
            AND s.currentNumberInStock > 0
        ''', (current_event['eventId'],)).fetchall()
    else:
        # No event found, show all active products with purchasePrice as fallback
        products = conn.execute('SELECT *, purchasePrice as eventSalePrice FROM products WHERE active = 1').fetchall()
    
    # Get tags and relations for each product
    products_with_tags = []
    for product in products:
        product_dict = dict(product)
        
        # Fetch tags for this product
        tags = conn.execute('''
            SELECT name, value FROM tags
            WHERE productId = ? AND active = 1
        ''', (product['productId'],)).fetchall()
        
        product_dict['tags'] = [dict(tag) for tag in tags]
        
        # Fetch relations for this product (where this product is the source)
        relations = conn.execute('''
            SELECT pr.*, p.name as relatedProductName, p.image as relatedProductImage,
                   s.salePrice as relatedProductPrice
            FROM productRelations pr
            JOIN products p ON pr.toProductId = p.productId
            LEFT JOIN stocks s ON p.productId = s.productId AND s.eventId = ? AND s.active = 1
            WHERE pr.fromProductId = ? AND pr.active = 1 AND p.active = 1
            ORDER BY p.name
        ''', (current_event['eventId'] if current_event else 0, product['productId'])).fetchall()
        
        product_dict['relations'] = [dict(rel) for rel in relations]
        
        # Fetch reverse relations (where this product is the target)
        reverse_relations = conn.execute('''
            SELECT pr.*, p.name as fromProductName, p.image as fromProductImage
            FROM productRelations pr
            JOIN products p ON pr.fromProductId = p.productId
            WHERE pr.toProductId = ? AND pr.active = 1 AND p.active = 1
            ORDER BY p.name
        ''', (product['productId'],)).fetchall()
        
        product_dict['reverseRelations'] = [dict(rel) for rel in reverse_relations]
        products_with_tags.append(product_dict)
        
        # Debug output
        print(f"[DEBUG] Product: {product_dict['name']}")
        print(f"[DEBUG]   productId: {product_dict['productId']}")
        print(f"[DEBUG]   tags: {product_dict['tags']}")
        print(f"[DEBUG]   relations: {len(product_dict['relations'])} relation(s)")
        print(f"[DEBUG]   reverseRelations: {len(product_dict['reverseRelations'])} relation(s)")
    
    conn.close()
    
    # Pass event name to template
    event_name = dict(current_event)['name'] if current_event else None
    return render_template('index.html', products=products_with_tags, event_name=event_name)

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
    """Get product details by ID with stock and category information for current event"""
    conn = get_db_connection()
    
    # Get current event
    current_event = None
    if EVENT_NAME:
        current_event = conn.execute(
            'SELECT * FROM events WHERE name = ? AND active = 1', (EVENT_NAME,)
        ).fetchone()
    
    if not current_event:
        current_event = conn.execute(
            'SELECT * FROM events WHERE active = 1 ORDER BY timestamp DESC LIMIT 1'
        ).fetchone()
    
    # Get product with category information
    product = conn.execute('''
        SELECT p.*, pc.name as categoryName
        FROM products p
        LEFT JOIN productCategories pc ON p.productCategoryId = pc.productCategoryId
        WHERE p.productId = ?
    ''', (product_id,)).fetchone()
    
    if product is None:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    
    product_dict = dict(product)
    
    # Get stock information for current event
    if current_event:
        stock = conn.execute('''
            SELECT * FROM stocks
            WHERE productId = ? AND eventId = ? AND active = 1
        ''', (product_id, current_event['eventId'])).fetchone()
        
        if stock:
            product_dict['stock'] = dict(stock)
        else:
            product_dict['stock'] = None
    else:
        product_dict['stock'] = None
    
    # Get tags for this product
    tags = conn.execute('''
        SELECT name, value FROM tags
        WHERE productId = ? AND active = 1
    ''', (product_id,)).fetchall()
    
    product_dict['tags'] = [dict(tag) for tag in tags]
    
    # Get relations for this product (where this product is the source)
    relations = conn.execute('''
        SELECT pr.*, p.name as relatedProductName, p.image as relatedProductImage,
               s.salePrice as relatedProductPrice
        FROM productRelations pr
        JOIN products p ON pr.toProductId = p.productId
        LEFT JOIN stocks s ON p.productId = s.productId AND s.eventId = ? AND s.active = 1
        WHERE pr.fromProductId = ? AND pr.active = 1 AND p.active = 1
        ORDER BY p.name
    ''', (current_event['eventId'] if current_event else 0, product_id)).fetchall()
    
    product_dict['relations'] = [dict(rel) for rel in relations]
    
    # Get reverse relations (where this product is the target)
    reverse_relations = conn.execute('''
        SELECT pr.*, p.name as fromProductName, p.image as fromProductImage
        FROM productRelations pr
        JOIN products p ON pr.fromProductId = p.productId
        WHERE pr.toProductId = ? AND pr.active = 1 AND p.active = 1
        ORDER BY p.name
    ''', (product_id,)).fetchall()
    
    product_dict['reverseRelations'] = [dict(rel) for rel in reverse_relations]
    
    conn.close()
    return jsonify(product_dict)

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
                image = ?,
                url = ?,
                manualUrl = ?,
                note = ?,
                active = ?
            WHERE productId = ?
        ''', (
            data.get('name'),
            timestamp,
            purchase_price,
            data.get('description'),
            data.get('image'),
            data.get('url'),
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

# Register admin blueprint
from admin import admin_bp
app.register_blueprint(admin_bp)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if ADMIN_PASSWORD and password == ADMIN_PASSWORD:
            session['admin_authenticated'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid password')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_authenticated', None)
    return redirect(url_for('index'))

@app.route('/admin')
@require_admin
def admin_dashboard():
    """Admin dashboard page"""
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    init_app()
    app.run(debug=True, host='0.0.0.0', port=PORT)

# Made with Bob