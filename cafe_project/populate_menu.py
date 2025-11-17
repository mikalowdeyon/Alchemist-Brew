import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')
django.setup()

from cafe.models import MenuItem

# Menu data from the hardcoded array
MENU_DATA = [
    # COFFEES AND PASTRIES
    { 'name': "The Midas Touch (Caramel Macchiato)", 'category': "Coffees and Pastries", 'price': 180.00, 'description': "A truly magical concoction. This coffee is infused with a caramel so rich and luxurious, it feels as though everything it touches has been turned to gold.", 'is_best_seller': True },
    { 'name': "The Black Onyx (Cold Brew)", 'category': "Coffees and Pastries", 'price': 140.00, 'description': "A powerful, dark brew as deep and mysterious as a polished onyx stone. This elixir provides strength and focus for your day's quests." },
    { 'name': "The Sweet Sorcery (Spanish Latte)", 'category': "Coffees and Pastries", 'price': 200.00, 'description': "A bewitching and delightful brew of our espresso and sweetened condensed milk, creating a rich, creamy, and irresistible potion." },
    { 'name': "The Nimbus Brew (Cappuccino)", 'category': "Coffees and Pastries", 'price': 180.00, 'description': "A classic potion of espresso, velvety steamed milk, and a thick cloud of ethereal foam. A light, airy brew for a peaceful moment.", 'is_best_seller': True },
    { 'name': "The Chocolate Chimera (Mocha)", 'category': "Coffees and Pastries", 'price': 175.00, 'description': "A rich and mysterious fusion of espresso, decadent chocolate, and steamed milk. A delicious and complex beast of a drink" },
    { 'name': "The Silver Orb (Latte) ", 'category': "Coffees and Pastries", 'price': 180.00, 'description': "A smooth, harmonious blend of espresso and steamed milk, topped with a silken, creamy finish. A perfectly balanced concoction." },
    { 'name': "The Elixir of Vigor", 'category': "Coffees and Pastries", 'price': 180.00, 'description': "Equal parts espresso and steamed milk. A small, potent, and perfectly balanced draught for quick vitality." },
    { 'name': "Caramelized Orb", 'category': "Coffees and Pastries", 'price': 190.00, 'description': "A latte flavored with rich vanilla, topped with a thin layer of caramelized sugar for a satisfying crackle." },
    { 'name': "The Golden Spiral (Cinnamon Roll)", 'category': "Coffees and Pastries", 'price': 80.00, 'description': "A warm, coiled pastry infused with the Spirits of Prosperity and sweet spice, guaranteeing a day of good fortune." },
    { 'name': "The Dark Matter (Chocolate Fudge Brownie)", 'category': "Coffees and Pastries", 'price': 80.00, 'description': "A dense, intensely rich, and cosmic void of pure chocolate essence. Consume and embrace the mysteries of the universe." },
    { 'name': "The Celestial Gateau (Blueberry Lemon Cake) ", 'category': "Coffees and Pastries", 'price': 140.00, 'description': "A vibrant slice of Blueberry Lemon Cake, tasting like the sweet, clear air found just beyond the heavenly gates." },
    { 'name': "The Phoenix's Feather (Croissant)", 'category': "Coffees and Pastries", 'price': 90.00, 'description': "A light, flaky, and buttery creation, reborn from the ashes with a delicate crust of golden immortality." },
    { 'name': "The Sunstone Cookie (Chocolate Chip Cookie)", 'category': "Coffees and Pastries", 'price': 80.00, 'description': "A soft, warm cookie embedded with rich chocolate chips, capturing the benevolent power and warmth of the sun." },
    { 'name': "The Molten Core (Chocolate Lava Cake)", 'category': "Coffees and Pastries", 'price': 140.00, 'description': "A decadent chocolate cake concealing a molten, fiery center. Break the crust to release the intense, pure energy within." },
    { 'name': "The Lunar Cheesecake (cheskeyk)", 'category': "Coffees and Pastries", 'price': 140.00, 'description': "A velvety smooth cheesecake, its light and creamy texture as cool and ethereal as a slice of the full moon." },
    { 'name': "The Heartstone Slice (Red Velvet Cake)", 'category': "Coffees and Pastries", 'price': 150.00, 'description': "A deep red velvet cake, symbolizing the true heart of the alchemist. Richly layered with a divine cream cheese frosting." },

    # NON-COFFEES
    { 'name': "The Hearthfire Potion (Chai Latte)", 'category': "Non-Coffees", 'price': 120.00, 'description': "A warm, spiced potion with notes of cinnamon, cardamom, and clove, designed to ignite your inner fire and bring a sense of cozy magic." },
    { 'name': "The Lunar Lemonade (Fresh Lemonade)", 'category': "Non-Coffees", 'price': 100.00, 'description': "A tart, refreshing elixir crafted to cool and enlighten. This icy potion is a simple, yet spellbinding, charm for a hot day." },
    { 'name': "The Dragon's Breath (Hot Chocolate)", 'category': "Non-Coffees", 'price': 100.00, 'description': "A rich, dark potion of molten chocolate and milk, guaranteed to warm you from the inside out and give you a powerful glow." },
    { 'name': "Phoenix's Rebirth", 'category': "Non-Coffees", 'price': 140.00, 'description': "A bright, invigorating draught of sweet mango and citrus, with a subtle, slow-burning kick of chili at the finish. Rejuvenating and surprising." },
    { 'name': "Sylph's Zephyr", 'category': "Non-Coffees", 'price': 130.00, 'description': "A light, effervescent potion of fresh lime juice, mint, and sparkling water. As gentle and refreshing as a breath of wind." },
    { 'name': "Emerald Insight", 'category': "Non-Coffees", 'price': 140.00, 'description': "Earthy, vibrant matcha shaken with cold, tart lemonade. A potent, focused green elixir for a clear mind." },
    { 'name': "Potion of Levitation", 'category': "Non-Coffees", 'price': 130.00, 'description': "A classic, bubbly, sweet potion of dark root beer topped with a scoop of vanilla ice cream. A timeless charm for pure enjoyment." },
    { 'name': "Witch's Brew", 'category': "Non-Coffees", 'price': 130.00, 'description': "Tart hibiscus tea brewed strong, sweetened slightly, and mixed with fresh berries. A blood-red, flavorful, and thirst-quenching spell." },

    # BARISTA'S SPECIALS
    { 'name': "The Jade Essence(Matcha Latte)", 'category': "Barista's Specials", 'price': 200.00, 'description': "A vibrant, emerald-green potion crafted from the purest, finely ground tea leaves. This earthy and revitalizing brew awakens the mind and nourishes the soul." },
    { 'name': "Aurora Borealis", 'category': "Barista's Specials", 'price': 180.00, 'description': "A visually stunning refresher layered with passion fruit and ginger, achieving its vibrant, cosmic blue hue naturally. Icy cold and bright." },
    { 'name': "Tears of the Siren", 'category': "Barista's Specials", 'price': 200.00, 'description': "A dangerously smooth caramel frappe blended with a touch of sea salt and a light, mesmerizing turquoise drizzle." },
    { 'name': "The Rose Elixir (Iced Strawberry Frappe)", 'category': "Barista's Specials", 'price': 200.00, 'description': "A sweet, ruby-hued concoction of strawberries and ice, whipped into a delightful, frosty blend. It's a charm to lift your spirits and enchant your senses." },
    { 'name': "The Golden Elixir (Iced Caramel Latte)", 'category': "Barista's Specials", 'price': 150.00, 'description': "A sweet, sun-kissed potion infused with golden caramel. This rich and creamy brew is crafted to turn your day from simple to sublime." },
    { 'name': "The Voidstone Potion (Cookies & Cream Frappe) ", 'category': "Barista's Specials", 'price': 200.00, 'description': "A dark, cold concoction of rich chocolate and crushed cookie fragments, blended into a potion as mysterious and powerful as a voidstone." },
    { 'name': "The Enchanted Swirl (Milkshake)", 'category': "Barista's Specials", 'price': 180.00, 'description': "A classic, thick potion of ice cream and magic, swirled into a blissful, creamy concoction." },
    { 'name': "The Fae Woodland", 'category': "Barista's Specials", 'price': 150.00, 'description': "A classic, thick potion of ice cream and magic, swirled into a blissful, creamy concoction." },
]

def populate_menu():
    print("Populating menu items...")
    for item_data in MENU_DATA:
        item, created = MenuItem.objects.get_or_create(
            name=item_data['name'],
            defaults={
                'category': item_data['category'],
                'price': item_data['price'],
                'available': True,
                'is_best_seller': item_data.get('is_best_seller', False)
            }
        )
        if created:
            print(f"Created: {item.name}")
        else:
            # Update existing item if is_best_seller differs
            if item.is_best_seller != item_data.get('is_best_seller', False):
                item.is_best_seller = item_data.get('is_best_seller', False)
                item.save()
                print(f"Updated: {item.name}")
            else:
                print(f"Already exists: {item.name}")

    print("Menu population complete!")

if __name__ == '__main__':
    populate_menu()
