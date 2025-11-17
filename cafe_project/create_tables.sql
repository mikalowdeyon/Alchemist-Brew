-- Create tables for the cafe app in Supabase

-- MenuItem table
CREATE TABLE IF NOT EXISTS cafe_menuitem (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(6,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

-- Order table
CREATE TABLE IF NOT EXISTS cafe_order (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    total_price DECIMAL(8,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_confirmed BOOLEAN DEFAULT FALSE
);

-- OrderItem table
CREATE TABLE IF NOT EXISTS cafe_orderitem (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES cafe_order(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES cafe_menuitem(id),
    quantity INTEGER DEFAULT 1,
    size VARCHAR(20),
    milk VARCHAR(20),
    sweetness VARCHAR(20)
);

-- StudyRoomBooking table
CREATE TABLE IF NOT EXISTS cafe_studyroombooking (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    date DATE NOT NULL,
    time_slot VARCHAR(100) NOT NULL,
    is_confirmed BOOLEAN DEFAULT FALSE
);

-- Drink table
CREATE TABLE IF NOT EXISTS cafe_drink (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image VARCHAR(100),
    featured BOOLEAN DEFAULT FALSE,
    is_best_seller BOOLEAN DEFAULT FALSE
);

-- Product table
CREATE TABLE IF NOT EXISTS cafe_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    description TEXT
);

-- Carts table for shopping cart
CREATE TABLE IF NOT EXISTS carts (
    user_id UUID PRIMARY KEY,
    menu_items JSONB DEFAULT '[]'::jsonb,
    reservation JSONB DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS) if needed
-- ALTER TABLE carts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE cafe_order ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE cafe_studyroombooking ENABLE ROW LEVEL SECURITY;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_cafe_menuitem_category ON cafe_menuitem(category);
CREATE INDEX IF NOT EXISTS idx_cafe_order_user_id ON cafe_order(user_id);
CREATE INDEX IF NOT EXISTS idx_cafe_studyroombooking_user_id ON cafe_studyroombooking(user_id);
CREATE INDEX IF NOT EXISTS idx_carts_user_id ON carts(user_id);
