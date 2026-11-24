from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class UserType(str, enum.Enum):
    CONSULTANT = "consultant"
    OWNER = "owner"
    BUYER = "buyer"
    ADMIN = "admin"

class PropertyType(str, enum.Enum):
    RESIDENTIAL = "RESIDENTIAL"
    COMMERCIAL = "COMMERCIAL"
    OFFICE = "OFFICE"



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(String(20), nullable=False)
    company = Column(String(255))  # For property owners
    property_count = Column(String(50))  # Number of properties
    location = Column(String(100))  # Primary location/city
    subscription_plan = Column(String(50))  # Subscription plan for owners
    citizenship_status = Column(String(50), nullable=True)  # local, nri, oci, foreign_national
    residence_country = Column(String(100), nullable=True)  # e.g., United States, UAE, UK
    target_purchase_country = Column(String(100), nullable=True)  # Where buyer wants to acquire land/property
    latitude = Column(Float)  # Auto-populated based on location
    longitude = Column(Float)  # Auto-populated based on location
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # Admin privileges
    profile_image = Column(String(500), nullable=True)  # User profile image URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    properties = relationship("Property", back_populates="owner")
    consultations = relationship("Consultation", back_populates="user")

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False)
    listing_type = Column(String(20), default="sale")  # "sale" or "rent"
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqft = Column(Float)
    price = Column(Float, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    video_url = Column(String(500), nullable=True)
    foreign_buyer_eligible = Column(Boolean, default=True)  # True if foreign nationals / NRIs can purchase
    is_available = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property")

class PropertyImage(Base):
    __tablename__ = "property_images"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    property = relationship("Property", back_populates="images")

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    company = Column(String(255))
    property_count = Column(String(50))
    property_types = Column(Text)  # JSON string of selected types
    challenges = Column(Text)  # JSON string of selected challenges
    features = Column(Text)  # JSON string of selected features
    budget = Column(String(50))
    timeline = Column(String(50))
    current_software = Column(String(255))
    team_size = Column(String(50))
    preferred_contact = Column(String(50))
    additional_info = Column(Text)
    status = Column(String(50), default="pending")  # pending, contacted, closed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="consultations")

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(String(100), nullable=False)  # electrician, plumber, maid, etc.
    property_id = Column(Integer, ForeignKey("properties.id"))
    description = Column(Text, nullable=False)
    urgency = Column(String(50), default="medium")  # low, medium, high, emergency
    status = Column(String(50), default="pending")  # pending, assigned, in_progress, completed
    scheduled_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    property = relationship("Property")

class ConsultantProfile(Base):
    __tablename__ = "consultant_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    license_number = Column(String(100))
    years_experience = Column(Integer, default=0)
    specialization = Column(String(255))  # residential, commercial, etc.
    total_sales_volume = Column(Float, default=0.0)
    properties_sold = Column(Integer, default=0)
    average_sale_price = Column(Float, default=0.0)
    client_satisfaction = Column(Float, default=0.0)  # percentage
    primary_email = Column(String(255))
    primary_phone = Column(String(20))
    mobile_phone = Column(String(20))
    fax_number = Column(String(20))
    website = Column(String(255))
    business_address = Column(String(500))
    years_in_business = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    client_type = Column(String(50))  # buyer, seller, investor, etc.
    status = Column(String(50), default="active")  # active, prospect, closed
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    consultant = relationship("User")

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    source = Column(String(50))  # website, referral, social_media, etc.
    status = Column(String(50), default="new")  # new, contacted, qualified, proposal, negotiation, closed_won, closed_lost
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    consultant = relationship("User")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String(255), nullable=False)
    description = Column(Text)
    service_rate = Column(String(50))  # percentage or fixed amount
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    consultant = relationship("User")

class ConsultationRequest(Base):
    __tablename__ = "consultation_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    consultant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    property_address = Column(String(500), nullable=False)
    consultation_type = Column(String(100), nullable=False)  # property_valuation, market_analysis, etc.
    description = Column(Text)
    preferred_date = Column(DateTime(timezone=True))
    preferred_time = Column(String(50))  # morning, afternoon, evening, flexible
    scheduled_date = Column(DateTime(timezone=True))
    scheduled_time = Column(String(50))
    status = Column(String(50), default="pending")  # pending, accepted, rejected, scheduled, completed, cancelled
    owner_name = Column(String(100))
    owner_email = Column(String(255))
    owner_phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    consultant = relationship("User", foreign_keys=[consultant_id])
    owner = relationship("User", foreign_keys=[owner_id])

class VisitorInfo(Base):
    __tablename__ = "visitor_info"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    looking_for = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User")

