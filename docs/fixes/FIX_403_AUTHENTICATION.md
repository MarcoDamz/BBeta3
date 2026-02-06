# 403 Forbidden Error - Authentication Required

**Date:** January 29, 2026  
**Status:** ✅ Good Progress - Just Need to Login!

---

## The Error

```
POST https://chatagentb-backend-548740531838.europe-west1.run.app/api/agents/ 403 (Forbidden)
```

---

## What This Means

🎉 **GOOD NEWS:** This is actually **progress**!

- ✅ **Frontend → Backend communication works!** (No 404, no CORS errors)
- ✅ **API URL is correct** (request reaches the right endpoint)
- ⚠️ **You're just not authenticated yet**

### Why 403 Forbidden?

The backend has security configured:

```python
# backend/agents/views.py
class AgentViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []  # Anyone can read
        return [IsAdminUser()]  # Only admins can create/update/delete
```

**Creating agents requires admin authentication** → You need to login first!

---

## Solution: 3 Simple Steps

### Step 1️⃣: Fix Superuser Password

**Why:** The superuser exists but has an incorrect password hash.

**How:**

1. **Connect to database:**
   ```bash
   gcloud sql connect chatagentb-db --user=chatagentb --database=chatagentb --project=bridgetbeta
   ```
   
   When prompted for password, enter:
   ```
   aTRtDg95o4u7MNjCXdQkJv3I
   ```

2. **Update password hash:**
   ```sql
   UPDATE auth_user SET password = 'pbkdf2_sha256$1000000$Eoc7cHvkjyUs78hLFyAglT$nMK9bphDTw3o4wmYGybxb8ZiWh+y+nqgaiSOPejrzT4=' WHERE username = 'admin';
   ```

3. **Verify:**
   ```sql
   SELECT username, email, is_superuser FROM auth_user WHERE username = 'admin';
   ```
   
   Should show:
   ```
   username | email          | is_superuser
   ---------+----------------+-------------
   admin    | admin@test.com | t
   ```

4. **Exit:**
   ```
   \q
   ```

### Step 2️⃣: Login via Frontend

1. **Open frontend:**
   ```
   https://chatagentb-frontend-548740531838.europe-west1.run.app
   ```

2. **Enter credentials:**
   - **Username:** `admin`
   - **Password:** `3RUwJfGr14KWVv0n`

3. **Click Login**

4. **Verify success:**
   - Should redirect to chat page
   - Open DevTools (F12) → Application → Cookies
   - Should see `sessionid` cookie ✅

### Step 3️⃣: Create Agents

Now that you're authenticated:

1. **Go to Admin page** (button in frontend or direct):
   ```
   https://chatagentb-frontend-548740531838.europe-west1.run.app/admin
   ```

2. **Click "Créer un agent"**

3. **Fill in details:**
   - Name: `Assistant Python`
   - Description: `Expert en programmation Python`
   - System Prompt: `Tu es un assistant expert en Python...`
   - Provider: `openai`
   - Model: `gpt-4`
   - Temperature: `0.7`

4. **Click "Créer"**

5. **Success!** ✅ No more 403 error!

---

## What Changed During Login

### Before Login (403 Forbidden):
```
Frontend → Backend
Request Headers:
  - Cookie: (none)

Backend Response:
  - 403 Forbidden
  - Reason: No session cookie = not authenticated
```

### After Login (Success):
```
Frontend → Backend
Request Headers:
  - Cookie: sessionid=abc123xyz...

Backend Response:
  - 201 Created (agent created successfully)
  - Agent data returned
```

---

## Technical Details

### Authentication Flow

1. **Login Request:**
   ```
   POST /api/auth/login/
   Body: { username: "admin", password: "..." }
   ```

2. **Backend Validates:**
   ```python
   user = authenticate(request, username=username, password=password)
   if user is not None:
       login(request, user)  # Creates session
   ```

3. **Session Cookie Set:**
   ```
   Set-Cookie: sessionid=...; HttpOnly; SameSite=Lax
   ```

4. **Future Requests Include Cookie:**
   ```
   Cookie: sessionid=...
   ```

5. **Backend Validates Session:**
   ```python
   IsAdminUser() → checks if user.is_staff and user.is_superuser
   ```

### Why Sessions Instead of JWT?

The project uses **Django session authentication**:

- ✅ More secure (HttpOnly cookies can't be stolen by JavaScript)
- ✅ Server-side session storage (can revoke instantly)
- ✅ Works with Django admin panel
- ✅ Simpler for single-domain applications

### CORS with Credentials

Frontend is configured correctly:

```javascript
// frontend/src/services/api.js
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,  // ✅ Required to send cookies
  headers: { "Content-Type": "application/json" },
});
```

Backend CORS allows credentials:

```python
# backend/chatagentb/settings.py
CORS_ALLOW_CREDENTIALS = True
```

---

## Verification Checklist

After completing all steps:

- [ ] **Database password updated** (Step 1)
- [ ] **Login successful** (Step 2)
- [ ] **Session cookie present** (DevTools → Application → Cookies)
- [ ] **User info displayed** (frontend shows admin username)
- [ ] **Can access Admin page**
- [ ] **Can create agents** (no 403 error)
- [ ] **Agent appears in list**

---

## Common Issues

### Issue: "Identifiants invalides" on Login

**Cause:** Password not updated or incorrect password used

**Solution:**
- Verify Step 1 was completed
- Check password is exactly: `3RUwJfGr14KWVv0n`
- No extra spaces before/after

### Issue: Login succeeds but still 403 on agent creation

**Cause:** User is not admin/superuser

**Solution:**
```sql
-- Verify user is superuser
SELECT username, is_staff, is_superuser FROM auth_user WHERE username = 'admin';

-- If not, fix it:
UPDATE auth_user SET is_staff = true, is_superuser = true WHERE username = 'admin';
```

### Issue: Session cookie not saving

**Cause:** CORS or browser security

**Solution:**
- Check DevTools Console for CORS errors
- Verify `withCredentials: true` in api.js
- Try clearing browser cache and cookies
- Try incognito mode

---

## Alternative: Create Agents via Django Admin

If frontend still has issues, you can create agents via Django admin:

1. **Login to Django admin:**
   ```
   https://chatagentb-backend-548740531838.europe-west1.run.app/admin/
   ```
   
   - Username: `admin`
   - Password: `3RUwJfGr14KWVv0n`

2. **Navigate to:** Agents → Add Agent

3. **Fill form and save**

4. **Return to frontend** → agents should appear in list

---

## Progress Summary

### ✅ Completed

- Infrastructure deployed (18 attempts journey!)
- Static files serving (WhiteNoise)
- CORS configured correctly
- API URL fixed (added `/api` suffix)
- Frontend-backend communication working

### ⚠️ Current Step

- **Fix superuser password** (5 minutes)
- **Login to application** (1 minute)
- **Create agents** (works after login)

### 📊 Progress: 95% Complete!

Just one more step! 🎉

---

## Next Steps After Login

Once you're logged in and can create agents:

1. **Create demo agents** (optional):
   - Python Expert
   - JavaScript Guru
   - DevOps Specialist

2. **Test chat functionality:**
   - Create conversation
   - Send messages
   - Verify LLM integration

3. **Test Auto-Chat** (optional):
   - Select 2 agents
   - Start auto-chat
   - Watch them converse

4. **Configure environment:**
   - Add OpenAI API key (if not already set)
   - Add Anthropic API key (optional)
   - Test different LLM providers

---

## Quick Command Reference

```bash
# Fix superuser password
gcloud sql connect chatagentb-db --user=chatagentb --database=chatagentb --project=bridgetbeta
# Password: aTRtDg95o4u7MNjCXdQkJv3I

UPDATE auth_user SET password = 'pbkdf2_sha256$1000000$Eoc7cHvkjyUs78hLFyAglT$nMK9bphDTw3o4wmYGybxb8ZiWh+y+nqgaiSOPejrzT4=' WHERE username = 'admin';

\q

# Login credentials
Username: admin
Password: 3RUwJfGr14KWVv0n

# URLs
Frontend: https://chatagentb-frontend-548740531838.europe-west1.run.app
Backend:  https://chatagentb-backend-548740531838.europe-west1.run.app
Admin:    https://chatagentb-backend-548740531838.europe-west1.run.app/admin/
```

---

## Documentation References

- **FIX_SUPERUSER_PASSWORD.md** - Detailed password fix guide
- **API.md** - API endpoints documentation
- **DEPLOYMENT_SUCCESS.md** - Full deployment history
- **STATIC_FILES_FIX.md** - Static files issue resolution
- **CORS_FIX.md** - CORS configuration fix
- **API_URL_FIX.md** - API URL path fix

---

## Summary

**Error:** 403 Forbidden when creating agents  
**Cause:** Not authenticated (no login yet)  
**Solution:** Fix superuser password → Login → Create agents  
**Status:** ✅ Almost there! Just need to login  
**Time:** 5-10 minutes to complete  

**You're 95% done!** 🎉 Just fix the password, login, and you're ready to use your chatbot! 🚀
