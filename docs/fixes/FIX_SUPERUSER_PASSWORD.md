# FIX SUPERUSER PASSWORD

## The Problem
The password hash inserted earlier was incorrect. We need to update it with a proper Django-generated hash.

## Solution: Update Password in Database

### Method 1: Cloud Shell (Recommended)

1. **Open Cloud Shell:**
   https://shell.cloud.google.com/?project=bridgetbeta&shellonly=true

2. **Connect to database:**
   ```bash
   gcloud sql connect chatagentb-db --user=chatagentb --database=chatagentb --project=bridgetbeta
   ```

3. **Enter password:**
   ```
   aTRtDg95o4u7MNjCXdQkJv3I
   ```

4. **Update the admin user's password:**
   ```sql
   UPDATE auth_user 
   SET password = 'pbkdf2_sha256$1000000$Eoc7cHvkjyUs78hLFyAglT$nMK9bphDTw3o4wmYGybxb8ZiWh+y+nqgaiSOPejrzT4='
   WHERE username = 'admin';
   ```

5. **Verify the update:**
   ```sql
   SELECT username, email, is_superuser, is_staff, is_active 
   FROM auth_user 
   WHERE username = 'admin';
   ```
   
   You should see:
   ```
   username | email           | is_superuser | is_staff | is_active
   ---------+-----------------+--------------+----------+-----------
   admin    | admin@admin.fr  | t            | t        | t
   ```

6. **Exit:**
   ```sql
   \q
   ```

### Method 2: Delete and Recreate

If the UPDATE doesn't work, delete and recreate:

```sql
-- Delete old user
DELETE FROM auth_user WHERE username = 'admin';

-- Create new user with correct password
INSERT INTO auth_user (
  password, 
  last_login, 
  is_superuser, 
  username, 
  first_name, 
  last_name, 
  email, 
  is_staff, 
  is_active, 
  date_joined
) VALUES (
  'pbkdf2_sha256$1000000$Eoc7cHvkjyUs78hLFyAglT$nMK9bphDTw3o4wmYGybxb8ZiWh+y+nqgaiSOPejrzT4=',
  NULL,
  true,
  'admin',
  '',
  '',
  'admin@admin.fr',
  true,
  true,
  NOW()
);
```

## Test Login

After updating the password:

1. **Go to:** https://chatagentb-backend-548740531838.europe-west1.run.app/admin/
2. **Login with:**
   - Username: `admin`
   - Password: `3RUwJfGr14KWVv0n`

## If Still Failing

Check these common issues:

### 1. CSRF Token Issues
The backend might be rejecting the login due to CSRF. Check browser console for errors.

### 2. Session Issues
Clear your browser cookies for the admin site and try again.

### 3. Database Connection
Verify the user exists:
```sql
SELECT * FROM auth_user WHERE username = 'admin';
```

### 4. Backend Logs
Check for authentication errors:
```powershell
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chatagentb-backend AND textPayload:login" --limit=20 --project=bridgetbeta
```

## Alternative: Create via Django Management Command

If direct database access isn't working, create a one-time Cloud Run Job:

```bash
# This will work because it uses Django's ORM properly
cat > /tmp/create_su.py << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    user = User.objects.get(username='admin')
    user.set_password('3RUwJfGr14KWVv0n')
    user.save()
    print('Password updated!')
except User.DoesNotExist:
    User.objects.create_superuser('admin', 'admin@admin.fr', '3RUwJfGr14KWVv0n')
    print('User created!')
EOF

# Execute via gcloud (this requires alpha features)
# Or upload the script and run it in the container
```

## Success Check

After fixing the password, you should be able to:
1. ✅ Login to admin panel
2. ✅ See Django administration homepage
3. ✅ Access all admin sections (Agents, Conversations, Messages)

## Credentials (Final)

- **URL:** https://chatagentb-backend-548740531838.europe-west1.run.app/admin/
- **Username:** `admin`
- **Email:** `admin@admin.fr`
- **Password:** `3RUwJfGr14KWVv0n`
- **Password Hash (Django):** `pbkdf2_sha256$1000000$Eoc7cHvkjyUs78hLFyAglT$nMK9bphDTw3o4wmYGybxb8ZiWh+y+nqgaiSOPejrzT4=`
