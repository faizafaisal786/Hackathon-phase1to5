# Authentication

## Overview
JWT-based authentication system for secure user access.

## Implementation
- ✅ JWT (JSON Web Tokens) for stateless authentication
- ✅ Bcrypt password hashing
- ✅ Token-based session management
- ✅ Protected API routes

## Technology Stack
- **python-jose[cryptography]**: JWT encoding/decoding
- **passlib[bcrypt]**: Password hashing
- **FastAPI Security**: HTTPBearer scheme
- **Python 3.10+**: Modern Python features

## Authentication Flow

### 1. User Registration
```
Client -> POST /auth/register
{
  "email": "user@example.com",
  "username": "username",
  "password": "plaintext_password",
  "full_name": "John Doe"
}

Server:
1. Validates input data
2. Checks if email/username already exists
3. Hashes password with bcrypt
4. Stores user in database
5. Returns user data (without password)

Response: 201 Created
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### 2. User Login
```
Client -> POST /auth/token
{
  "username": "username",
  "password": "plaintext_password"
}

Server:
1. Finds user by username or email
2. Verifies password with bcrypt
3. Checks if user is active
4. Creates JWT token with user ID
5. Returns token

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Accessing Protected Routes
```
Client -> GET /tasks
Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Server:
1. Extracts token from Authorization header
2. Decodes and verifies JWT signature
3. Extracts user ID from token payload
4. Fetches user from database
5. Checks if user is active
6. Proceeds with request if valid

Response: 200 OK with requested data
```

## JWT Token Structure

### Payload
```json
{
  "sub": 1,                    // User ID
  "exp": 1704153600           // Expiration timestamp
}
```

### Configuration
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret Key**: Configured in .env file
- **Expiration**: 30 minutes (configurable)
- **Token Type**: Bearer

## Security Features

### Password Security
- ✅ Passwords hashed with bcrypt (cost factor: 12)
- ✅ Plain passwords never stored
- ✅ Passwords not returned in API responses
- ✅ Minimum password length enforced

### Token Security
- ✅ Short expiration time (30 minutes)
- ✅ Signed tokens prevent tampering
- ✅ Secret key stored in environment variables
- ✅ HTTPS recommended for production

### Authorization
- ✅ User ownership verification on all operations
- ✅ Active user check on each request
- ✅ 403 Forbidden for unauthorized access
- ✅ 401 Unauthorized for invalid tokens

## API Endpoints

### Public Endpoints (No auth required)
- `POST /auth/register` - Create new account
- `POST /auth/login` - Login (form data)
- `POST /auth/token` - Login (JSON)

### Protected Endpoints (JWT required)
- All `/tasks/*` endpoints

## Frontend Integration

### Token Storage
```typescript
// Store token after login
localStorage.setItem('token', access_token);

// Include in API requests
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
```

### Auth Context
```typescript
const AuthContext = createContext({
  token: string | null,
  login: (username, password) => Promise<void>,
  register: (...) => Promise<void>,
  logout: () => void,
  isAuthenticated: boolean
});
```

### Protected Routes
```typescript
// Redirect to login if not authenticated
if (!isAuthenticated) {
  router.push('/login');
}
```

### Token Refresh
Current implementation: Simple expiration (30 min)
Future: Implement refresh tokens for extended sessions

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Inactive user"
}
```

## Dependencies Code

### Backend (app/auth.py)
```python
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"])

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

### Frontend (lib/api.ts)
```typescript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## Environment Variables

### Required
```env
SECRET_KEY=your-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Security Best Practices
1. Generate strong random secret key
2. Never commit .env to version control
3. Use different keys for dev/staging/prod
4. Rotate keys periodically
5. Use HTTPS in production

## Future Enhancements
- Refresh token implementation
- Email verification
- Password reset functionality
- Two-factor authentication (2FA)
- OAuth integration (Google, GitHub)
- Session management and revocation
- Rate limiting on auth endpoints
