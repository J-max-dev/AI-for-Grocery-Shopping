from flask import Flask, render_template, request
import random

app = Flask(__name__)

class Item:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

class ItemDatabase:
    def __init__(self):
        self.items = []

    def add_item(self, name, category, price):
        item = Item(name, category, price)
        self.items.append(item)

    def search_item(self, keyword):
        matching_items = []
        for item in self.items:
            if keyword.lower() in item.name.lower():
                matching_items.append(item)
        return matching_items

def recommend_items(database, selected_items, num_recommendations):
    recommendations = []
    for item in database.items:
        if item not in selected_items:
            recommendations.append(item)
    random.shuffle(recommendations)
    if len(recommendations) >= num_recommendations:
        return recommendations[:num_recommendations]
    else:
        return []

# Creating a sample item database
database = ItemDatabase()
# Adding fruit items
database.add_item("Apple", "Fruit", 1.99)
database.add_item("Banana", "Fruit", 0.99)
database.add_item("Orange", "Fruit", 1.49)
# Adding vegetable items
database.add_item("Carrot", "Vegetable", 0.99)
database.add_item("Tomato", "Vegetable", 1.49)
database.add_item("Cucumber", "Vegetable", 0.79)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
    keyword = request.form['keyword']
    results = database.search_item(keyword)
    return render_template('results.html', results=results)

@app.route('/recommendation', methods=['GET','POST'])
def recommendation():
    num_recommendations = int(request.form['num_recommendations'])
    selected_items = []
    while True:
        item_name = input("Enter an item name (or 'done' if finished): ")
        if item_name.lower() == 'done':
            break
        else:
            item = next((item for item in database.items if item.name.lower() == item_name.lower()), None)
            if item:
                selected_items.append(item)
            else:
                print("Item not found in the database. Please try again.")

    recommendations = recommend_items(database, selected_items, num_recommendations)
    return render_template('recommendation.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run()
