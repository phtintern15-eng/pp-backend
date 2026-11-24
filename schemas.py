from typing import Optional, List, Any
from datetime import datetime
from models import UserType, PropertyType

EmailStr = str

class BaseModel:
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

    @classmethod
    def from_orm(cls, obj):
        kwargs = {}
        for k in dir(obj):
            if not k.startswith('_'):
                try:
                    kwargs[k] = getattr(obj, k)
                except Exception:
                    pass
        return cls(**kwargs)

    def __getattr__(self, item):
        return None


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_type: UserType
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
    user_type: Optional[UserType] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    profile_image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Property Schemas
class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    property_type: PropertyType
    listing_type: Optional[str] = "sale"  # "sale" or "rent"
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    price: float
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
    property_type: Optional[PropertyType] = None
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

class PropertyImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: bool

    class Config:
        from_attributes = True

class PropertyResponse(PropertyBase):
    id: int
    foreign_buyer_eligible: Optional[bool] = True
    is_available: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    images: List[PropertyImageResponse] = []
    
    class Config:
        from_attributes = True

# Consultation Schemas
class ConsultationBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    property_count: str
    property_types: List[str]
    challenges: List[str]
    features: List[str]
    budget: Optional[str] = None
    timeline: Optional[str] = None
    current_software: Optional[str] = None
    team_size: Optional[str] = None
    preferred_contact: str
    additional_info: Optional[str] = None

class ConsultationCreate(ConsultationBase):
    pass

class ConsultationResponse(ConsultationBase):
    id: int
    user_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Service Request Schemas
class ServiceRequestBase(BaseModel):
    service_type: str
    property_id: Optional[int] = None
    description: str
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

class ServiceRequestResponse(ServiceRequestBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Consultant Profile Schemas
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

class ConsultantProfileCreate(ConsultantProfileBase):
    pass

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

class ConsultantProfileResponse(ConsultantProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Client Schemas
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

class ClientResponse(ClientBase):
    id: int
    consultant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Lead Schemas
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

class LeadResponse(LeadBase):
    id: int
    consultant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Service Schemas
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

class ServiceResponse(ServiceBase):
    id: int
    consultant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Consultation Request Schemas
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

class ConsultationRequestUpdate(BaseModel):
    title: Optional[str] = None
    property_address: Optional[str] = None
    consultation_type: Optional[str] = None
    description: Optional[str] = None
    preferred_date: Optional[datetime] = None
    preferred_time: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    scheduled_time: Optional[str] = None
    status: Optional[str] = None

class ConsultationRequestResponse(ConsultationRequestBase):
    id: int
    consultant_id: int
    owner_id: int
    status: str
    scheduled_date: Optional[datetime] = None
    scheduled_time: Optional[str] = None
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    owner_phone: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Visitor Info Schemas
class VisitorInfoCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    looking_for: Optional[str] = None

class VisitorInfoResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    looking_for: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True


# Session Schemas
class SessionUser(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    user_type: str
    is_admin: bool = False
    is_active: bool = True
    company: Optional[str] = None
    location: Optional[str] = None

class SessionInfoResponse(BaseModel):
    authenticated: bool
    session_active: bool
    user: Optional[SessionUser] = None
