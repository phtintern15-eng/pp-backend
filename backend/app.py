# Prime Property Platform - Pure Flask WSGI Web Application
import json, os, random, re, sys, time, traceback, bcrypt
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from flask import Flask, g, jsonify, make_response, request, send_from_directory, session
from flask_cors import CORS
from jose import JWTError, jwt
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException as WerkzeugHTTPException
try: import psutil
except ImportError: psutil = None
for p in (os.path.dirname(os.path.abspath(__file__)), os.path.dirname(os.path.dirname(os.path.abspath(__file__)))): (sys.path.insert(0, p) if p not in sys.path else None)
from config import config
from database import Base, SessionLocal, engine
from models import Client, ConsultantProfile, Consultation, ConsultationRequest, Lead, Property, PropertyImage, Service, ServiceRequest, User, UserSession, VisitorInfo
from schemas import (BaseModel, ClientCreate, ClientUpdate, ConsultantProfileUpdate, ConsultationCreate, ConsultationRequestCreate,
                     LeadCreate, LeadUpdate, PropertyCreate, PropertyUpdate, ServiceCreate, ServiceRequestCreate, ServiceRequestUpdate, ServiceUpdate, TokenData, UserCreate, UserUpdate)
active_sessions: Dict[int, datetime] = {}
SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES = config.SECRET_KEY, config.ALGORITHM, config.ACCESS_TOKEN_EXPIRE_MINUTES
FRONTEND_DIR, CSS_DIR, JS_DIR, IMAGES_DIR, UPLOADS_DIR = map(os.path.abspath, (config.FRONTEND_DIR, config.CSS_DIR, config.JS_DIR, config.IMAGES_DIR, config.UPLOADS_DIR))
os.makedirs(UPLOADS_DIR, exist_ok=True)
app = Flask(__name__, template_folder=FRONTEND_DIR, static_folder=None); application = app
if config.BEHIND_PROXY:
    try: from werkzeug.middleware.proxy_fix import ProxyFix; app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    except Exception as e: print(f"ProxyFix note: {e}")
CORS(app, supports_credentials=True)
app.config.update(SECRET_KEY=config.SECRET_KEY, DEBUG=config.DEBUG, SESSION_COOKIE_NAME=config.SESSION_COOKIE_NAME, SESSION_COOKIE_SECURE=config.SESSION_COOKIE_SECURE,
                   SESSION_COOKIE_HTTPONLY=config.SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE=config.SESSION_COOKIE_SAMESITE, PERMANENT_SESSION_LIFETIME=config.PERMANENT_SESSION_LIFETIME)
Base.metadata.create_all(bind=engine)
@app.before_request
def setup_db_session(): g.db = None if request.path.startswith(("/css/", "/js/", "/images/", "/uploads/", "/static/")) or request.path == "/favicon.ico" else SessionLocal()
@app.teardown_request
def teardown_db_session(exc=None):
    try: (g.db.rollback() if exc else None); (g.db.close() if getattr(g, "db", None) else None)
    except Exception: pass
@app.after_request
def add_no_cache_headers(resp):
    resp.headers.update({"Cache-Control": "no-cache, no-store, must-revalidate, max-age=0", "Pragma": "no-cache", "Expires": "0"}); return resp
def _rb():
    try: (g.db.rollback() if getattr(g, "db", None) else None)
    except Exception: pass
class HTTPException(Exception):
    def __init__(self, status_code=400, detail=None, headers=None): super().__init__(detail); self.status_code, self.detail, self.headers = status_code, detail or "An error occurred", headers or {}
class status: HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR = 400, 401, 403, 404, 500
@app.errorhandler(WerkzeugHTTPException)
def handle_werkzeug(exc): return jsonify({"detail": exc.description, "error": exc.description}), exc.code
@app.errorhandler(HTTPException)
def handle_custom_http(exc):
    _rb(); d = getattr(exc, "detail", None) or getattr(exc, "description", str(exc)); r = jsonify({"detail": d, "error": d}); r.status_code = getattr(exc, "status_code", 400); r.headers.update(getattr(exc, "headers", None) or {}); return r
@app.errorhandler(Exception)
def handle_unexpected(exc): _rb(); traceback.print_exc(); d = getattr(exc, "description", None) or str(exc) or "Internal Server Error"; return jsonify({"detail": d, "error": d}), 500
def serialize_model(obj: Any) -> Any:
    if obj is None or isinstance(obj, (int, float, str, bool)): return obj
    if isinstance(obj, datetime): return obj.isoformat()
    if hasattr(obj, "dict") and callable(obj.dict): return serialize_model(obj.dict())
    if hasattr(obj, "to_dict") and callable(obj.to_dict): return serialize_model(obj.to_dict())
    if hasattr(obj, "__table__"):
        res = {col.name: getattr(obj, col.name).isoformat() if isinstance(getattr(obj, col.name), datetime) else (getattr(obj, col.name).value if hasattr(getattr(obj, col.name), "value") else getattr(obj, col.name)) for col in obj.__table__.columns}
        if hasattr(obj, "images"): res["images"] = [serialize_model(img) for img in getattr(obj, "images", [])]
        if hasattr(obj, "owner") and getattr(obj, "owner", None):
            ow = obj.owner; fn = f"{getattr(ow, 'first_name', '') or ''} {getattr(ow, 'last_name', '') or ''}".strip() or getattr(ow, "email", "Verified Owner")
            res.update({"owner_name": fn, "owner_email": getattr(ow, "email", None), "owner_phone": getattr(ow, "phone_number", None), "owner_type": getattr(ow, "user_type", "owner"), "owner": {"id": getattr(ow, "id", None), "name": fn, "email": getattr(ow, "email", None), "phone_number": getattr(ow, "phone_number", None), "user_type": getattr(ow, "user_type", "owner")}})
        return res
    if isinstance(obj, dict): return {k: serialize_model(v) for k, v in obj.items()}
    return [serialize_model(x) for x in obj] if isinstance(obj, (list, tuple, set)) else str(obj)
def to_response(result: Any): return (jsonify(serialize_model(result[0])), result[1]) if isinstance(result, tuple) and len(result) == 2 else jsonify(serialize_model(result))
def verify_password(plain: str, hashed: str) -> bool:
    try: return bool(plain and hashed) and bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8")) or False
    except Exception: return False
def get_password_hash(plain: str) -> str: return bcrypt.hashpw(plain.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str: return jwt.encode(dict(data, exp=datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))), SECRET_KEY, algorithm=ALGORITHM)
def verify_token(token: str, cred_exc: HTTPException) -> TokenData:
    try:
        sub = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if sub: return TokenData(email=sub)
    except JWTError: pass
    raise cred_exc
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    if not email: return None
    c = str(email).strip()
    return db.query(User).filter(User.email == c).first() or db.query(User).filter(func.lower(User.email) == c.lower()).first() or ((c.lower() in ("admin", "administrator")) and db.query(User).filter(User.email == "admin@primeproperties.com").first()) or None
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    u = get_user_by_email(db, email); return u if (u and verify_password(password, u.hashed_password)) else None
def get_current_user_from_request(db: Session) -> User:
    ah, tok = request.headers.get("Authorization", ""), None
    tok = ah[7:].strip() if ah.startswith("Bearer ") else request.cookies.get("access_token")
    cred_exc, u = HTTPException(401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"}), None
    if tok:
        try: u = get_user_by_email(db, email=verify_token(tok, cred_exc).email)
        except Exception: pass
    if not u:
        sid, sem = session.get("user_id"), session.get("user_email")
        u = db.query(User).filter(User.id == sid).first() if sid else (get_user_by_email(db, email=sem) if sem else None)
    if not u: raise cred_exc
    active_sessions[u.id] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES); return u
def get_current_active_user_from_request(db: Session) -> User:
    u = get_current_user_from_request(db)
    if not u.is_active: raise HTTPException(400, "Inactive user")
    return u
def get_user_type_str(u: User) -> str: return getattr(u.user_type, "value", str(u.user_type)) if u.user_type else "user"
def is_admin_or_staff(u: User) -> bool: return bool(u and (u.is_admin or get_user_type_str(u) in ["admin", "consultant"]))
def require_admin(u: Optional[User] = None) -> User:
    curr = u or get_current_user_from_request(g.db)
    if not is_admin_or_staff(curr): raise HTTPException(403, "Access denied. Admin access only.")
    return curr
def set_user_flask_session(u: User): session.permanent = True; session.update({"user_id": u.id, "user_email": u.email, "user_type": get_user_type_str(u), "is_admin": bool(u.is_admin)})
def get_coordinates_for_city(city: Optional[str]): return {"bangalore": (12.9716, 77.5946), "mumbai": (19.0760, 72.8777), "delhi": (28.7041, 77.1025), "hyderabad": (17.3850, 78.4867), "pune": (18.5204, 73.8567), "chennai": (13.0827, 80.2707), "coimbatore": (11.0168, 76.9558), "kochi": (9.9312, 76.2673), "kolkata": (22.5726, 88.3639), "ahmedabad": (23.0225, 72.5714), "jaipur": (26.9124, 75.7873), "surat": (21.1702, 72.8311), "lucknow": (26.8467, 80.9462), "kanpur": (26.4499, 80.3319), "nagpur": (21.1458, 79.0882), "indore": (22.7196, 75.8577), "thane": (19.2183, 72.9781), "bhopal": (23.2599, 77.4126), "visakhapatnam": (17.6868, 83.2185), "noida": (28.5355, 77.3910)}.get(city.lower().strip() if city else "", (None, None))
@app.route("/<folder>/<path:filename>")
@app.route("/static/<folder>/<path:filename>")
def serve_asset(folder, filename):
    d = {"css": CSS_DIR, "styles": CSS_DIR, "js": JS_DIR, "images": IMAGES_DIR, "uploads": UPLOADS_DIR}.get(folder)
    return send_from_directory(d, filename) if (d and os.path.exists(os.path.join(d, filename))) else ("Not Found", 404)
@app.route("/favicon.ico")
def favicon(): return send_from_directory(IMAGES_DIR, "favicon.ico", mimetype="image/vnd.microsoft.icon")
PAGES = [("", "index.html"), ("about", "about.html"), ("foreign-investors", "foreign_investors.html"), ("foreign-buyers", "foreign_investors.html"), ("property", "properties.html"), ("properties", "properties.html"), ("pricing", "pricing.html"), ("service", "service.html"), ("service-requests", "service_requests.html"), ("service_requests", "service_requests.html"), ("investment-dashboard", "investment_dashboard.html"), ("owner-profile", "owner_profile.html"), ("consultant-profile", "consultant_profile.html"), ("admin-dashboard", "admin_dashboard.html"), ("user-dashboard", "user_dashboard.html"), ("analytics", "analytics.html"), ("notifications", "notifications.html"), ("users", "users.html"), ("owners", "owners.html"), ("admin-properties", "admin_properties.html"), ("admin_properties", "admin_properties.html"), ("admin/properties", "admin_properties.html"), ("revenue", "revenue.html"), ("invoices", "invoices.html"), ("reports", "reports.html"), ("maintenance", "maintenance.html"), ("settings", "settings.html"), ("security", "security.html"), ("backup", "settings.html"), ("owner-properties", "owner_profile.html"), ("owner-tenants", "owner_profile.html"), ("login", "login.html"), ("register", "register.html"), ("client-login", "login.html"), ("portal-login", "login.html")]
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
def serve_page(page_file: str):
    for d in (FRONTEND_DIR, TEMPLATES_DIR):
        if os.path.exists(os.path.join(d, page_file)): return send_from_directory(d, page_file)
    return "Page Not Found", 404
for r, pf in PAGES: app.add_url_rule(f"/{r}" if r else "/", f"page_{r or 'root'}", (lambda p=pf: serve_page(p)))
@app.route("/<path:p>.html")
def fallback_html(p): return serve_page(f"{p}.html")
@app.route("/api/auth/register", methods=["POST"])
def register():
    db, ud = g.db, UserCreate(**(request.get_json(silent=True) or {}))
    if not ud.email or not ud.password: raise HTTPException(400, "Email and password are required")
    if get_user_by_email(db, ud.email): raise HTTPException(400, "Email already registered")
    lat, lng = get_coordinates_for_city(ud.location) if ud.location else (None, None)
    u = User(**{k: v for k, v in ud.dict().items() if k != "password"}, latitude=lat, longitude=lng, hashed_password=get_password_hash(ud.password))
    db.add(u); db.commit(); db.refresh(u); return to_response(u)
@app.route("/api/auth/login", methods=["POST"])
def login():
    db, d = g.db, request.get_json(silent=True) or {}
    u = authenticate_user(db, (d.get("email") or "").strip(), d.get("password") or "")
    if not u: raise HTTPException(401, "Incorrect email or password", {"WWW-Authenticate": "Bearer"})
    exp_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES); tok, exp = create_access_token({"sub": u.email}, exp_delta), datetime.utcnow() + exp_delta; active_sessions[u.id] = exp; set_user_flask_session(u)
    try: db.add(UserSession(user_id=u.id, session_token=tok, ip_address=request.remote_addr, user_agent=(request.headers.get("User-Agent") or "")[:255], expires_at=exp, is_active=True)); db.commit()
    except Exception as e: print(f"UserSession DB note: {e}")
    resp = make_response(jsonify({"access_token": tok, "token_type": "bearer", "user": {"id": u.id, "email": u.email, "first_name": u.first_name, "last_name": u.last_name, "user_type": get_user_type_str(u), "is_admin": bool(u.is_admin)}}))
    resp.set_cookie("access_token", tok, max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60, httponly=False, samesite="Lax", path="/"); return resp
@app.route("/api/auth/login-form", methods=["POST"])
def login_form():
    u = authenticate_user(g.db, request.form.get("username"), request.form.get("password"))
    if not u: raise HTTPException(401, "Incorrect email or password", {"WWW-Authenticate": "Bearer"})
    tok = create_access_token({"sub": u.email}); active_sessions[u.id] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES); set_user_flask_session(u); return to_response({"access_token": tok, "token_type": "bearer"})
@app.route("/api/auth/session", methods=["GET"])
def get_session_status():
    try:
        u = get_current_user_from_request(g.db)
        return to_response({"authenticated": True, "session_active": True, "user": {"id": u.id, "email": u.email, "first_name": u.first_name, "last_name": u.last_name, "user_type": get_user_type_str(u), "is_admin": bool(u.is_admin), "is_active": bool(u.is_active), "company": u.company, "location": u.location}})
    except HTTPException: return to_response({"authenticated": False, "session_active": False, "user": None})
@app.route("/api/auth/logout", methods=["POST", "GET"])
def logout():
    uid = session.get("user_id") or (getattr(g, "db", None) and getattr(get_current_user_from_request(g.db), "id", None) if session.get("user_id") is None else None)
    if uid:
        active_sessions.pop(uid, None)
        try: g.db.query(UserSession).filter(UserSession.user_id == uid, UserSession.is_active == True).update({"is_active": False}); g.db.commit()
        except Exception: pass
    session.clear(); resp = make_response(jsonify({"message": "Successfully logged out", "status": "logged_out"}))
    resp.delete_cookie("access_token", path="/"); resp.delete_cookie(app.config.get("SESSION_COOKIE_NAME", "prime_session"), path="/"); return resp
@app.route("/api/visitor-info", methods=["POST"])
def create_visitor_info():
    d = request.get_json(silent=True) or {}; v = VisitorInfo(full_name=d.get("full_name") or d.get("name") or d.get("fullName") or "Anonymous Inquirer", email=d.get("email") or "inquiry@primeproperties.com", phone=d.get("phone") or "", looking_for=d.get("looking_for") or "")
    g.db.add(v); g.db.commit(); g.db.refresh(v); return to_response(v)
@app.route("/api/user/dashboard-summary", methods=["GET"])
def get_user_dashboard_summary():
    db, u = g.db, get_current_user_from_request(g.db)
    u_cons, u_reqs = db.query(Consultation).filter(Consultation.user_id == u.id).all(), db.query(ServiceRequest).filter(ServiceRequest.user_id == u.id).all()
    curated = [{"id": p.id, "title": p.title, "price": p.price, "city": p.city, "state": p.state, "bedrooms": p.bedrooms, "bathrooms": p.bathrooms, "square_feet": p.area_sqft, "area_sqft": p.area_sqft, "property_type": get_user_type_str(p), "featured_image": p.images[0].image_url if p.images else "/images/luxury_villa.png"} for p in db.query(Property).filter(Property.is_available == True).order_by(Property.created_at.desc()).limit(6).all()]
    return to_response({"user": {"id": u.id, "first_name": u.first_name, "last_name": u.last_name, "email": u.email, "phone": u.phone or "", "user_type": get_user_type_str(u), "location": u.location or "", "is_admin": u.is_admin}, "stats": {"active_inquiries": len(u_cons), "service_requests": len(u_reqs), "available_properties": db.query(Property).filter(Property.is_available == True).count(), "portfolio_status": "VIP Premium Client"}, "recent_consultations": [{"id": c.id, "company": c.company or "Private Investor", "budget": c.budget or "Flexible", "timeline": c.timeline or "Immediate", "status": c.status or "In Review", "created_at": c.created_at.isoformat() if getattr(c, "created_at", None) else None} for c in u_cons[:5]], "recent_service_requests": [{"id": r.id, "service_type": r.service_type, "status": r.status, "preferred_date": r.scheduled_date.isoformat() if getattr(r, "scheduled_date", None) else None, "notes": r.description or ""} for r in u_reqs[:5]], "curated_listings": curated})
@app.route("/api/users/me", methods=["GET", "PUT", "DELETE"])
def current_user_route():
    db, u = g.db, get_current_user_from_request(g.db)
    if request.method == "GET": return to_response(u)
    if request.method == "DELETE": u.is_active = False; db.commit(); return to_response({"message": "Account deactivated successfully"})
    d = UserUpdate(**(request.get_json(silent=True) or {})).dict(exclude_unset=True)
    for k, v in d.items(): setattr(u, k, v)
    db.commit(); db.refresh(u); return to_response(u)
@app.route("/api/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    db, now, res = g.db, datetime.utcnow(), []; get_current_user_from_request(db)
    for u in db.query(User).filter(User.user_type != "admin", User.is_admin == False).offset(request.args.get("skip", 0, type=int)).limit(request.args.get("limit", 100, type=int)).all():
        is_on = (u.id in active_sessions and active_sessions[u.id] >= now) or bool(db.query(UserSession).filter(UserSession.user_id == u.id, UserSession.is_active == True, UserSession.expires_at >= now).first())
        res.append(dict({c.name: getattr(u, c.name).isoformat() if isinstance(getattr(u, c.name), datetime) else getattr(u, c.name) for c in u.__table__.columns if c.name != "hashed_password"}, is_online=is_on, session_status="online" if is_on else "offline"))
    return to_response(res)
@app.route("/api/admin/users", methods=["POST"])
def create_user_by_admin():
    db, u, d = g.db, require_admin(), UserCreate(**(request.get_json(silent=True) or {}))
    if get_user_type_str(u) != "admin": raise HTTPException(403, "Access denied. Admin access only.")
    if get_user_by_email(db, d.email): raise HTTPException(400, "Email already registered")
    if d.user_type == "admin": raise HTTPException(403, "Cannot create admin users through this endpoint")
    lat, lng = get_coordinates_for_city(d.location) if d.location else (None, None)
    new_u = User(**{k: v for k, v in d.dict().items() if k != "password"}, latitude=lat, longitude=lng, hashed_password=get_password_hash(d.password), is_active=True)
    db.add(new_u); db.commit(); db.refresh(new_u); return to_response(new_u)
@app.route("/api/admin/users/<int:user_id>", methods=["PUT", "DELETE"])
def modify_user_by_admin(user_id):
    db, u, target = g.db, require_admin(), g.db.query(User).get(user_id)
    if get_user_type_str(u) != "admin": raise HTTPException(403, "Access denied. Admin access only.")
    if not target: raise HTTPException(404, "User not found")
    if get_user_type_str(target) == "admin" or target.is_admin: raise HTTPException(403, "Cannot edit or delete admin users")
    if request.method == "DELETE":
        for p in db.query(Property).filter(Property.owner_id == user_id): db.query(PropertyImage).filter(PropertyImage.property_id == p.id).delete(); db.delete(p)
        for M in (Consultation, ServiceRequest, ConsultantProfile): db.query(M).filter(M.user_id == user_id).delete()
        db.delete(target); db.commit(); return to_response({"message": "User deleted successfully"})
    d = UserUpdate(**(request.get_json(silent=True) or {})).dict(exclude_unset=True)
    if "email" in d and d["email"] != target.email and db.query(User).filter(User.email == d["email"], User.id != user_id).first(): raise HTTPException(400, "Email already registered")
    for k, v in d.items(): setattr(target, k, v)
    db.commit(); db.refresh(target); return to_response(target)
@app.route("/api/admin/users/stats", methods=["GET"])
def get_admin_users_stats():
    db, u = g.db, require_admin()
    if get_user_type_str(u) != "admin": raise HTTPException(403, "Access denied. Admin access only.")
    base = db.query(User).filter(User.user_type != "admin", User.is_admin == False)
    tot, act, inact = base.count(), base.filter(User.is_active == True).count(), base.filter(User.is_active == False).count()
    now = datetime.now(); ms = datetime(now.year, now.month, 1); lms = datetime(now.year, now.month - 1, 1) if now.month > 1 else datetime(now.year - 1, 12, 1)
    tm, lm = base.filter(User.created_at >= ms).count(), base.filter(User.created_at >= lms, User.created_at < ms).count()
    act_tm, act_lm = base.filter(User.is_active == True, User.created_at >= ms).count(), base.filter(User.is_active == True, User.created_at >= lms, User.created_at < ms).count()
    return to_response({"total_users": tot, "active_users": act, "inactive_users": inact, "monthly_change": tm - lm, "active_monthly_change": act_tm - act_lm, "inactive_monthly_change": base.filter(User.is_active == False, User.created_at >= ms).count() - base.filter(User.is_active == False, User.created_at >= lms, User.created_at < ms).count()})
@app.route("/api/owner/profile", methods=["GET", "PUT"])
def owner_profile():
    db, u = g.db, check_role("owner")
    if request.method == "GET": return to_response(u)
    d = request.get_json(silent=True) or {}; [setattr(u, k, d[k]) for k in ("first_name", "last_name", "email", "phone", "company", "location", "profile_image") if k in d]
    db.commit(); db.refresh(u); return to_response({"message": "Profile updated successfully", "user": {col.name: getattr(u, col.name) for col in u.__table__.columns if col.name != "hashed_password"}})
@app.route("/api/owner/properties", methods=["GET"])
def get_owner_properties(): return to_response(g.db.query(Property).filter(Property.owner_id == check_role("owner").id).all())
@app.route("/api/owner/stats", methods=["GET"])
def get_owner_stats():
    u = check_role("owner")
    props = g.db.query(Property).filter(Property.owner_id == u.id).all(); tot, tot_val = len(props), sum((p.price for p in props if p.price))
    return to_response({"total_properties": tot, "total_value": tot_val, "available_properties": len([p for p in props if p.is_available]), "avg_property_value": tot_val / tot if tot else 0, "properties_by_type": {"residential": len([p for p in props if p.property_type == "residential"]), "commercial": len([p for p in props if p.property_type == "commercial"]), "office": len([p for p in props if p.property_type == "office"])}})
@app.route("/api/owner/contact-info", methods=["GET"])
def get_owner_contact_info():
    u = check_role("owner")
    rp = u.phone or ""; pc = rp.replace("+1-", "").replace("-", "").strip()
    return to_response({"primary_email": u.email, "primary_phone": rp, "mobile_phone": rp, "fax_number": f"+1-{pc}-{pc[-4:]}" if len(pc) >= 4 else "+1-800-555-0199", "website": f"www.{u.company.lower().replace(' ', '').replace('llc', '').replace('inc', '')}.com" if u.company else None, "business_name": u.company or "Private Estate Portfolio", "address": u.location or "Bengaluru, India", "years_in_business": 5})
@app.route("/api/properties", methods=["GET", "POST"], strict_slashes=False)
def properties_root():
    db = g.db
    if request.method == "POST":
        u, pd = get_current_user_from_request(db), PropertyCreate(**(request.get_json(silent=True) or {})).dict()
        imgs, prop = pd.pop("image_urls", []) or [], Property(**pd, owner_id=u.id); db.add(prop); db.commit(); db.refresh(prop)
        for idx, iu in enumerate(imgs): (db.add(PropertyImage(property_id=prop.id, image_url=iu.strip(), is_primary=idx == 0)) if iu and iu.strip() else None)
        if imgs: db.commit(); db.refresh(prop)
        return to_response(prop)
    q = db.query(Property)
    for p, c, fn in [("property_type", Property.property_type, lambda q, v: q.filter(c == v)), ("city", Property.city, lambda q, v: q.filter(c.ilike(f"%{v}%"))), ("min_price", Property.price, lambda q, v: q.filter(c >= v)), ("max_price", Property.price, lambda q, v: q.filter(c <= v))]: q = fn(q, request.args.get(p)) if request.args.get(p) else q
    return to_response(q.order_by(Property.id.desc()).offset(request.args.get("skip", 0, type=int)).limit(request.args.get("limit", 100, type=int)).all())
@app.route("/api/properties/my-properties", methods=["GET"])
def get_my_properties(): return to_response(g.db.query(Property).filter(Property.owner_id == get_current_user_from_request(g.db).id).all())
@app.route("/api/properties/<int:property_id>", methods=["GET", "PUT", "DELETE"])
def property_detail(property_id):
    db, prop = g.db, g.db.query(Property).get(property_id)
    if not prop: raise HTTPException(404, "Property not found")
    if request.method == "GET": return to_response(prop)
    u = get_current_user_from_request(db)
    if prop.owner_id != u.id and not is_admin_or_staff(u): raise HTTPException(403, "Not enough permissions")
    if request.method == "DELETE": db.delete(prop); db.commit(); return to_response({"message": "Property deleted successfully"})
    d = PropertyUpdate(**(request.get_json(silent=True) or {})).dict(exclude_unset=True); imgs = d.pop("image_urls", None)
    for k, v in d.items(): setattr(prop, k, v)
    if imgs is not None:
        db.query(PropertyImage).filter(PropertyImage.property_id == prop.id).delete()
        [db.add(PropertyImage(property_id=prop.id, image_url=iu.strip(), is_primary=idx == 0)) for idx, iu in enumerate(imgs) if iu and iu.strip()]
    db.commit(); db.refresh(prop); return to_response(prop)
@app.route("/api/properties/upload-media", methods=["POST"])
def upload_property_media():
    u, f = get_current_user_from_request(g.db), request.files.get("file")
    if not f: raise HTTPException(400, "No file uploaded")
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".webm", ".mov", ".m4v"}: raise HTTPException(400, "Unsupported file format")
    name = f"{int(time.time())}_{u.id}_{f.filename.replace(' ', '_')}"
    with open(os.path.join(UPLOADS_DIR, name), "wb") as dst: dst.write(f.read())
    return to_response({"url": f"/static/uploads/{name}", "filename": f.filename, "is_video": ext in {".mp4", ".webm", ".mov", ".m4v"}})
@app.route("/api/consultations", methods=["GET", "POST"], strict_slashes=False)
def consultations_root():
    db, u = g.db, get_current_user_from_request(g.db)
    if request.method == "GET": return to_response(db.query(Consultation).filter(Consultation.user_id == u.id).all())
    cd = ConsultationCreate(**(request.get_json(silent=True) or {})).dict()
    cd.update(property_types=str(cd.get("property_types")), challenges=str(cd.get("challenges")), features=str(cd.get("features")), user_id=u.id)
    c = Consultation(**cd); db.add(c); db.commit(); db.refresh(c); return to_response(c)
@app.route("/api/consultations/<int:cid>", methods=["GET"])
def get_consultation(cid):
    u, c = get_current_user_from_request(g.db), g.db.query(Consultation).filter(Consultation.id == cid).first()
    if not c or (c.user_id != u.id and not is_admin_or_staff(u)): raise HTTPException(404, "Consultation not found")
    return to_response(c)
@app.route("/api/consultations/admin/all", methods=["GET"])
def get_all_consultations():
    require_admin(); q = g.db.query(Consultation)
    if request.args.get("status_filter"): q = q.filter(Consultation.status == request.args.get("status_filter"))
    return to_response(q.offset(request.args.get("skip", 0, type=int)).limit(request.args.get("limit", 100, type=int)).all())
@app.route("/api/consultations/<int:cid>/status", methods=["PUT"])
def update_consultation_status(cid):
    require_admin(); d = request.get_json(silent=True) or {}; st, c = d.get("status") or d.get("new_status") or request.args.get("status") or request.args.get("new_status"), g.db.query(Consultation).get(cid)
    if not c: raise HTTPException(404, "Consultation not found")
    c.status = st; g.db.commit(); return to_response({"message": f"Consultation status updated to {st}"})
@app.route("/api/services", methods=["GET", "POST"], strict_slashes=False)
def services_root():
    db, u = g.db, get_current_user_from_request(g.db)
    if request.method == "GET": return to_response(db.query(ServiceRequest).filter(ServiceRequest.user_id == u.id).all())
    sd = ServiceRequestCreate(**(request.get_json(silent=True) or {})).dict()
    sr = ServiceRequest(**sd, user_id=u.id); db.add(sr); db.commit(); db.refresh(sr); return to_response(sr)
@app.route("/api/services/<int:sid>", methods=["GET", "PUT", "DELETE"])
def service_detail(sid):
    db, u = g.db, get_current_user_from_request(g.db); sr = db.query(ServiceRequest).get(sid)
    if not sr or (sr.user_id != u.id and not is_admin_or_staff(u)): raise HTTPException(404, "Service request not found")
    if request.method == "GET": return to_response(sr)
    if request.method == "DELETE": db.delete(sr); db.commit(); return to_response({"message": "Service request deleted successfully"})
    d = ServiceRequestUpdate(**(request.get_json(silent=True) or {})).dict(exclude_unset=True)
    for k, v in d.items(): setattr(sr, k, v)
    db.commit(); db.refresh(sr); return to_response(sr)
@app.route("/api/services/admin/all", methods=["GET"])
def get_all_services():
    require_admin(); q = g.db.query(ServiceRequest)
    if request.args.get("status_filter"): q = q.filter(ServiceRequest.status == request.args.get("status_filter"))
    if request.args.get("service_type"): q = q.filter(ServiceRequest.service_type == request.args.get("service_type"))
    return to_response(q.offset(request.args.get("skip", 0, type=int)).limit(request.args.get("limit", 100, type=int)).all())

def check_role(role: str) -> User:
    u = get_current_user_from_request(g.db)
    if get_user_type_str(u) != role: raise HTTPException(403, f"Access denied. {role.capitalize()} only.")
    return u
def check_consultant() -> User: return check_role("consultant")
@app.route("/api/consultant/profile", methods=["GET", "PUT"])
def consultant_profile():
    db, u = g.db, check_consultant(); prof = db.query(ConsultantProfile).filter(ConsultantProfile.user_id == u.id).first()
    if not prof: prof = ConsultantProfile(user_id=u.id, primary_email=u.email, primary_phone=u.phone, mobile_phone=u.phone, license_number="Not provided", years_experience=0, specialization="Not specified", total_sales_volume=0.0, properties_sold=0, average_sale_price=0.0, client_satisfaction=0.0); db.add(prof); db.commit(); db.refresh(prof)
    if request.method == "GET": return to_response(prof)
    d = ConsultantProfileUpdate(**(request.get_json(silent=True) or {})).dict(exclude_unset=True)
    for k, v in d.items(): setattr(prof, k, v)
    db.commit(); db.refresh(prof); return to_response(prof)
@app.route("/api/consultant/stats", methods=["GET"])
def get_consultant_stats():
    db, u = g.db, check_consultant(); p = db.query(ConsultantProfile).filter(ConsultantProfile.user_id == u.id).first()
    return to_response({"active_clients": db.query(Client).filter(Client.consultant_id == u.id, Client.status == "active").count(), "total_clients": db.query(Client).filter(Client.consultant_id == u.id).count(), "active_leads": db.query(Lead).filter(Lead.consultant_id == u.id, Lead.status.in_(["new", "contacted", "qualified", "proposal", "negotiation"])).count(), "total_leads": db.query(Lead).filter(Lead.consultant_id == u.id).count(), "properties_sold": p.properties_sold if p else 0, "total_sales_volume": p.total_sales_volume if p else 0, "years_experience": p.years_experience if p else 0, "client_satisfaction": p.client_satisfaction if p else 0})
def crud_consultant(model, item_id=None, create_schema=None, update_schema=None):
    db, u = g.db, check_consultant()
    if request.method == "GET": return to_response(db.query(model).filter(model.consultant_id == u.id).all())
    if request.method == "POST":
        d = (create_schema(**(request.get_json(silent=True) or {})).dict() if create_schema else (request.get_json(silent=True) or {}))
        obj = model(**d, consultant_id=u.id); db.add(obj); db.commit(); db.refresh(obj); return to_response(obj)
    obj = db.query(model).get(item_id)
    if not obj or obj.consultant_id != u.id: raise HTTPException(404, f"{model.__name__} not found")
    if request.method == "DELETE": db.delete(obj); db.commit(); return to_response({"message": f"{model.__name__} deleted successfully"})
    d = (update_schema(**(request.get_json(silent=True) or {})).dict(exclude_unset=True) if update_schema else (request.get_json(silent=True) or {}))
    for k, v in d.items(): setattr(obj, k, v)
    db.commit(); db.refresh(obj); return to_response(obj)
@app.route("/api/consultant/clients", methods=["GET", "POST"])
@app.route("/api/consultant/clients/<int:cid>", methods=["PUT", "DELETE"])
def consultant_clients(cid=None): return crud_consultant(Client, item_id=cid, create_schema=ClientCreate, update_schema=ClientUpdate)
@app.route("/api/consultant/leads", methods=["GET", "POST"])
@app.route("/api/consultant/leads/<int:lid>", methods=["PUT", "DELETE"])
def consultant_leads(lid=None): return crud_consultant(Lead, item_id=lid, create_schema=LeadCreate, update_schema=LeadUpdate)
@app.route("/api/consultant/services", methods=["GET", "POST"])
@app.route("/api/consultant/services/<int:sid>", methods=["PUT", "DELETE"])
def consultant_services(sid=None): return crud_consultant(Service, item_id=sid, create_schema=ServiceCreate, update_schema=ServiceUpdate)
@app.route("/api/consultants", methods=["GET"])
def get_consultants(): return to_response(g.db.query(User).filter(User.user_type == "consultant").all())
@app.route("/api/consultant/consultation-requests", methods=["GET", "POST"])
def consultant_requests():
    db, u = g.db, check_consultant()
    if request.method == "GET": return to_response(db.query(ConsultationRequest).filter(ConsultationRequest.consultant_id == u.id).order_by(desc(ConsultationRequest.created_at)).all())
    d = ConsultationRequestCreate(**(request.get_json(silent=True) or {})).dict(); ow = db.query(User).get(d["consultant_id"])
    if not ow: raise HTTPException(404, "Owner not found")
    cr = ConsultationRequest(**d, owner_id=ow.id, owner_name=f"{ow.first_name} {ow.last_name}", owner_email=ow.email, owner_phone=ow.phone)
    db.add(cr); db.commit(); db.refresh(cr); return to_response(cr)
@app.route("/api/consultant/consultation-requests/<int:rid>", methods=["GET"])
def get_consultation_request_item(rid):
    u, cr = check_consultant(), g.db.query(ConsultationRequest).get(rid)
    if not cr or cr.consultant_id != u.id: raise HTTPException(404, "Consultation request not found")
    return to_response(cr)
@app.route("/api/consultant/consultation-requests/<int:rid>/<act>", methods=["PUT"])
def update_cr_action(rid, act):
    db, u, cr = g.db, check_consultant(), g.db.query(ConsultationRequest).get(rid)
    if not cr or cr.consultant_id != u.id: raise HTTPException(404, "Consultation request not found")
    if act in ("accept", "reject") and cr.status != "pending": raise HTTPException(400, "Only pending requests can be updated")
    if act == "schedule":
        if cr.status != "accepted": raise HTTPException(400, "Only accepted requests can be scheduled")
        d = request.get_json(silent=True) or {}; (setattr(cr, "scheduled_date", datetime.fromisoformat(d["scheduled_date"])) if d.get("scheduled_date") else None); (setattr(cr, "scheduled_time", d["scheduled_time"]) if d.get("scheduled_time") else None)
    elif act == "complete" and cr.status != "scheduled": raise HTTPException(400, "Only scheduled consultations can be completed")
    cr.status, cr.updated_at = {"accept": "accepted", "reject": "rejected", "schedule": "scheduled", "complete": "completed"}.get(act, cr.status), func.now()
    db.commit(); return to_response({"message": f"Consultation request {cr.status}"})

@app.route("/api/admin/dashboard/test", methods=["GET"])
def test_admin_dashboard(): require_admin(); return to_response({"status": "success", "message": "Admin dashboard API is working", "total_users": g.db.query(User).count(), "user_type": get_user_type_str(get_current_user_from_request(g.db))})
@app.route("/api/admin/dashboard/stats", methods=["GET"])
def get_admin_dashboard_stats():
    db, u, tot_u, tot_p = g.db, require_admin(), g.db.query(User).count(), g.db.query(Property).count(); rev = tot_p * 25000
    return to_response({"total_users": tot_u, "total_owners": db.query(User).filter(User.user_type == "owner").count(), "total_consultants": db.query(User).filter(User.user_type == "consultant").count(), "total_properties": tot_p, "active_properties": db.query(Property).filter(Property.is_available == True).count(), "total_consultations": db.query(Consultation).count(), "pending_consultations": db.query(Consultation).filter(Consultation.status == "pending").count(), "total_service_requests": db.query(ServiceRequest).count(), "pending_service_requests": db.query(ServiceRequest).filter(ServiceRequest.status == "pending").count(), "total_revenue": rev, "monthly_revenue": rev // 12, "growth_rate": 15.4, "active_users": db.query(User).filter(User.is_active == True).count(), "online_users": len(active_sessions), "occupancy_rate": 92.5, "collection_rate": 96.8})
@app.route("/api/admin/dashboard/system-metrics", methods=["GET"])
def get_system_metrics():
    require_admin(); cpu_p, mem_mb, mem_p, nth, nco, bw_s, bw_r = 0, 0, 0, 1, 0, 0, 0
    if psutil:
        try:
            p = psutil.Process(os.getpid()); cpu_p, mem, conn, io = p.cpu_percent(0.05) / (psutil.cpu_count() or 1), p.memory_info(), p.connections(), p.io_counters()
            mem_mb, mem_p, nth, nco = mem.rss / 1048576, (mem.rss / psutil.virtual_memory().total) * 100, p.num_threads(), (len(conn) if conn else 0)
            if io: bw_s, bw_r = io.write_bytes / 1048576, io.read_bytes / 1048576
        except Exception as e: print(f"psutil err: {e}")
    return to_response({"cpu": {"usage_percent": round(cpu_p, 2), "cores": psutil.cpu_count() if psutil else 4}, "memory": {"used_mb": round(mem_mb, 2), "used_gb": round(mem_mb / 1024, 2), "percent": round(mem_p, 2), "total_gb": round(psutil.virtual_memory().total / (1024**3), 2) if psutil else 16.0}, "process": {"threads": nth, "connections": nco, "bandwidth_sent_mb": round(bw_s, 2), "bandwidth_recv_mb": round(bw_r, 2)}})
@app.route("/api/admin/dashboard/users", methods=["GET"])
def get_admin_dashboard_users(): require_admin(); return to_response(g.db.query(User).order_by(desc(User.created_at)).limit(5).all())
@app.route("/api/admin/dashboard/consultants", methods=["GET"])
def get_admin_dashboard_consultants():
    db = g.db; require_admin()
    return to_response([{"id": c.id, "name": f"{c.first_name} {c.last_name}", "email": c.email, "phone": c.phone, "specialization": p.specialization if (p := db.query(ConsultantProfile).filter(ConsultantProfile.user_id == c.id).first()) else "Luxury Estates", "clients_count": db.query(Client).filter(Client.consultant_id == c.id).count(), "leads_count": db.query(Lead).filter(Lead.consultant_id == c.id).count(), "rating": p.client_satisfaction if p else 4.9} for c in db.query(User).filter(User.user_type == "consultant").all()])
@app.route("/api/admin/dashboard/activity", methods=["GET"])
def get_admin_dashboard_activity():
    db, s8 = g.db, datetime.now() - timedelta(days=8); require_admin()
    acts = [{"type": "user_registration", "title": "New User Registration", "description": f"{x.first_name} {x.last_name} registered as {x.user_type}", "timestamp": x.created_at, "icon": "fas fa-user-plus"} for x in db.query(User).filter(User.created_at >= s8).order_by(desc(User.created_at)).limit(10)] + [{"type": "property_added", "title": "Property Added", "description": f"New property '{x.title}' added", "timestamp": x.created_at, "icon": "fas fa-building"} for x in db.query(Property).filter(Property.created_at >= s8).order_by(desc(Property.created_at)).limit(10)] + [{"type": "consultation_request", "title": "Consultation Request", "description": f"Consultation request from {x.first_name} {x.last_name}", "timestamp": x.created_at, "icon": "fas fa-comments"} for x in db.query(Consultation).filter(Consultation.created_at >= s8).order_by(desc(Consultation.created_at)).limit(10)] + [{"type": "service_request", "title": "Service Request", "description": f"Service request: {x.service_type}", "timestamp": x.created_at, "icon": "fas fa-tools"} for x in db.query(ServiceRequest).filter(ServiceRequest.created_at >= s8).order_by(desc(ServiceRequest.created_at)).limit(10)]
    return to_response(sorted(acts, key=lambda x: x["timestamp"] or datetime.min, reverse=True))
@app.route("/api/admin/dashboard/revenue", methods=["GET"])
def get_admin_dashboard_revenue():
    db = g.db; require_admin()
    rdata = [{"month": (st := datetime.now().replace(day=1) - timedelta(days=30 * i)).strftime("%b"), "month_full": st.strftime("%B %Y"), "revenue": db.query(Property).filter(Property.created_at >= st, Property.created_at < st + timedelta(days=30)).count() * 1000} for i in range(12)]
    tot, cm = sum((x["revenue"] for x in rdata)), (rdata[-1]["revenue"] if rdata else 0)
    gr = ((cm - rdata[-2]["revenue"]) / rdata[-2]["revenue"] * 100) if len(rdata) >= 2 and rdata[-2]["revenue"] > 0 else 0
    return to_response({"monthly_revenue": list(reversed(rdata)), "total_revenue": tot, "average_monthly": tot / 12 if rdata else 0, "weekly_revenue": cm / 4, "quarterly_revenue": sum((x["revenue"] for x in rdata[-3:])), "yearly_revenue": tot, "growth_rate": round(gr, 2), "breakdown": {"property_sales": {"revenue": round(tot * 0.6, 2), "percentage": 60}, "consultations": {"revenue": round(tot * 0.25, 2), "percentage": 25}, "services": {"revenue": round(tot * 0.1, 2), "percentage": 10}, "other": {"revenue": round(tot * 0.05, 2), "percentage": 5}}, "comparisons": {"weekly": {"current": cm / 4, "previous": rdata[-2]["revenue"] / 4 if len(rdata) >= 2 else 0}, "monthly": {"current": cm, "previous": rdata[-2]["revenue"] if len(rdata) >= 2 else 0}, "quarterly": {"current": sum((x["revenue"] for x in rdata[-3:])), "previous": sum((x["revenue"] for x in rdata[-6:-3])) if len(rdata) >= 6 else 0}, "yearly": {"current": tot, "previous": 0}}})
@app.route("/api/admin/dashboard/property-distribution", methods=["GET"])
def get_admin_dashboard_property_distribution():
    require_admin(); dd = {"RESIDENTIAL": 0, "COMMERCIAL": 0, "OFFICE": 0}
    for pt, cnt in g.db.query(Property.property_type, func.count(Property.id)).group_by(Property.property_type): dd[(pt.value if hasattr(pt, "value") else str(pt)).upper()] = cnt
    return to_response([{"type": {"RESIDENTIAL": "Residential", "COMMERCIAL": "Commercial", "OFFICE": "Office"}.get(k, k), "count": cnt} for k, cnt in dd.items() if k in {"RESIDENTIAL", "COMMERCIAL", "OFFICE"}])
@app.route("/api/admin/dashboard/maintenance-analytics", methods=["GET"])
def get_admin_dashboard_maintenance_analytics():
    require_admin(); m, lbls = {"electrician": 0, "plumber": 0, "maid": 0, "hvac": 0, "carpenter": 0, "painter": 0, "other": 0}, {"electrician": "Electrical", "plumber": "Plumbing", "maid": "Cleaning", "hvac": "HVAC", "carpenter": "Carpentry", "painter": "Painting", "other": "Other"}
    for st, cnt in g.db.query(ServiceRequest.service_type, func.count(ServiceRequest.id)).group_by(ServiceRequest.service_type):
        s = (st or "").lower(); k = "electrician" if "electr" in s else ("plumber" if any(x in s for x in ("plumb", "water", "pipe")) else ("maid" if any(x in s for x in ("maid", "clean", "housekeep")) else ("hvac" if any(x in s for x in ("hvac", "air", "cool", "heat")) else ("carpenter" if "carpent" in s or "wood" in s else ("painter" if "paint" in s else "other")))))
        m[k] += cnt
    return to_response(sorted([{"type": k, "label": lbls[k], "count": v} for k, v in m.items()], key=lambda x: x["count"], reverse=True))
@app.route("/api/admin/dashboard/payment-analytics", methods=["GET"])
def get_admin_dashboard_payment_analytics():
    db = g.db; require_admin()
    comp, act_u = db.query(ServiceRequest).filter(ServiceRequest.status == "completed").count(), db.query(User).filter(User.is_active == True).count()
    on_t, late = comp + act_u * 2, db.query(ServiceRequest).filter(ServiceRequest.status.in_(["assigned", "in_progress"])).count()
    over, part = db.query(ServiceRequest).filter(ServiceRequest.status == "pending", ServiceRequest.created_at < datetime.now() - timedelta(days=7)).count(), max(3, 10); tot = max(1, on_t + late + over + part)
    return to_response([{"status": st, "label": st, "count": cnt, "percentage": round(cnt / tot * 100, 1)} for st, cnt in [("On Time", on_t), ("Late", late), ("Overdue", over), ("Partial", part)]])
@app.route("/api/admin/notifications", methods=["GET"])
def get_admin_notifications():
    db, u, ft, lim, s7 = g.db, require_admin(), request.args.get("filter_type"), request.args.get("limit", 50, type=int), datetime.now() - timedelta(days=7)
    try:
        notifs = [{"id": f"user_{x.id}", "title": "New User Registration", "message": f"{x.first_name} {x.last_name} registered as {x.user_type}.", "category": "system", "type": "info", "is_read": False, "is_critical": False, "timestamp": x.created_at, "icon": "fas fa-user-plus"} for x in db.query(User).filter(User.created_at >= s7).order_by(desc(User.created_at)).limit(10)] + [{"id": f"property_{x.id}", "title": "Property Added", "message": f'Property "{x.title}" was added.', "category": "system", "type": "info", "is_read": False, "is_critical": False, "timestamp": x.created_at, "icon": "fas fa-building"} for x in db.query(Property).filter(Property.created_at >= s7).order_by(desc(Property.created_at)).limit(10)] + [{"id": f"service_request_{x.id}", "title": "Service Request", "message": f"Service request for {x.service_type} ({x.status}).", "category": "maintenance", "type": "warning" if x.urgency in ["high", "emergency"] else "info", "is_read": False, "is_critical": x.urgency in ["high", "emergency"], "timestamp": x.created_at, "icon": "fas fa-tools"} for x in db.query(ServiceRequest).filter(ServiceRequest.created_at >= s7).order_by(desc(ServiceRequest.created_at)).limit(10)] + [{"id": f"consultation_{x.id}", "title": "Consultation Request", "message": f"Consultation request from {x.first_name} {x.last_name}.", "category": "system", "type": "info", "is_read": False, "is_critical": False, "timestamp": x.created_at, "icon": "fas fa-comments"} for x in db.query(Consultation).filter(Consultation.created_at >= s7).order_by(desc(Consultation.created_at)).limit(10)]
        if (oc := db.query(ServiceRequest).filter(ServiceRequest.status == "pending", ServiceRequest.created_at < s7, ServiceRequest.urgency.in_(["high", "emergency"])).count()) > 0: notifs.append({"id": "system_alert_pending_services", "title": "System Alert", "message": f"{oc} high-priority requests pending >7 days.", "category": "system", "type": "critical", "is_read": False, "is_critical": True, "timestamp": datetime.now(), "icon": "fas fa-exclamation-triangle"})
    except Exception as e: notifs = []; print(f"Notif err: {e}")
    notifs.sort(key=lambda x: x["timestamp"] or datetime.min, reverse=True)
    filt = {"unread": lambda n: not n.get("is_read"), "critical": lambda n: n.get("is_critical"), "system": lambda n: n.get("category") == "system", "payment": lambda n: n.get("category") == "payment", "maintenance": lambda n: n.get("category") == "maintenance"}.get(ft)
    return to_response(([n for n in notifs if filt(n)] if filt else notifs)[:lim])
@app.route("/api/admin/leads", methods=["GET"])
def get_all_leads():
    db, u = g.db, require_admin(); leads = db.query(Lead).order_by(desc(Lead.created_at)).all()
    return to_response([{"id": l.id, "first_name": l.first_name, "last_name": l.last_name, "email": l.email, "phone": l.phone, "source": l.source, "status": l.status, "notes": l.notes, "consultant_name": f"{c.first_name} {c.last_name}" if (c := db.query(User).get(l.consultant_id)) else "Unassigned", "created_at": l.created_at, "updated_at": l.updated_at} for l in leads])
@app.route("/api/admin/leads/sources", methods=["GET"])
def get_lead_sources_analytics():
    require_admin(); raw = g.db.query(Lead.source, func.count(Lead.id)).group_by(Lead.source).all(); tot = sum((c for _, c in raw)) or 1
    return to_response({"sources": [{"source": s or "Unknown", "count": c, "percentage": round(c / tot * 100, 1)} for s, c in raw], "total_leads": tot})
@app.route("/api/admin/leads/analytics", methods=["GET"])
def get_lead_analytics():
    db, tot = g.db, require_admin() and g.db.query(Lead).count()
    mleads = [{"month": (st := datetime.now().replace(day=1) - timedelta(days=30 * i)).strftime("%b"), "count": db.query(Lead).filter(Lead.created_at >= st, Lead.created_at < st + timedelta(days=30)).count()} for i in range(6)]
    return to_response({"total_leads": tot, "active_leads": db.query(Lead).filter(Lead.status.in_(["new", "contacted", "qualified"])).count(), "converted_leads": db.query(Lead).filter(Lead.status == "closed_won").count(), "conversion_rate": round(db.query(Lead).filter(Lead.status == "closed_won").count() / tot * 100, 1) if tot else 0, "monthly_leads": list(reversed(mleads))})

@app.route("/api/market-trends", methods=["GET"])
def get_market_trends():
    now = datetime.now(); rng = random.Random((now.year * 100000) + (now.month * 1000) + (now.day * 24) + now.hour)
    hubs = [("🇦🇪", "Dubai, UAE", "Palm Jumeirah, Downtown, Dubai Hills", "$", 1120, (-20, 30), 18.4, (-0.6, 0.8), 8.6, (-0.3, 0.3), 24, (-3, 3), ["Very Bullish", "Aggressive Capital Inflow"], None), ("🇮🇳", "Bangalore, India", "Indiranagar, Whitefield, North Airport Corridor", "$", 295, (-6, 10), 14.2, (-0.5, 0.7), 7.8, (-0.2, 0.3), 18, (-2, 2), ["Bullish", "High Expansion", "Tech Wealth Inflow"], 24500),
            ("🇬🇧", "London, UK", "Mayfair, Kensington, Belgravia", "£", 2450, (-35, 45), 6.8, (-0.4, 0.5), 5.4, (-0.2, 0.2), 42, (-3, 4), ["Stable Safe-Haven", "Institutional Anchor"], None), ("🇺🇸", "Miami, USA", "Brickell, Coconut Grove, Star Island", "$", 1450, (-25, 35), 12.1, (-0.5, 0.6), 6.9, (-0.2, 0.3), 31, (-2, 3), ["Bullish", "Wealth Migration"], None),
            ("🇸🇬", "Singapore", "District 9, Marina Bay, Sentosa Cove", "S$", 3200, (-40, 50), 7.5, (-0.3, 0.4), 4.8, (-0.2, 0.2), 38, (-3, 3), ["Capital Preservation", "Private Banking Hub"], None), ("🇫🇷", "Paris, France", "Golden Triangle, 8th Arrondissement, Le Marais", "€", 1820, (-25, 35), 8.3, (-0.4, 0.5), 5.1, (-0.2, 0.2), 35, (-2, 3), ["Trophy Acquisition", "Resilient Luxury"], None)]
    gh = []
    for flag, city, corr, curr, bsq, sqv, byoy, yv, byld, yval, bdays, dv, sents, inr_b in hubs:
        pd = rng.randint(*sqv); pv, yoy, yld, days = bsq + pd, round(byoy + rng.uniform(*yv), 1), round(byld + rng.uniform(*yval), 1), max(10, bdays + rng.randint(*dv))
        gh.append({"flag": flag, "city": f"{flag} {city}", "corridors": corr, "avg_price_sqft": f"${pv:,} (₹{int(inr_b + pd * 83):,}/sqft)" if inr_b else f"{curr}{pv:,}", "yoy_appreciation": f"{'+' if yoy >= 0 else ''}{yoy}%", "yoy_positive": yoy >= 0, "rental_yield": f"{yld:.1f}%", "liquidity_velocity": f"{'High' if days < 32 else ('Moderate' if days < 45 else 'Stable')} ({days} days)", "sentiment": rng.choice(sents)})
    nxt = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    return to_response({"as_of": f"Live Hourly Benchmark • {now.strftime('%b %Y')}", "hourly_update_interval": 3600, "last_updated": now.strftime("%I:%M %p"), "last_updated_date": now.strftime("%d %b %Y"), "next_update_in_seconds": max(0, int((nxt - now).total_seconds())), "next_update_time": nxt.strftime("%I:%M %p"), "hour_cycle": now.strftime("%Y-%m-%d %H:00"), "global_hubs": gh, "quarterly_reports": [{"title": "2026 Global Ultra-Prime Wealth & Real Estate Report", "tag": "Macro Wealth Index", "read_time": "12 min read", "date": "October 2026", "summary": "Analyzing capital flight patterns and residential tech corridors.", "download_url": "#"}, {"title": "Cross-Border NRI & Foreign Acquisition Dossier", "tag": "FEMA & Tax Compliance", "read_time": "15 min read", "date": "September 2026", "summary": "Remote Embassy POA registration and Form 15CA/CB fast-track.", "download_url": "#"}, {"title": "Golden Visa & Sovereign Residency Benchmark", "tag": "Global Mobility", "read_time": "9 min read", "date": "August 2026", "summary": "Comparative breakdown of real estate acquisition thresholds.", "download_url": "#"}]})

class ChatbotRequest(BaseModel): message: str = ""
@app.route("/api/ai-concierge-chat", methods=["POST"])
def ai_concierge_chat():
    db: Session = g.db
    msg = ((request.get_json(silent=True) or {}).get("message") or "").strip().lower()
    def ans(txt, acts): return to_response({"status": "success", "reply": txt, "quick_actions": acts, "timestamp": datetime.utcnow().isoformat()})
    city_map = {"bengaluru": "Bengaluru", "bangalore": "Bengaluru", "whitefield": "Whitefield", "indiranagar": "Indiranagar", "sadashivanagar": "Sadashivanagar", "mumbai": "Mumbai", "worli": "Worli", "bandra": "Bandra", "delhi": "Delhi", "goa": "Goa", "dubai": "Dubai", "london": "London", "beverly hills": "Beverly Hills", "miami": "Miami Beach", "paris": "Paris"}
    for k, cname in city_map.items():
        if k in msg:
            props = db.query(Property).filter(or_(Property.city.ilike(f"%{cname}%"), Property.address.ilike(f"%{cname}%"))).limit(4).all()
            txt = f"📍 **{cname} Portfolio Spotlight**:\n\n" + ("\n".join([f"• **{p.title}** - {p.price} | {p.bedrooms or 4} BHK | {p.city}" for p in props]) if props else f"No active public listings in {cname}. Contact advisory concierge for private pocket estates.")
            return ans(txt, [{"label": f"🏰 View {cname} Estates", "action": "navigate", "url": f"/property?city={cname}"}, {"label": "💬 WhatsApp Broker", "action": "whatsapp", "text": f"Inquiring about {cname} estates"}])
    rules = [
        ((("maintenance", "service request", "repair", "plumb", "electric"), "🛠️ **Estate Maintenance & Client Services**\nSubmit work orders directly via our Client Services Portal.", [{"label": "🛠️ Submit Service Request", "action": "navigate", "url": "/service"}, {"label": "📋 Service Dashboard", "action": "navigate", "url": "/service-requests"}])), ((("viewing", "tour", "visit", "book appointment"), "📅 **Private Estate Viewings & Helipad Transfers**\nPrivate guided viewings arranged with senior curators.", [{"label": "📅 Book Private Tour", "action": "navigate", "url": "/service#private-viewing"}, {"label": "💬 WhatsApp Concierge", "action": "whatsapp", "text": "Book private viewing"}])),
        ((("guidance value", "circle rate", "kaveri", "stamp duty"), "🏛️ **Karnataka Kaveri 2.0 Guidance Rate Tool**\nCalculate statutory stamp duty and registration cess across 31 Karnataka districts.", [{"label": "🏛️ Guidance Rate Calculator", "action": "navigate", "url": "/investment-dashboard#sr-valuation-tool"}, {"label": "📊 Market Dashboard", "action": "navigate", "url": "/investment-dashboard"}])), ((("pricing", "subscription", "plan", "cost", "fee"), "🏷️ **Advisory Membership & Portfolio Subscriptions**\n• **Sovereign Advisory**: ₹1,250/mo\n• **Presidential Portfolio**: ₹3,150/mo\n• **Royal Dynasty Trust**: Bespoke.", [{"label": "🏷️ Compare Plans", "action": "navigate", "url": "/pricing"}, {"label": "⚡ Instant Subscription", "action": "navigate", "url": "/pricing#payment-section"}])),
        ((("foreign", "nri", "fema", "rbi", "repatriation"), "🌍 **Foreign Investor & NRI Advisory Desk**\n• FEMA Master Direction Compliance\n• NRE/NRO Capital Repatriation (Form 15CA/CB)\n• Remote Embassy POA Registration.", [{"label": "🌍 Foreign Buyer Guide", "action": "navigate", "url": "/foreign-investors"}, {"label": "📋 NRI Verification", "action": "navigate", "url": "/foreign-investors#fema-dossier"}])), ((("contact", "phone", "office", "email", "support", "headquarters"), "📞 **Global Headquarters & Concierge Desks**\n• **Bengaluru Flagship**: +91 (80) 4120-7799\n• **Dubai Desk**: +971 (4) 388-9900\n• **Email**: concierge@primeproperties.com", [{"label": "📞 Call Concierge", "action": "call", "phone": "+918041207799"}, {"label": "💬 WhatsApp Advisory", "action": "whatsapp", "text": "Prime Advisory assistance"}])),
        ((("villa", "penthouse", "mansion", "waterfront", "estate", "property", "buy", "apartment"), "🏰 **Curated Ultra-Prime Inventory**\nBrowse our global collection of trophy penthouses, heritage bungalows, and beachfront estates.", [{"label": "🏰 Explore Properties", "action": "navigate", "url": "/property"}, {"label": "🔍 Search Filters", "action": "navigate", "url": "/properties"}])), ((("hello", "hi", "hey", "greetings", "namaste"), "✨ **Greetings and welcome to Prime Properties Concierge**.\nHow may I assist your portfolio today? Inquire about luxury estates, guidance values, NRI FEMA compliance, or advisory pricing.", [{"label": "🏰 Browse Estates", "action": "navigate", "url": "/property"}, {"label": "🏷️ Advisory Plans", "action": "navigate", "url": "/pricing"}]))
    ]
    for kw_tuple, rep, acts in rules:
        if any(k in msg for k in kw_tuple): return ans(rep, acts)
    return ans("Thank you for contacting Prime Properties Advisory Concierge.\nI can assist with properties, Kaveri 2.0 SR guidance rates, foreign/NRI compliance, pricing plans, and maintenance tickets.", [{"label": "🏰 Explore Properties", "action": "navigate", "url": "/property"}, {"label": "🏛️ SR Calculator", "action": "navigate", "url": "/investment-dashboard#sr-valuation-tool"}, {"label": "🏷️ Pricing Plans", "action": "navigate", "url": "/pricing"}, {"label": "💬 WhatsApp Desk", "action": "whatsapp", "text": f"Hello Prime Concierge: {msg}"}])

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    print("\n" + "=" * 60 + "\n  [+] Pure Flask Platform Running at: http://127.0.0.1:8000\n" + "=" * 60 + "\n")
    run_simple("127.0.0.1", 8000, app, use_reloader=True, use_debugger=True)
