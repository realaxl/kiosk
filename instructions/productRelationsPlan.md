# Product Relations Extension - Implementation Plan

## Overview
This plan extends the kiosk system to support **product relationships** - defining how products relate to each other (e.g., "Product A requires Battery B"). The `productRelations` table has already been added to the database schema, and this plan covers the complete implementation using existing CSS classes from [`static/css/admin.css`](static/css/admin.css:1).

## Requirements Summary
- Products can have relationships to other products
- Example: Some products require batteries (another product)
- Bidirectional descriptions: `fromDescription` and `toDescription`
- Admin interface to manage product relationships
- Gallery display showing related products
- Database table already defined in [`assets/db.mmd`](assets/db.mmd:44)

---

## Database Schema (Already Defined)

### `productRelations` Table
Already present in [`assets/db.mmd`](assets/db.mmd:44):

```sql
CREATE TABLE productRelations (
    productRelationId INTEGER PRIMARY KEY,
    fromProductId INTEGER NOT NULL,
    toProductId INTEGER NOT NULL,
    fromDescription TEXT,
    toDescription TEXT,
    note TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (fromProductId) REFERENCES products(productId),
    FOREIGN KEY (toProductId) REFERENCES products(productId)
)
```

**Example Relationship:**
```
Product A: LED Badge (fromProductId = 5)
Product B: 9V Battery (toProductId = 12)
fromDescription: "benötigt" (requires)
toDescription: "wird benötigt in" (required by)

Display on Product A page: "LED Badge benötigt 9V Battery"
Display on Product B page: "9V Battery wird benötigt in LED Badge"
```

---

## CSS Class Reuse Strategy

The implementation will reuse existing CSS classes from [`static/css/admin.css`](static/css/admin.css:1):

- `.item` (line 266) → for relation items
- `.item-thumbnail` (line 281) → for product thumbnails in relations
- `.item-info` (line 304) → for relation information
- `.item-name` (line 309) → for product names
- `.item-description` (line 316) → for relation descriptions
- `.item-actions` (line 330) → for edit/delete buttons
- `.modal` (line 372) → for relation editor modal
- `.modal-content` (line 390) → modal container
- `.modal-header` (line 402) → modal header
- `.modal-body` (line 431) → modal body
- `.modal-footer` (line 435) → modal footer
- `.form-group` (line 447) → form fields
- `.btn`, `.btn-sm` (lines 79, 95) → buttons

Only minimal custom CSS will be added for relation-specific styling.

---

## Implementation Plan

### Phase 1: Database Setup ✓

The `productRelations` table is already defined in [`assets/db.mmd`](assets/db.mmd:44). We need to:

1. Add table definition to [`src/create_database.py`](src/create_database.py:107)
2. Run database creation/migration

### Phase 2: Backend API

Add product relations endpoints to [`src/admin.py`](src/admin.py:1):

- `GET /admin/api/products/<id>/relations` - Get all relations for a product
- `POST /admin/api/product-relations` - Create new relation
- `PUT /admin/api/product-relations/<id>` - Update relation
- `DELETE /admin/api/product-relations/<id>` - Delete relation (soft delete)

### Phase 3: Admin UI

Update [`templates/admin_products.html`](templates/admin_products.html:1):

1. Add relations section to product editor modal
2. Create relation editor modal (reusing `.modal` classes)
3. Add JavaScript for relation management
4. Use existing CSS classes for styling

### Phase 4: Gallery Display

Update [`templates/index.html`](templates/index.html:1):

1. Modify gallery API to include relations
2. Display relations in product detail modal
3. Add relation badge to product cards

---

## Detailed Implementation Steps

### Step 1: Update Database Schema

**File:** [`src/create_database.py`](src/create_database.py:107)

Add after the `tags` table definition (line 106):

```python
"productRelations": {
    "columns": {
        "productRelationId": "INTEGER PRIMARY KEY",
        "fromProductId": "INTEGER NOT NULL",
        "toProductId": "INTEGER NOT NULL",
        "fromDescription": "TEXT",
        "toDescription": "TEXT",
        "note": "TEXT",
        "active": "INTEGER NOT NULL DEFAULT 1"
    },
    "foreign_keys": [
        "FOREIGN KEY (fromProductId) REFERENCES products(productId)",
        "FOREIGN KEY (toProductId) REFERENCES products(productId)"
    ]
}
```

### Step 2: Backend API Implementation

**File:** [`src/admin.py`](src/admin.py:1)

Add after products routes (around line 450):

```python
# ============================================================================
# PRODUCT RELATIONS ROUTES
# ============================================================================

@admin_bp.route('/api/products/<int:product_id>/relations', methods=['GET'])
@require_admin
def get_product_relations(product_id):
    """Get all relations for a specific product"""
    conn = get_db_connection()
    
    # Relations where this product is the source
    from_relations = conn.execute('''
        SELECT pr.*, p.name as toProductName, p.image as toProductImage
        FROM productRelations pr
        JOIN products p ON pr.toProductId = p.productId
        WHERE pr.fromProductId = ? AND pr.active = 1
        ORDER BY p.name
    ''', (product_id,)).fetchall()
    
    # Relations where this product is the target
    to_relations = conn.execute('''
        SELECT pr.*, p.name as fromProductName, p.image as fromProductImage
        FROM productRelations pr
        JOIN products p ON pr.fromProductId = p.productId
        WHERE pr.toProductId = ? AND pr.active = 1
        ORDER BY p.name
    ''', (product_id,)).fetchall()
    
    conn.close()
    return jsonify({
        'fromRelations': [dict(r) for r in from_relations],
        'toRelations': [dict(r) for r in to_relations]
    })

@admin_bp.route('/api/product-relations', methods=['POST'])
@require_admin
def create_product_relation():
    """Create a new product relation"""
    data = request.get_json()
    conn = get_db_connection()
    
    # Validate products exist
    from_product = conn.execute('SELECT productId FROM products WHERE productId = ?', 
                                (data.get('fromProductId'),)).fetchone()
    to_product = conn.execute('SELECT productId FROM products WHERE productId = ?', 
                              (data.get('toProductId'),)).fetchone()
    
    if not from_product or not to_product:
        conn.close()
        return jsonify({'error': 'One or both products not found'}), 404
    
    # Prevent self-referencing
    if data.get('fromProductId') == data.get('toProductId'):
        conn.close()
        return jsonify({'error': 'Product cannot be related to itself'}), 400
    
    # Check for duplicate
    existing = conn.execute('''
        SELECT productRelationId FROM productRelations 
        WHERE fromProductId = ? AND toProductId = ? AND active = 1
    ''', (data.get('fromProductId'), data.get('toProductId'))).fetchone()
    
    if existing:
        conn.close()
        return jsonify({'error': 'Relation already exists'}), 400
    
    try:
        cursor = conn.execute('''
            INSERT INTO productRelations 
            (fromProductId, toProductId, fromDescription, toDescription, note, active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('fromProductId'),
            data.get('toProductId'),
            data.get('fromDescription', ''),
            data.get('toDescription', ''),
            data.get('note', ''),
            1
        ))
        conn.commit()
        relation_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'productRelationId': relation_id})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/product-relations/<int:relation_id>', methods=['PUT'])
@require_admin
def update_product_relation(relation_id):
    """Update a product relation"""
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE productRelations
            SET fromDescription = ?, toDescription = ?, note = ?, active = ?
            WHERE productRelationId = ?
        ''', (
            data.get('fromDescription'),
            data.get('toDescription'),
            data.get('note'),
            1 if data.get('active') else 0,
            relation_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/product-relations/<int:relation_id>', methods=['DELETE'])
@require_admin
def delete_product_relation(relation_id):
    """Delete (soft delete) a product relation"""
    conn = get_db_connection()
    try:
        conn.execute('UPDATE productRelations SET active = 0 WHERE productRelationId = ?', (relation_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
```

### Step 3: Admin UI - Product Relations Section

**File:** [`templates/admin_products.html`](templates/admin_products.html:1)

Add to product edit modal (after existing form fields):

```html
<!-- Product Relations Section -->
<div class="modal-section" style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #eee;">
    <h3 style="margin-bottom: 15px;">Produktbeziehungen</h3>
    
    <!-- From Relations -->
    <div class="relations-section">
        <h4>Dieses Produkt benötigt:</h4>
        <div id="fromRelationsList" class="relations-list"></div>
        <button type="button" class="btn btn-sm btn-outline-primary" onclick="addRelation()">
            <i class="bi bi-plus-circle"></i> Beziehung hinzufügen
        </button>
    </div>
    
    <!-- To Relations (read-only) -->
    <div class="relations-section" style="margin-top: 15px;">
        <h4>Wird benötigt in:</h4>
        <div id="toRelationsList" class="relations-list"></div>
    </div>
</div>

<!-- Relation Editor Modal -->
<div id="relationModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Produktbeziehung</h2>
            <span class="close" onclick="closeRelationModal()">&times;</span>
        </div>
        <div class="modal-body">
            <form id="relationForm">
                <input type="hidden" id="relationId">
                <input type="hidden" id="relationFromProductId">
                
                <div class="form-group">
                    <label for="relationToProductId">Zielprodukt *</label>
                    <select id="relationToProductId" class="form-control" required>
                        <option value="">-- Produkt auswählen --</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="relationFromDescription">Beschreibung (von → zu)</label>
                    <input type="text" id="relationFromDescription" class="form-control" 
                           placeholder="z.B. benötigt, erfordert">
                    <small class="form-text text-muted">
                        Anzeige: "[Dieses Produkt] [Beschreibung] [Zielprodukt]"
                    </small>
                </div>
                
                <div class="form-group">
                    <label for="relationToDescription">Beschreibung (zu → von)</label>
                    <input type="text" id="relationToDescription" class="form-control" 
                           placeholder="z.B. wird benötigt in">
                    <small class="form-text text-muted">
                        Anzeige: "[Zielprodukt] [Beschreibung] [Dieses Produkt]"
                    </small>
                </div>
                
                <div class="form-group">
                    <label for="relationNote">Notiz</label>
                    <textarea id="relationNote" class="form-control" rows="2"></textarea>
                </div>
            </form>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" onclick="closeRelationModal()">Abbrechen</button>
            <button type="button" class="btn btn-primary" onclick="saveRelation()">Speichern</button>
        </div>
    </div>
</div>

<style>
/* Minimal custom CSS - reuses classes from admin.css */
.relations-section {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.relations-section h4 {
    font-size: 14px;
    font-weight: 600;
    color: #495057;
    margin-bottom: 10px;
}

.relations-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 10px;
}

/* Relations use .item class from admin.css */
</style>

<script>
let currentProductId = null;
let currentRelations = { from: [], to: [] };

async function loadProductRelations(productId) {
    currentProductId = productId;
    
    try {
        const response = await fetch(`/admin/api/products/${productId}/relations`);
        const data = await response.json();
        
        currentRelations = {
            from: data.fromRelations || [],
            to: data.toRelations || []
        };
        
        renderRelations();
    } catch (error) {
        console.error('Error loading relations:', error);
    }
}

function renderRelations() {
    // Render "from" relations using .item class
    const fromList = document.getElementById('fromRelationsList');
    if (currentRelations.from.length === 0) {
        fromList.innerHTML = '<p class="text-muted" style="font-size: 13px;">Keine Beziehungen</p>';
    } else {
        fromList.innerHTML = currentRelations.from.map(rel => `
            <div class="item">
                <div class="item-thumbnail">
                    ${rel.toProductImage ? 
                        `<img src="/images/cache/${rel.toProductImage}" alt="${rel.toProductName}">` :
                        '📦'
                    }
                </div>
                <div class="item-info">
                    <div class="item-name">${rel.toProductName}</div>
                    ${rel.fromDescription ? 
                        `<div class="item-description">${rel.fromDescription}</div>` : 
                        ''
                    }
                </div>
                <div class="item-actions">
                    <button class="btn btn-sm btn-outline-primary" onclick="editRelation(${rel.productRelationId})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteRelation(${rel.productRelationId})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    // Render "to" relations (read-only)
    const toList = document.getElementById('toRelationsList');
    if (currentRelations.to.length === 0) {
        toList.innerHTML = '<p class="text-muted" style="font-size: 13px;">Keine Beziehungen</p>';
    } else {
        toList.innerHTML = currentRelations.to.map(rel => `
            <div class="item">
                <div class="item-thumbnail">
                    ${rel.fromProductImage ? 
                        `<img src="/images/cache/${rel.fromProductImage}" alt="${rel.fromProductName}">` :
                        '📦'
                    }
                </div>
                <div class="item-info">
                    <div class="item-name">${rel.fromProductName}</div>
                    ${rel.toDescription ? 
                        `<div class="item-description">${rel.toDescription}</div>` : 
                        ''
                    }
                </div>
            </div>
        `).join('');
    }
}

function addRelation() {
    document.getElementById('relationId').value = '';
    document.getElementById('relationFromProductId').value = currentProductId;
    document.getElementById('relationToProductId').value = '';
    document.getElementById('relationFromDescription').value = 'benötigt';
    document.getElementById('relationToDescription').value = 'wird benötigt in';
    document.getElementById('relationNote').value = '';
    
    loadProductsForRelation();
    document.getElementById('relationModal').classList.add('active');
}

async function loadProductsForRelation() {
    try {
        const response = await fetch('/admin/api/products');
        const products = await response.json();
        
        const select = document.getElementById('relationToProductId');
        select.innerHTML = '<option value="">-- Produkt auswählen --</option>';
        
        products
            .filter(p => p.productId !== currentProductId && p.active === 1)
            .forEach(product => {
                const option = document.createElement('option');
                option.value = product.productId;
                option.textContent = product.name;
                select.appendChild(option);
            });
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

async function saveRelation() {
    const relationId = document.getElementById('relationId').value;
    const data = {
        fromProductId: parseInt(document.getElementById('relationFromProductId').value),
        toProductId: parseInt(document.getElementById('relationToProductId').value),
        fromDescription: document.getElementById('relationFromDescription').value,
        toDescription: document.getElementById('relationToDescription').value,
        note: document.getElementById('relationNote').value
    };
    
    try {
        let response;
        if (relationId) {
            response = await fetch(`/admin/api/product-relations/${relationId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch('/admin/api/product-relations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        
        const result = await response.json();
        
        if (result.success) {
            closeRelationModal();
            await loadProductRelations(currentProductId);
            // alert('Beziehung gespeichert');
        } else {
            alert(result.error || 'Fehler beim Speichern');
        }
    } catch (error) {
        console.error('Error saving relation:', error);
        alert('Fehler beim Speichern');
    }
}

async function deleteRelation(relationId) {
    if (!confirm('Beziehung wirklich löschen?')) return;
    
    try {
        const response = await fetch(`/admin/api/product-relations/${relationId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            await loadProductRelations(currentProductId);
            // alert('Beziehung gelöscht');
        } else {
            alert(result.error || 'Fehler beim Löschen');
        }
    } catch (error) {
        console.error('Error deleting relation:', error);
        alert('Fehler beim Löschen');
    }
}

function closeRelationModal() {
    document.getElementById('relationModal').classList.remove('active');
}

// Hook into existing editProduct function
const originalEditProduct = window.editProduct;
window.editProduct = async function(productId) {
    await originalEditProduct(productId);
    await loadProductRelations(productId);
};
</script>
```

### Step 4: Gallery Display

**File:** [`src/app.py`](src/app.py:1)

Update gallery endpoint to include relations (around line 150):

```python
@app.route('/api/gallery')
def get_gallery():
    """Get gallery data with products and their relations"""
    conn = get_db_connection()
    
    event = conn.execute(
        'SELECT * FROM events WHERE active = 1 ORDER BY timestamp DESC LIMIT 1'
    ).fetchone()
    
    if not event:
        conn.close()
        return jsonify({'error': 'No active event'}), 404
    
    stocks = conn.execute('''
        SELECT s.*, p.name, p.description, p.image, p.url, p.manualUrl,
               pc.name as categoryName
        FROM stocks s
        JOIN products p ON s.productId = p.productId
        LEFT JOIN productCategories pc ON p.productCategoryId = pc.productCategoryId
        WHERE s.eventId = ? AND s.active = 1 AND p.active = 1
        ORDER BY s.favorite DESC, p.name
    ''', (event['eventId'],)).fetchall()
    
    products_with_relations = []
    for stock in stocks:
        product_dict = dict(stock)
        
        # Get relations
        relations = conn.execute('''
            SELECT pr.*, p.name as relatedProductName, p.image as relatedProductImage
            FROM productRelations pr
            JOIN products p ON pr.toProductId = p.productId
            WHERE pr.fromProductId = ? AND pr.active = 1
        ''', (stock['productId'],)).fetchall()
        
        product_dict['relations'] = [dict(r) for r in relations]
        products_with_relations.append(product_dict)
    
    conn.close()
    
    return jsonify({
        'event': dict(event),
        'products': products_with_relations
    })
```

**File:** [`templates/index.html`](templates/index.html:1)

Add to product detail modal and card:

```html
<!-- In product detail modal, after description -->
<div v-if="selectedProduct.relations && selectedProduct.relations.length > 0" 
     style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
    <h5 style="font-size: 16px; font-weight: 600; margin-bottom: 10px;">Benötigte Produkte:</h5>
    <div v-for="rel in selectedProduct.relations" :key="rel.productRelationId" 
         style="display: flex; align-items: center; gap: 10px; padding: 10px; background: white; border-radius: 6px; margin-bottom: 8px;">
        <img v-if="rel.relatedProductImage" 
             :src="'/images/cache/' + rel.relatedProductImage" 
             style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">
        <div v-else style="width: 50px; height: 50px; background: #e9ecef; border-radius: 4px; display: flex; align-items: center; justify-content: center;">📦</div>
        <div style="flex: 1;">
            <div style="font-weight: 600;">{{ rel.relatedProductName }}</div>
            <div v-if="rel.fromDescription" style="font-size: 13px; color: #6c757d; font-style: italic;">
                {{ rel.fromDescription }}
            </div>
        </div>
    </div>
</div>

<!-- Add badge to product card -->
<span v-if="product.relations && product.relations.length > 0" 
      style="position: absolute; top: 10px; right: 10px; background: rgba(13, 110, 253, 0.9); color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; z-index: 10;">
    <i class="bi bi-link-45deg"></i> {{ product.relations.length }}
</span>
```

---

## Testing Checklist

- [ ] Database table created successfully
- [ ] Create product relation via admin UI
- [ ] Edit relation descriptions
- [ ] Delete relation
- [ ] Prevent self-referencing relations
- [ ] Prevent duplicate relations
- [ ] View relations in product editor (both directions)
- [ ] Relations display in gallery product detail
- [ ] Relation badge shows on product cards

---

## Notes

- Reuses existing CSS classes from [`static/css/admin.css`](static/css/admin.css:1)
- Relations are bidirectional in display but directional in storage
- Soft delete (active flag) for relations
- Products can have multiple relations
