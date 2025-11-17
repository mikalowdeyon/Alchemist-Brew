import os
import django
from supabase import create_client, Client

# Setup Django (for settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')
django.setup()

# Supabase credentials
SUPABASE_URL = 'https://xaiblnxwezqrhusbvpwl.supabase.co'
SUPABASE_ANON_KEY = 'sb_publishable_QSuYzyM9Y7ak4Q1li0pLOg_cttfXwcn'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Menu data
MENU_DATA = [
    # COFFEE SELECTION
    { 'name': "The Midas Touch (Caramel Macchiato)", 'category': "COFFEE", 'price': 180.00, 'description': "A truly magical concoction. This coffee is infused with a caramel so rich and luxurious, it feels as though everything it touches has been turned to gold." },
    { 'name': "The Black Onyx (Cold Brew)", 'category': "COFFEE", 'price': 140.00, 'description': "A powerful, dark brew as deep and mysterious as a polished onyx stone. This elixir provides strength and focus for your day's quests." },
    { 'name': "The Sweet Sorcery (Spanish Latte)", 'category': "COFFEE", 'price': 200.00, 'description': "A bewitching and delightful brew of our espresso and sweetened condensed milk, creating a rich, creamy, and irresistible potion." },
    { 'name': "The Nimbus Brew (Cappuccino)", 'category': "COFFEE", 'price': 180.00, 'description': "A classic potion of espresso, velvety steamed milk, and a thick cloud of ethereal foam. A light, airy brew for a peaceful moment." },
    { 'name': "The Chocolate Chimera (Mocha)", 'category': "COFFEE", 'price': 175.00, 'description': "A rich and mysterious fusion of espresso, decadent chocolate, and steamed milk. A delicious and complex beast of a drink" },
    { 'name': "The Silver Orb (Latte) ", 'category': "COFFEE", 'price': 180.00, 'description': "A smooth, harmonious blend of espresso and steamed milk, topped with a silken, creamy finish. A perfectly balanced concoction." },
    { 'name': "The Elixir of Vigor", 'category': "COFFEE", 'price': 180.00, 'description': "Equal parts espresso and steamed milk. A small, potent, and perfectly balanced draught for quick vitality." },
    { 'name': "Caramelized Orb", 'category': "COFFEE", 'price': 190.00, 'description': "A latte flavored with rich vanilla, topped with a thin layer of caramelized sugar for a satisfying crackle." },

    # NON-COFFEE SELECTION
    { 'name': "The Hearthfire Potion (Chai Latte)", 'category': "NON-COFFEE", 'price': 120.00, 'description': "A warm, spiced potion with notes of cinnamon, cardamom, and clove, designed to ignite your inner fire and bring a sense of cozy magic." },
    { 'name': "The Lunar Lemonade (Fresh Lemonade)", 'category': "NON-COFFEE", 'price': 100.00, 'description': "A tart, refreshing elixir crafted to cool and enlighten. This icy potion is a simple, yet spellbinding, charm for a hot day." },
    { 'name': "The Dragon's Breath (Hot Chocolate)", 'category': "NON-COFFEE", 'price': 100.00, 'description': "A rich, dark potion of molten chocolate and milk, guaranteed to warm you from the inside out and give you a powerful glow." },
    { 'name': "Phoenix's Rebirth", 'category': "NON-COFFEE", 'price': 140.00, 'description': "A bright, invigorating draught of sweet mango and citrus, with a subtle, slow-burning kick of chili at the finish. Rejuvenating and surprising." },
    { 'name': "Sylph's Zephyr", 'category': "NON-COFFEE", 'price': 130.00, 'description': "A light, effervescent potion of fresh lime juice, mint, and sparkling water. As gentle and refreshing as a breath of wind." },
    { 'name': "Emerald Insight", 'category': "NON-COFFEE", 'price': 140.00, 'description': "Earthy, vibrant matcha shaken with cold, tart lemonade. A potent, focused green elixir for a clear mind." },
    { 'name': "Potion of Levitation", 'category': "NON-COFFEE", 'price': 130.00, 'description': "A classic, bubbly, sweet potion of dark root beer topped with a scoop of vanilla ice cream. A timeless charm for pure enjoyment." },
    { 'name': "Witch's Brew", 'category': "NON-COFFEE", 'price': 130.00, 'description': "Tart hibiscus tea brewed strong, sweetened slightly, and mixed with fresh berries. A blood-red, flavorful, and thirst-quenching spell." },

    # ICED & CHILLED CONCOCTIONS
    { 'name': "The Jade Essence(Matcha Latte)", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 200.00, 'description': "A vibrant, emerald-green potion crafted from the purest, finely ground tea leaves. This earthy and revitalizing brew awakens the mind and nourishes the soul." },
    { 'name': "Aurora Borealis", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 180.00, 'description': "A visually stunning refresher layered with passion fruit and ginger, achieving its vibrant, cosmic blue hue naturally. Icy cold and bright." },
    { 'name': "Tears of the Siren", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 200.00, 'description': "A dangerously smooth caramel frappe blended with a touch of sea salt and a light, mesmerizing turquoise drizzle." },
    { 'name': "The Rose Elixir (Iced Strawberry Frappe)", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 200.00, 'description': "A sweet, ruby-hued concoction of strawberries and ice, whipped into a delightful, frosty blend. It's a charm to lift your spirits and enchant your senses." },
    { 'name': "The Golden Elixir (Iced Caramel Latte)", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 150.00, 'description': "A sweet, sun-kissed potion infused with golden caramel. This rich and creamy brew is crafted to turn your day from simple to sublime." },
    { 'name': "The Voidstone Potion (Cookies & Cream Frappe) ", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 200.00, 'description': "A dark, cold concoction of rich chocolate and crushed cookie fragments, blended into a potion as mysterious and powerful as a voidstone." },
    { 'name': "The Enchanted Swirl (Milkshake)", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 180.00, 'description': "A classic, thick potion of ice cream and magic, swirled into a blissful, creamy concoction." },
    { 'name': "The Fae Woodland", 'category': "ICED & CHILLED CONCOCTIONS", 'price': 150.00, 'description': "A classic, thick potion of ice cream and magic, swirled into a blissful, creamy concoction." },

    # PASTRIES
    { 'name': "The Golden Spiral (Cinnamon Roll)", 'category': "PASTRIES", 'price': 80.00, 'description': "A warm, coiled pastry infused with the Spirits of Prosperity and sweet spice, guaranteeing a day of good fortune." },
    { 'name': "The Dark Matter (Chocolate Fudge Brownie)", 'category': "PASTRIES", 'price': 80.00, 'description': "A dense, intensely rich, and cosmic void of pure chocolate essence. Consume and embrace the mysteries of the universe." },
    { 'name': "The Celestial Gateau (Blueberry Lemon Cake) ", 'category': "PASTRIES", 'price': 140.00, 'description': "A vibrant slice of Blueberry Lemon Cake, tasting like the sweet, clear air found just beyond the heavenly gates." },
    { 'name': "The Phoenix's Feather (Croissant)", 'category': "PASTRIES", 'price': 90.00, 'description': "A light, flaky, and buttery creation, reborn from the ashes with a delicate crust of golden immortality." },
    { 'name': "The Sunstone Cookie (Chocolate Chip Cookie)", 'category': "PASTRIES", 'price': 80.00, 'description': "A soft, warm cookie embedded with rich chocolate chips, capturing the benevolent power and warmth of the sun." },
    { 'name': "The Molten Core (Chocolate Lava Cake)", 'category': "PASTRIES", 'price': 140.00, 'description': "A decadent chocolate cake concealing a molten, fiery center. Break the crust to release the intense, pure energy within." },
    { 'name': "The Lunar Cheesecake (cheskeyk)", 'category': "PASTRIES", 'price': 140.00, 'description': "A velvety smooth cheesecake, its light and creamy texture as cool and ethereal as a slice of the full moon." },
    { 'name': "The Heartstone Slice (Red Velvet Cake)", 'category': "PASTRIES", 'price': 150.00, 'description': "A deep red velvet cake, symbolizing the true heart of the alchemist. Richly layered with a divine cream cheese frosting." },
]

def populate_supabase():
    print("Populating menu items in Supabase...")
    for item_data in MENU_DATA:
        try:
            response = supabase.table('cafe_menuitem').insert({
                'name': item_data['name'],
                'category': item_data['category'],
                'price': item_data['price'],
                'available': True
            }).execute()
            print(f"Inserted: {item_data['name']}")
        except Exception as e:
            print(f"Error inserting {item_data['name']}: {e}")
            # Try to update if exists
            try:
                response = supabase.table('cafe_menuitem').update({
                    'category': item_data['category'],
                    'price': item_data['price'],
                    'available': True
                }).eq('name', item_data['name']).execute()
                print(f"Updated: {item_data['name']}")
            except Exception as e2:
                print(f"Error updating {item_data['name']}: {e2}")


if __name__ == '__main__':
    populate_supabase()
