"""
Admin interface module for managing events, products, stocks, and sales
All routes require admin authentication
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import time
from pathlib import Path
from functools import wraps

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

def require_admin(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    """Create a database connection"""
    from app import DB_NAME
    db_path = PROJECT_ROOT / 'db' / DB_NAME
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================================
# EVENTS ROUTES
# ============================================================================

@admin_bp.route('/events')
@require_admin
def events():
    """Events management page"""
    conn = get_db_connection()
    show_all = request.args.get('show_all', 'false') == 'true'
    
    if show_all:
        events = conn.execute('SELECT * FROM events ORDER BY timestamp DESC').fetchall()
    else:
        events = conn.execute('SELECT * FROM events WHERE active = 1 ORDER BY timestamp DESC').fetchall()
    
    conn.close()
    return render_template('admin_events.html', events=events, show_all=show_all)

@admin_bp.route('/api/events', methods=['GET'])
@require_admin
def get_events():
    """Get all events"""
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(event) for event in events])

@admin_bp.route('/api/events/<int:event_id>', methods=['GET'])
@require_admin
def get_event(event_id):
    """Get a single event by ID"""
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE eventId = ?', (event_id,)).fetchone()
    conn.close()
    
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    
    return jsonify(dict(event))

@admin_bp.route('/api/events', methods=['POST'])
@require_admin
def create_event():
    """Create a new event"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('''
            INSERT INTO events (name, timestamp, description, note, active)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('name'),
            data.get('timestamp', int(time.time())),
            data.get('description', ''),
            data.get('note', ''),
            1 if data.get('active', True) else 0
        ))
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'eventId': event_id})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/events/<int:event_id>', methods=['PUT'])
@require_admin
def update_event(event_id):
    """Update an event"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE events
            SET name = ?, timestamp = ?, description = ?, note = ?, active = ?
            WHERE eventId = ?
        ''', (
            data.get('name'),
            data.get('timestamp'),
            data.get('description'),
            data.get('note'),
            1 if data.get('active') else 0,
            event_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/events/<int:event_id>', methods=['DELETE'])
@require_admin
def delete_event(event_id):
    """Delete an event"""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM events WHERE eventId = ?', (event_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PRODUCT CATEGORIES ROUTES
# ============================================================================

@admin_bp.route('/product-categories')
@require_admin
def product_categories():
    """Product categories management page"""
    conn = get_db_connection()
    show_all = request.args.get('show_all', 'false') == 'true'
    
    if show_all:
        categories = conn.execute('SELECT * FROM productCategories ORDER BY name').fetchall()
    else:
        categories = conn.execute('SELECT * FROM productCategories WHERE active = 1 ORDER BY name').fetchall()
    
    conn.close()
    return render_template('admin_product_categories.html', categories=categories, show_all=show_all)

@admin_bp.route('/api/product-categories', methods=['GET'])
@require_admin
def get_product_categories():
    """Get all product categories"""
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM productCategories ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(cat) for cat in categories])

@admin_bp.route('/api/product-categories', methods=['POST'])
@require_admin
def create_product_category():
    """Create a new product category"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('''
            INSERT INTO productCategories (name, description, image, note, active)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('name'),
            data.get('description', ''),
            data.get('image', ''),
            data.get('note', ''),
            1 if data.get('active', True) else 0
        ))
        conn.commit()
        category_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'productCategoryId': category_id})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/product-categories/<int:category_id>', methods=['PUT'])
@require_admin
def update_product_category(category_id):
    """Update a product category"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE productCategories
            SET name = ?, description = ?, image = ?, note = ?, active = ?
            WHERE productCategoryId = ?
        ''', (
            data.get('name'),
            data.get('description'),
            data.get('image'),
            data.get('note'),
            1 if data.get('active') else 0,
            category_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/product-categories/<int:category_id>', methods=['DELETE'])
@require_admin
def delete_product_category(category_id):
    """Delete a product category"""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM productCategories WHERE productCategoryId = ?', (category_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PRODUCTS ROUTES
# ============================================================================

@admin_bp.route('/products')
@require_admin
def products():
    """Products management page"""
    conn = get_db_connection()
    
    # Always fetch all products, let frontend handle filtering
    products = conn.execute('''
        SELECT p.*, pc.name as categoryName
        FROM products p
        LEFT JOIN productCategories pc ON p.productCategoryId = pc.productCategoryId
        ORDER BY p.name
    ''').fetchall()
    
    categories = conn.execute('SELECT * FROM productCategories WHERE active = 1 ORDER BY name').fetchall()
    conn.close()
    return render_template('admin_products.html', products=products, categories=categories)

@admin_bp.route('/api/products/<int:product_id>', methods=['GET'])
@require_admin
def get_product(product_id):
    """Get a single product by ID"""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE productId = ?', (product_id,)).fetchone()
    conn.close()
    
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(dict(product))

@admin_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@require_admin
def update_product(product_id):
    """Update a product"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE products
            SET productCategoryId = ?, name = ?, timestamp = ?, purchasePrice = ?,
                description = ?, image = ?, url = ?, manualUrl = ?, note = ?, active = ?
            WHERE productId = ?
        ''', (
            data.get('productCategoryId'),
            data.get('name'),
            data.get('timestamp', int(time.time())),
            data.get('purchasePrice', 0),
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
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/products', methods=['POST'])
@require_admin
def create_product():
    """Create a new product"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('''
            INSERT INTO products (productCategoryId, name, timestamp, purchasePrice, description, image, url, manualUrl, note, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('productCategoryId'),
            data.get('name'),
            data.get('timestamp', int(time.time())),
            data.get('purchasePrice', 0),
            data.get('description', ''),
            data.get('image', ''),
            data.get('url', ''),
            data.get('manualUrl', ''),
            data.get('note', ''),
            1 if data.get('active', True) else 0
        ))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'productId': product_id})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@require_admin
def delete_product(product_id):
    """Delete a product"""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM products WHERE productId = ?', (product_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# STOCKS ROUTES
# ============================================================================

@admin_bp.route('/stocks')
@require_admin
def stocks():
    """Stock management page"""
    import os
    conn = get_db_connection()
    
    # Get all events
    events = conn.execute('SELECT * FROM events ORDER BY timestamp DESC').fetchall()
    
    # Get all product categories
    categories = conn.execute('SELECT * FROM productCategories ORDER BY name').fetchall()
    
    # Get all products with their category info
    products = conn.execute('''
        SELECT p.*, pc.name as categoryName
        FROM products p
        LEFT JOIN productCategories pc ON p.productCategoryId = pc.productCategoryId
        ORDER BY p.name
    ''').fetchall()
    
    # Get default event from .env
    default_event_name = os.getenv('EVENT', '')
    default_event_id = None
    if default_event_name:
        default_event = conn.execute('SELECT eventId FROM events WHERE name = ?', (default_event_name,)).fetchone()
        if default_event:
            default_event_id = default_event['eventId']
    
    conn.close()
    return render_template('admin_stocks.html',
                         events=events,
                         categories=categories,
                         products=products,
                         default_event_id=default_event_id)

@admin_bp.route('/api/stocks', methods=['GET'])
@require_admin
def get_stocks():
    """Get stocks for a specific event and product"""
    event_id = request.args.get('eventId')
    product_id = request.args.get('productId')
    
    conn = get_db_connection()
    
    if event_id and product_id:
        stocks = conn.execute('''
            SELECT * FROM stocks
            WHERE eventId = ? AND productId = ?
        ''', (event_id, product_id)).fetchall()
    elif event_id:
        stocks = conn.execute('SELECT * FROM stocks WHERE eventId = ?', (event_id,)).fetchall()
    elif product_id:
        stocks = conn.execute('SELECT * FROM stocks WHERE productId = ?', (product_id,)).fetchall()
    else:
        stocks = conn.execute('SELECT * FROM stocks').fetchall()
    
    conn.close()
    return jsonify([dict(stock) for stock in stocks])

@admin_bp.route('/api/stocks', methods=['POST'])
@require_admin
def create_stock():
    """Create a new stock entry"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        # Log the incoming data for debugging
        print(f"Creating stock with data: {data}")
        
        cursor = conn.execute('''
            INSERT INTO stocks (eventId, productId, initialNumberInStock, currentNumberInStock, salePrice, note, favorite, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('eventId'),
            data.get('productId'),
            data.get('initialNumberInStock', 0),
            data.get('currentNumberInStock', 0),
            data.get('salePrice', 0),
            data.get('note', ''),
            0,  # favorite defaults to 0
            1 if data.get('active', True) else 0
        ))
        conn.commit()
        stock_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'stockId': stock_id})
    except Exception as e:
        conn.close()
        print(f"Error creating stock: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/stocks/<int:stock_id>', methods=['PUT'])
@require_admin
def update_stock(stock_id):
    """Update a stock entry"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        print(f"Updating stock {stock_id} with data: {data}")
        
        conn.execute('''
            UPDATE stocks
            SET initialNumberInStock = ?, currentNumberInStock = ?, salePrice = ?, note = ?, favorite = ?, active = ?
            WHERE stockId = ?
        ''', (
            data.get('initialNumberInStock'),
            data.get('currentNumberInStock'),
            data.get('salePrice'),
            data.get('note'),
            1 if data.get('favorite', False) else 0,
            1 if data.get('active') else 0,
            stock_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        print(f"Error updating stock: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/stocks/<int:stock_id>', methods=['DELETE'])
@require_admin
def delete_stock(stock_id):
    """Delete a stock entry"""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM stocks WHERE stockId = ?', (stock_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# SALES ROUTES
# ============================================================================

@admin_bp.route('/sales')
@require_admin
def sales():
    """Sales management page"""
    conn = get_db_connection()
    
    sales = conn.execute('''
        SELECT s.*, st.productId, p.name as productName, e.name as eventName
        FROM sales s
        JOIN stocks st ON s.stockId = st.stockId
        JOIN products p ON st.productId = p.productId
        JOIN events e ON st.eventId = e.eventId
        ORDER BY s.timestamp DESC
    ''').fetchall()
    
    conn.close()
    return render_template('admin_sales.html', sales=sales)

@admin_bp.route('/api/sales', methods=['GET'])
@require_admin
def get_sales():
    """Get all sales"""
    conn = get_db_connection()
    sales = conn.execute('SELECT * FROM sales ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(sale) for sale in sales])

@admin_bp.route('/api/sales', methods=['POST'])
@require_admin
def create_sale():
    """Create a new sale"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('''
            INSERT INTO sales (stockId, numberItemsSold, timestamp, note)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('stockId'),
            data.get('numberItemsSold'),
            data.get('timestamp', int(time.time())),
            data.get('note', '')
        ))
        conn.commit()
        sale_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'saleId': sale_id})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/sales/<int:sale_id>', methods=['PUT'])
@require_admin
def update_sale(sale_id):
    """Update a sale"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE sales
            SET stockId = ?, numberItemsSold = ?, timestamp = ?, note = ?
            WHERE saleId = ?
        ''', (
            data.get('stockId'),
            data.get('numberItemsSold'),
            data.get('timestamp'),
            data.get('note'),
            sale_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@require_admin
def delete_sale(sale_id):
    """Delete a sale"""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM sales WHERE saleId = ?', (sale_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# TAGS ROUTES
# ============================================================================

@admin_bp.route('/tags')
@require_admin
def tags():
    """Tags management page"""
    conn = get_db_connection()
    
    # Get filter parameters
    tag_name_filter = request.args.get('tag_name', 'all')
    show_all = request.args.get('show_all', 'false') == 'true'
    
    # Build query based on filters
    query = '''
        SELECT p.*,
               GROUP_CONCAT(t.tagId || ':' || t.name || ':' || COALESCE(t.value, '') || ':' || t.active, '|') as tags
        FROM products p
        LEFT JOIN tags t ON p.productId = t.productId
    '''
    
    conditions = []
    params = []
    
    # Filter by tag name if not "all"
    if tag_name_filter != 'all':
        conditions.append('t.name = ?')
        params.append(tag_name_filter)
    
    # Filter by active status
    if not show_all:
        conditions.append('(t.active = 1 OR t.tagId IS NULL)')
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' GROUP BY p.productId ORDER BY p.name'
    
    products = conn.execute(query, params).fetchall()
    
    # Get all unique tag names for the filter dropdown
    tag_names = conn.execute('''
        SELECT DISTINCT name FROM tags ORDER BY name
    ''').fetchall()
    
    conn.close()
    return render_template('admin_tags.html',
                         products=products,
                         tag_names=tag_names,
                         tag_name_filter=tag_name_filter,
                         show_all=show_all)

@admin_bp.route('/api/tags', methods=['GET'])
@require_admin
def get_tags():
    """Get all tags or tags for a specific product"""
    product_id = request.args.get('productId')
    conn = get_db_connection()
    
    if product_id:
        tags = conn.execute('SELECT * FROM tags WHERE productId = ? ORDER BY name', (product_id,)).fetchall()
    else:
        tags = conn.execute('SELECT * FROM tags ORDER BY name').fetchall()
    
    conn.close()
    return jsonify([dict(tag) for tag in tags])

@admin_bp.route('/api/tags/names', methods=['GET'])
@require_admin
def get_tag_names():
    """Get all unique tag names"""
    conn = get_db_connection()
    tag_names = conn.execute('SELECT DISTINCT name FROM tags ORDER BY name').fetchall()
    conn.close()
    return jsonify([row['name'] for row in tag_names])

@admin_bp.route('/api/tags', methods=['POST'])
@require_admin
def create_tag():
    """Create a new tag"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('''
            INSERT INTO tags (productId, name, value, note, active)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('productId'),
            data.get('name'),
            data.get('value', ''),
            data.get('note', ''),
            1 if data.get('active', True) else 0
        ))
        conn.commit()
        tag_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'tagId': tag_id})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/tags/<int:tag_id>', methods=['PUT'])
@require_admin
def update_tag(tag_id):
    """Update a tag"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE tags
            SET productId = ?, name = ?, value = ?, note = ?, active = ?
            WHERE tagId = ?
        ''', (
            data.get('productId'),
            data.get('name'),
            data.get('value'),
            data.get('note'),
            1 if data.get('active') else 0,
            tag_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/tags/<int:tag_id>', methods=['DELETE'])
@require_admin
def delete_tag(tag_id):
    """Delete a tag"""
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM tags WHERE tagId = ?', (tag_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Made with Bob
