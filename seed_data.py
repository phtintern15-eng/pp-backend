"""
Seed the database with initial property data and an admin user.
Run once: py seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine, Base
from models import User, Property, PropertyType, PropertyImage
import bcrypt
import json

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

PROPERTIES = [
    {
        "title": "The Bel-Air Glass Pavilion",
        "prop_type": "villa", "category": "villas", "status": "For Sale", "purpose": "buy",
        "price": "$4,850,000", "price_raw": 4850000,
        "location": "Beverly Hills, CA", "beds": 5, "baths": 6, "sqft": "6,400",
        "image_url": "/static/images/hero_luxury_villa.jpg",
        "description": "An architectural tour de force featuring panoramic hillside vistas, zero-edge infinity pool, floor-to-ceiling motorized Fleetwood glass doors, and a custom Italian Poliform kitchen.",
        "amenities": json.dumps(["Infinity Pool", "Wine Cellar", "Smart Home Automation", "Private Cinema", "Electric Vehicle Charger"]),
        "agent_name": "Victoria Stone",
        "agent_avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80"
    },
    {
        "title": "Skyline Horizon Penthouse",
        "prop_type": "penthouse", "category": "penthouses", "status": "Featured", "purpose": "buy",
        "price": "$6,200,000", "price_raw": 6200000,
        "location": "Manhattan, New York", "beds": 4, "baths": 4.5, "sqft": "4,950",
        "image_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80",
        "description": "Perched high above Central Park, this duplex penthouse features a private wrap-around terrace, 14-foot ceilings, bespoke marble fireplaces, and unmatched skyline panoramas.",
        "amenities": json.dumps(["Wrap-around Terrace", "Private Elevator Access", "Concierge 24/7", "Calacatta Marble Bathrooms", "Valet Parking"]),
        "agent_name": "David Vance",
        "agent_avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80"
    },
    {
        "title": "Azure Shoreline Ocean Villa",
        "prop_type": "waterfront", "category": "waterfront", "status": "For Sale", "purpose": "buy",
        "price": "$5,400,000", "price_raw": 5400000,
        "location": "Miami Beach, FL", "beds": 6, "baths": 7, "sqft": "7,100",
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
        "description": "Private direct dockage with deepwater access, resort-style poolside cabanas, outdoor summer kitchen, and luminous open-plan living designed for ultimate seaside tranquility.",
        "amenities": json.dumps(["Private Deepwater Dock", "Outdoor Kitchen", "Heated Pool", "Rooftop Deck", "Spa & Sauna"]),
        "agent_name": "Victoria Stone",
        "agent_avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80"
    },
    {
        "title": "Nordic Minimalist Loft",
        "prop_type": "condo", "category": "condos", "status": "For Rent", "purpose": "rent",
        "price": "$14,500 / mo", "price_raw": 14500,
        "location": "Tribeca, New York", "beds": 3, "baths": 3, "sqft": "2,850",
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "description": "Warm minimalist aesthetic with Scandinavian white oak floors, exposed architectural brick accents, custom fluted millwork, and top-tier Gaggenau appliances.",
        "amenities": json.dumps(["Exposed Brick", "Chef Kitchen", "Keyed Elevator", "Soundproofing", "Fitness Studio Access"]),
        "agent_name": "Elena Rostova",
        "agent_avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80"
    },
    {
        "title": "The Aspen Ridge Chalet",
        "prop_type": "villa", "category": "villas", "status": "For Sale", "purpose": "buy",
        "price": "$3,950,000", "price_raw": 3950000,
        "location": "Aspen, Colorado", "beds": 5, "baths": 5.5, "sqft": "5,300",
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
        "description": "Ski-in/ski-out luxury residence surrounded by evergreen forest. Highlights include heated stone terraces, indoor spa pool, floor-to-ceiling timber beams, and breathtaking mountain views.",
        "amenities": json.dumps(["Ski-in / Ski-out", "Heated Driveway", "Indoor Jacuzzi", "Stone Fireplace", "Wine Room"]),
        "agent_name": "David Vance",
        "agent_avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80"
    },
    {
        "title": "The Metropolitan Oasis Residence",
        "prop_type": "condo", "category": "condos", "status": "For Rent", "purpose": "rent",
        "price": "$19,000 / mo", "price_raw": 19000,
        "location": "Downtown Los Angeles, CA", "beds": 3, "baths": 3.5, "sqft": "3,400",
        "image_url": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",
        "description": "Contemporary urban luxury with a sprawling private botanical terrace, integrated Sub-Zero appliances, double rain showers, and 24-hour white-glove security.",
        "amenities": json.dumps(["Private Terrace Garden", "Sub-Zero Suite", "24/7 Doorman", "Rooftop Pool", "Private Storage"]),
        "agent_name": "Elena Rostova",
        "agent_avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80"
    },
]

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Admin user
        admin_user = None
        for admin_email in ["admin@primeproperties.com", "admin@auraestates.com"]:
            existing = db.query(User).filter(User.email == admin_email).first()
            if not existing:
                admin = User(
                    first_name="Admin",
                    last_name="Prime",
                    email=admin_email,
                    hashed_password=get_password_hash("admin123"),
                    user_type="admin",
                    is_admin=True,
                    company="Prime Properties",
                    location="New York"
                )
                db.add(admin)
                db.commit()
                db.refresh(admin)
                admin_user = admin
                print(f"Admin user created: {admin_email} / admin123")
            else:
                admin_user = existing

        # Properties
        existing_props = db.query(Property).count()
        if existing_props == 0 and admin_user:
            for p in PROPERTIES:
                # Map to Property model
                prop_type_enum = PropertyType.RESIDENTIAL
                prop_item = Property(
                    title=p["title"],
                    description=p["description"],
                    address=p["location"],
                    city=p["location"].split(",")[0].strip() if "," in p["location"] else p["location"],
                    state=p["location"].split(",")[1].strip() if "," in p["location"] else "CA",
                    zip_code="90210",
                    property_type=prop_type_enum,
                    bedrooms=p.get("beds", 4),
                    bathrooms=int(p.get("baths", 4)),
                    area_sqft=float(p.get("sqft", "5000").replace(",", "")),
                    price=float(p.get("price_raw", 2500000)),
                    owner_id=admin_user.id
                )
                db.add(prop_item)
                db.commit()
                db.refresh(prop_item)
                
                # Add primary image
                if p.get("image_url"):
                    from models import PropertyImage
                    img = PropertyImage(
                        property_id=prop_item.id,
                        image_url=p["image_url"],
                        is_primary=True
                    )
                    db.add(img)
            db.commit()
            print(f"Seeded {len(PROPERTIES)} properties with images")
        else:
            print(f"Properties already exist ({existing_props} found)")

        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
