"""
backend/schemas.py
Data validation schemas for request body parsing.
Provides lightweight Pydantic-compatible dataclasses without external overhead.
"""
from typing import Optional, List
from datetime import datetime

EmailStr = str

class BaseModel:
    """Lightweight dictionary-backed schema model compatible with FastAPI/Pydantic syntax."""
    def __init__(self, **kwargs):
        self._raw_kwargs = dict(kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def dict(self, exclude_unset=False):
        if exclude_unset:
            return {k: v for k, v in self._raw_kwargs.items() if not k.startswith('_')}
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def model_dump(self, *args, **kwargs):
        return self.dict(*args, **kwargs)

    def __getattr__(self, item):
        return None


# ==============================================================================
# User Schemas
# ==============================================================================
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_type: str = "buyer"
    company: Optional[str] = None
    property_count: Optional[str] = None
    location: Optional[str] = None
    subscription_plan: Optional[str] = None
    citizenship_status: Optional[str] = None
    residence_country: Optional[str] = None
    target_purchase_country: Optional[str] = None
    profile_image: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    profile_image: Optional[str] = None
    user_type: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: Optional[int] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ==============================================================================
# Property Schemas
# ==============================================================================
class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    property_type: str = "RESIDENTIAL"
    listing_type: Optional[str] = "sale"
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    price: float = 0.0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    video_url: Optional[str] = None
    foreign_buyer_eligible: Optional[bool] = True

class PropertyCreate(PropertyBase):
    is_available: Optional[bool] = True
    image_urls: Optional[List[str]] = []

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    property_type: Optional[str] = None
    listing_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    price: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    video_url: Optional[str] = None
    foreign_buyer_eligible: Optional[bool] = None
    is_available: Optional[bool] = None
    image_urls: Optional[List[str]] = None


# ==============================================================================
# Consultation Schemas
# ==============================================================================
class ConsultationBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    property_count: Optional[str] = None
    property_types: Optional[List[str]] = None
    challenges: Optional[List[str]] = None
    features: Optional[List[str]] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    current_software: Optional[str] = None
    team_size: Optional[str] = None
    preferred_contact: Optional[str] = None
    additional_info: Optional[str] = None

class ConsultationCreate(ConsultationBase):
    pass


# ==============================================================================
# Service Request Schemas
# ==============================================================================
class ServiceRequestBase(BaseModel):
    service_type: str
    property_id: Optional[int] = None
    description: str = ""
    urgency: str = "medium"
    scheduled_date: Optional[datetime] = None

class ServiceRequestCreate(ServiceRequestBase):
    pass

class ServiceRequestUpdate(BaseModel):
    service_type: Optional[str] = None
    property_id: Optional[int] = None
    description: Optional[str] = None
    urgency: Optional[str] = None
    status: Optional[str] = None
    scheduled_date: Optional[datetime] = None


# ==============================================================================
# Authentication & Session Token Schemas
# ==============================================================================
class TokenData(BaseModel):
    email: Optional[str] = None


# ==============================================================================
# Consultant Profile Schemas
# ==============================================================================
class ConsultantProfileBase(BaseModel):
    license_number: Optional[str] = None
    years_experience: Optional[int] = 0
    specialization: Optional[str] = None
    total_sales_volume: Optional[float] = 0.0
    properties_sold: Optional[int] = 0
    average_sale_price: Optional[float] = 0.0
    client_satisfaction: Optional[float] = 0.0
    primary_email: Optional[str] = None
    primary_phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    fax_number: Optional[str] = None
    website: Optional[str] = None
    business_address: Optional[str] = None
    years_in_business: Optional[int] = 0

class ConsultantProfileUpdate(BaseModel):
    license_number: Optional[str] = None
    years_experience: Optional[int] = None
    specialization: Optional[str] = None
    total_sales_volume: Optional[float] = None
    properties_sold: Optional[int] = None
    average_sale_price: Optional[float] = None
    client_satisfaction: Optional[float] = None
    primary_email: Optional[str] = None
    primary_phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    fax_number: Optional[str] = None
    website: Optional[str] = None
    business_address: Optional[str] = None
    years_in_business: Optional[int] = None


# ==============================================================================
# Client & Lead Schemas
# ==============================================================================
class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    client_type: Optional[str] = None
    status: Optional[str] = "active"
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    client_type: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = "new"
    notes: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


# ==============================================================================
# Service & Consultation Request Schemas
# ==============================================================================
class ServiceBase(BaseModel):
    service_name: str
    description: Optional[str] = None
    service_rate: Optional[str] = None
    is_active: Optional[bool] = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    description: Optional[str] = None
    service_rate: Optional[str] = None
    is_active: Optional[bool] = None

class ConsultationRequestBase(BaseModel):
    title: str
    property_address: str
    consultation_type: str
    description: Optional[str] = None
    preferred_date: Optional[datetime] = None
    preferred_time: Optional[str] = None

class ConsultationRequestCreate(ConsultationRequestBase):
    consultant_id: int
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    owner_phone: Optional[str] = None


# ==============================================================================
# Visitor Inquiry Schema
# ==============================================================================
class VisitorInfoCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    looking_for: Optional[str] = None

# Backward compatibility aliases
PropertyResponse = PropertyBase
ConsultationResponse = ConsultationBase
ServiceRequestResponse = ServiceRequestBase
ConsultantProfileResponse = ConsultantProfileBase
ClientResponse = ClientBase
LeadResponse = LeadBase
ServiceResponse = ServiceBase
ConsultationRequestResponse = ConsultationRequestBase
VisitorInfoResponse = VisitorInfoCreate
Token = BaseModel
LoginRequest = BaseModel
MessageResponse = BaseModel
SessionUser = BaseModel
SessionInfoResponse = BaseModel
