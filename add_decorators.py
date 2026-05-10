import re

with open('src/admin.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add @require_admin before all @admin_bp.route decorators that don't already have it
pattern = r'(@admin_bp\.route\([^\)]+\))\n(?!@require_admin\n)(def )'
replacement = r'\1\n@require_admin\n\2'
content = re.sub(pattern, replacement, content)

with open('src/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added @require_admin decorators to all admin routes')

# Made with Bob
