from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Temporary Database 
shopping_items = []

@app.route('/ab', methods=['POST'])
def process_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Text data not provided"}), 400
    
    text = data['text']
    items = extract_items_from_text(text)

    # Mock database operation (saving items)
    save_items_to_db(items)

    return jsonify({"text": text, "items": items})

def extract_items_from_text(text):
    items = []
    # Split the text at commas and "and"
    segments = re.split(r',|and', text)
    pattern = re.compile(r'(\d+)\s*(kg|g|l|lbs|oz|liters|ml|units)\s*(\S+(?:\s+\S+)*)')  # Matches quantities, units, and nouns
    
    for segment in segments:
        matches = re.findall(pattern, segment)
        for match in matches:
            quantity = int(match[0])
            unit = match[1]
            item = match[2]
            items.append({"item": item.strip(), "quantity": quantity, "unit": unit})
    
    return items

def save_items_to_db(items):
    global shopping_items
    for item in items:
        # Check if item already exists
        existing_item = next((x for x in shopping_items if x['item'] == item['item'] and x['unit'] == item['unit']), None)
        if existing_item:
            # If item exists, update quantity
            existing_item['quantity'] += item['quantity']
        else:
            # If item does not exist, add it to the list
            shopping_items.append(item)

@app.route('/shopping-list', methods=['GET'])
def get_shopping_list():
    return jsonify({"shopping_list": shopping_items}), 200

if __name__ == '__main__':
    app.run(debug=True)
