# Admin Setup Guide - Sneaker Platform

## Overview

This guide provides step-by-step instructions for administrators to set up the Sneaker Platform for production use. It covers all essential configurations needed before creators and customers can start using the platform.

## Prerequisites

- Server with PHP 8.2+ and Node.js 18+
- Database (MySQL 8.0+ or PostgreSQL 13+)
- SSL certificate for production
- Domain name configured

## 1. Initial Environment Setup

### 1.1 Environment Variables

Create a `.env` file with the following configuration:

```env
# Application
APP_NAME="Sneaker Platform"
APP_ENV=production
APP_DEBUG=false
APP_URL=https://your-domain.com
APP_KEY=base64:your-generated-key

# Database
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=sneaker_platform
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password

# Mail Configuration
MAIL_MAILER=smtp
MAIL_HOST=your-smtp-host
MAIL_PORT=587
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@your-domain.com
MAIL_FROM_NAME="${APP_NAME}"

# Stripe Configuration
STRIPE_KEY=pk_live_your_publishable_key
STRIPE_SECRET=sk_live_your_secret_key

# Frontend Stripe Key (for Vite)
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_your_publishable_key

# Pricing Configuration
PLATFORM_FEE_PCT=0.12
DEFAULT_TAX_PCT=0.00
DEFAULT_CURRENCY=USD
SHIPPING_ZONES_JSON={"US": 1500, "EU": 1800, "APAC": 2000, "OTHER": 2500}

# Unsplash Integration (for placeholder images)
UNSPLASH_ACCESS_KEY=your_unsplash_access_key
UNSPLASH_SECRET_KEY=your_unsplash_secret_key

# Queue Configuration
QUEUE_CONNECTION=redis
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

# File Storage
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=your-s3-bucket
AWS_USE_PATH_STYLE_ENDPOINT=false

# Session & Cache
SESSION_DRIVER=redis
CACHE_DRIVER=redis

# Logging
LOG_CHANNEL=stack
LOG_DEPRECATIONS_CHANNEL=null
LOG_LEVEL=warning

# Security
SESSION_SECURE_COOKIE=true
SESSION_SAME_SITE=lax
```

### 1.2 Database Setup

```bash
# Run migrations
php artisan migrate --force

# Seed initial data
php artisan db:seed --force

# Create admin user
php artisan make:admin
```

## 2. Admin User Creation

### 2.1 Create Admin Account

Run the following command to create your admin account:

```bash
php artisan make:admin
```

Or manually create via database seeder:

```bash
php artisan tinker
```

```php
use App\Models\User;
use App\Enums\UserRole;
use App\Enums\UserStatus;
use Illuminate\Support\Facades\Hash;

User::create([
    'name' => 'Admin User',
    'email' => 'admin@your-domain.com',
    'password' => Hash::make('secure-password'),
    'role' => UserRole::ADMIN,
    'status' => UserStatus::ACTIVE,
    'email_verified_at' => now(),
]);
```

### 2.2 Admin Login

1. Navigate to `/login`
2. Use your admin credentials
3. Access admin dashboard at `/admin`

### 2.3 User Registration Flow

The platform now includes role selection during registration:

- **Customer Registration**: Users can select "Shop & Order" to browse and purchase designs
- **Creator Registration**: Users can select "Design & Create" to upload designs and earn commissions
- **Role Validation**: Backend validates role selection and assigns appropriate permissions
- **Role-Based Redirects**: Users are redirected to appropriate dashboards based on their role

## 3. Manufacturer Setup

### 3.1 Add Manufacturers

Navigate to **Admin > Manufacturers** and add your manufacturing partners:

**Required Information:**
- Company name
- Region (APAC, EU, NA, LATAM)
- Contact email
- Phone number
- Minimum order quantity
- Base price tier (low, mid, high)
- Specialties (leather, mesh, canvas, etc.)
- Certifications
- Lead time (days)

**Example Manufacturer Entry:**
```json
{
  "name": "Alpha Factory",
  "region": "APAC",
  "contact_email": "orders@alphafactory.com",
  "phone": "+86-755-1234-5678",
  "min_order_quantity": 25,
  "base_price_tier": "mid",
  "metadata": {
    "specialties": ["leather", "synthetic", "canvas"],
    "certifications": ["ISO9001", "OEKO-TEX"],
    "lead_time_days": 21,
    "quality_rating": 4.8,
    "established_year": 2010
  }
}
```

### 3.2 Configure Manufacturer Skills

For each manufacturer, set up their capabilities:

1. Go to **Admin > Manufacturers > [Manufacturer] > Skills**
2. Add supported silhouettes
3. Configure capacity settings
4. Set matching weights

### 3.3 Partner Portal Access

Manufacturers will receive signed URLs for:
- Order acceptance/rejection
- Milestone updates
- Issue management

## 4. Catalog Configuration

### 4.1 Silhouettes Setup

Navigate to **Admin > Silhouettes** and add sneaker silhouettes:

**Required Information:**
- Manufacturer association
- Silhouette code (unique)
- Name and description
- Panel specifications (JSON)
- Image URLs
- Active status

**Example Silhouette:**
```json
{
  "manufacturer_id": 1,
  "code": "AIR_MAX_90",
  "name": "Air Max 90",
  "description": "Classic Air Max 90 silhouette",
  "specs": {
    "panels": ["toe", "midfoot", "heel", "tongue", "eyelets"]
  },
  "images": [
    "https://example.com/air-max-90-front.jpg",
    "https://example.com/air-max-90-side.jpg"
  ],
  "active": true
}
```

### 4.2 Materials Library

Navigate to **Admin > Materials** and configure materials:

**Required Information:**
- Manufacturer association
- Material code (unique per manufacturer)
- Name and description
- Color (hex code)
- Category (leather, mesh, canvas, etc.)
- Printable status
- Constraints (JSON)
- Active status

**Example Material:**
```json
{
  "manufacturer_id": 1,
  "code": "LEATHER_001",
  "name": "Premium Leather Black",
  "description": "High-quality black leather",
  "color": "#000000",
  "category": "leather",
  "printable": true,
  "constraints": {
    "max_colors": 6,
    "min_dpi": 300,
    "bleed_required": true
  },
  "active": true
}
```

## 5. Quality Gates Configuration

### 5.1 IP Guardrails (Gate A)

Configure intellectual property scanning:

1. **OCR Settings**: Enable/disable text detection
2. **Similarity Threshold**: Set minimum similarity score (0.0-1.0)
3. **Shape Detection**: Configure shape matching sensitivity
4. **Blocked Keywords**: Add trademarked terms

### 5.2 Manufacturability Checks (Gate B)

Set manufacturing constraints:

1. **DPI Requirements**: Minimum 300 DPI
2. **Bleed Requirements**: 0.125" minimum
3. **Color Limits**: Maximum 6 colors per design
4. **Panel Coverage**: Minimum 10% coverage per panel

### 5.3 Production Package Validation (Gate C)

Configure final validation:

1. **Package Quality**: DPI, bleed, coverage checks
2. **Color Count**: Validate against material constraints
3. **File Format**: Ensure proper file types

## 6. Pricing Configuration

### 6.1 Platform Fees

Set in `.env`:
```env
PLATFORM_FEE_PCT=0.12  # 12% platform fee
```

### 6.2 Shipping Zones

Configure in `.env`:
```env
SHIPPING_ZONES_JSON={"US": 1500, "EU": 1800, "APAC": 2000, "OTHER": 2500}
```

### 6.3 Tax Configuration

Set tax rates in `config/tax.php`:
```php
'rates' => [
    'US' => 0.00,  // No VAT for US
    'EU' => 0.20,  // 20% VAT for EU
    'APAC' => 0.10, // 10% VAT for APAC
],
```

## 7. Email Configuration

### 7.1 Email Templates

Verify email templates are configured:
- Order confirmation emails
- Manufacturer assignment notifications
- Milestone updates
- Issue notifications
- Delivery confirmations

### 7.2 Email Settings

Test email delivery:
```bash
php artisan tinker
Mail::raw('Test email', function($message) {
    $message->to('test@example.com')->subject('Test');
});
```

## 8. Queue Configuration

### 8.1 Queue Workers

Set up queue workers for background jobs:

```bash
# Start queue worker
php artisan queue:work --tries=3 --timeout=300

# For production, use supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start sneaker-platform-worker:*
```

### 8.2 Scheduled Tasks

Configure cron for scheduled tasks:

```bash
# Add to crontab
* * * * * cd /path/to/your/app && php artisan schedule:run >> /dev/null 2>&1
```

## 9. Security Configuration

### 9.1 SSL Certificate

Ensure SSL is properly configured for production.

### 9.2 Rate Limiting

Configure rate limits in `app/Http/Kernel.php`:
- API endpoints: 60 requests/minute
- Login attempts: 5 attempts/minute
- File uploads: 10 files/minute

### 9.3 File Upload Security

Configure file upload restrictions:
- Maximum file size: 10MB
- Allowed formats: PNG, JPG, SVG
- Virus scanning (recommended)

## 10. Monitoring Setup

### 10.1 Error Tracking

Configure error tracking service (Sentry, Bugsnag, etc.)

### 10.2 Performance Monitoring

Set up application performance monitoring (APM)

### 10.3 Log Management

Configure log aggregation and monitoring

## 11. Testing Checklist

Before going live, verify:

### 11.1 Core Functionality
- [ ] User registration and login
- [ ] Design creation and editing
- [ ] Order placement and payment
- [ ] Manufacturer assignment
- [ ] Milestone tracking
- [ ] Issue reporting

### 11.2 Admin Functions
- [ ] Order management
- [ ] Manufacturer management
- [ ] Catalog management
- [ ] Issue resolution
- [ ] Analytics dashboard

### 11.3 Partner Portal
- [ ] Manufacturer login via signed URLs
- [ ] Order acceptance/rejection
- [ ] Milestone updates
- [ ] Issue management

### 11.4 Payment Processing
- [ ] Stripe integration
- [ ] Payment capture
- [ ] Refund processing
- [ ] Tax calculation

## 12. Go-Live Checklist

### 12.1 Final Preparations
- [ ] All environment variables configured
- [ ] Database seeded with initial data
- [ ] Admin user created
- [ ] Manufacturers added and configured
- [ ] Catalog populated with silhouettes and materials
- [ ] Quality gates configured
- [ ] Email templates tested
- [ ] Queue workers running
- [ ] SSL certificate installed
- [ ] Monitoring configured

### 12.2 User Onboarding
- [ ] Create sample creator accounts
- [ ] Create sample customer accounts
- [ ] Prepare welcome emails
- [ ] Set up help documentation
- [ ] Configure support channels

### 12.3 Launch Sequence
1. Enable user registration
2. Send invitations to beta creators
3. Monitor system performance
4. Gradually increase user access
5. Monitor feedback and issues

## 13. Post-Launch Monitoring

### 13.1 Key Metrics to Track
- User registration rate
- Design creation rate
- Order conversion rate
- Payment success rate
- Issue resolution time
- System performance

### 13.2 Regular Maintenance
- Daily: Check queue workers and logs
- Weekly: Review analytics and performance
- Monthly: Update catalog and pricing
- Quarterly: Security audit and updates

## Support

For technical support during setup:
- Check application logs: `storage/logs/laravel.log`
- Review queue failures: `php artisan queue:failed`
- Monitor system resources
- Contact development team for issues

---

*Last Updated: January 2025*
*Document Location: `/docs/admin-setup-guide.md`*
