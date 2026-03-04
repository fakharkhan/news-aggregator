# Admin Quick Reference - Sneaker Platform

## Overview

This quick reference guide provides fast access to common admin tasks, troubleshooting steps, and important commands for the Sneaker Platform.

---

## 🔧 Common Commands

### Database Operations
```bash
# Run migrations
php artisan migrate --force

# Seed database
php artisan db:seed --force

# Reset database (development only)
php artisan migrate:fresh --seed

# Create admin user
php artisan make:admin
```

### Cache Management
```bash
# Clear all caches
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Cache for production
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### Queue Management
```bash
# Start queue worker
php artisan queue:work --tries=3 --timeout=300

# Check failed jobs
php artisan queue:failed

# Retry failed jobs
php artisan queue:retry all

# Clear failed jobs
php artisan queue:flush
```

### Maintenance Mode
```bash
# Enable maintenance mode
php artisan down

# Disable maintenance mode
php artisan up

# Maintenance mode with secret token
php artisan down --secret="your-secret-token"
```

---

## 📊 System Monitoring

### Check System Status
```bash
# Check application status
php artisan about

# Check queue status
php artisan queue:monitor

# Check scheduled tasks
php artisan schedule:list

# Check storage links
php artisan storage:link
```

### Log Monitoring
```bash
# View application logs
tail -f storage/logs/laravel.log

# View queue logs
tail -f storage/logs/queue.log

# View error logs
tail -f storage/logs/error.log
```

### Performance Checks
```bash
# Check database connections
php artisan tinker
DB::connection()->getPdo();

# Check cache status
php artisan tinker
Cache::has('test');

# Check file permissions
ls -la storage/
ls -la bootstrap/cache/
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Payment Processing Issues
**Problem**: Stripe payments failing
**Solution**:
```bash
# Check Stripe configuration
php artisan tinker
config('services.stripe');

# Test Stripe connection
php artisan tinker
\Stripe\Stripe::setApiKey(config('services.stripe.secret'));
```

#### 2. Email Delivery Issues
**Problem**: Emails not sending
**Solution**:
```bash
# Test email configuration
php artisan tinker
Mail::raw('Test email', function($message) {
    $message->to('test@example.com')->subject('Test');
});

# Check mail configuration
php artisan config:show mail
```

#### 3. File Upload Issues
**Problem**: Files not uploading
**Solution**:
```bash
# Check storage permissions
chmod -R 775 storage/
chmod -R 775 bootstrap/cache/

# Check disk space
df -h

# Check file upload limits
php -i | grep upload
```

#### 4. Queue Issues
**Problem**: Background jobs not processing
**Solution**:
```bash
# Restart queue workers
php artisan queue:restart

# Check queue status
php artisan queue:work --once

# Clear failed jobs
php artisan queue:flush
```

#### 5. Performance Issues
**Problem**: Slow page loads
**Solution**:
```bash
# Clear all caches
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Optimize autoloader
composer dump-autoload --optimize

# Check database queries
php artisan tinker
\DB::enableQueryLog();
// Run your query
\DB::getQueryLog();
```

---

## 👥 User Management

### Create Users
```bash
# Create admin user
php artisan tinker
use App\Models\User;
use App\Enums\UserRole;
use App\Enums\UserStatus;
use Illuminate\Support\Facades\Hash;

User::create([
    'name' => 'Admin User',
    'email' => 'admin@example.com',
    'password' => Hash::make('password'),
    'role' => UserRole::ADMIN,
    'status' => UserStatus::ACTIVE,
    'email_verified_at' => now(),
]);
```

### Manage User Roles
```bash
# Change user role
php artisan tinker
$user = User::where('email', 'user@example.com')->first();
$user->update(['role' => UserRole::CREATOR]);

# Deactivate user
$user->update(['status' => UserStatus::SUSPENDED]);
```

### Reset Passwords
```bash
# Reset user password
php artisan tinker
$user = User::where('email', 'user@example.com')->first();
$user->update(['password' => Hash::make('new-password')]);
```

---

## 🏭 Manufacturer Management

### Add Manufacturer
```bash
php artisan tinker
use App\Models\Manufacturer;

Manufacturer::create([
    'name' => 'New Factory',
    'region' => 'APAC',
    'contact_email' => 'orders@newfactory.com',
    'phone' => '+86-123-456-7890',
    'min_order_quantity' => 25,
    'active' => true,
    'base_price_tier' => 'mid',
    'metadata' => [
        'specialties' => ['leather', 'canvas'],
        'certifications' => ['ISO9001'],
        'lead_time_days' => 21,
    ],
]);
```

### Update Manufacturer Status
```bash
php artisan tinker
$manufacturer = Manufacturer::find(1);
$manufacturer->update(['active' => false]);
```

---

## 📦 Order Management

### Check Order Status
```bash
php artisan tinker
use App\Models\Order;

// Get all orders
Order::with(['design', 'user'])->get();

// Get orders by status
Order::where('status', 'paid')->get();

// Get orders with issues
Order::whereHas('issues')->get();
```

### Process Refunds
```bash
php artisan tinker
use App\Services\RefundService;

$order = Order::find(1);
$refundService = new RefundService();
$refundService->processRefund($order, 'Customer request');
```

---

## 🔍 Debugging

### Enable Debug Mode
```bash
# Set debug mode in .env
APP_DEBUG=true

# Clear config cache
php artisan config:clear
```

### Check Environment
```bash
# Check environment variables
php artisan tinker
env('APP_ENV');
env('DB_CONNECTION');
env('STRIPE_KEY');
```

### Database Debugging
```bash
# Enable query logging
php artisan tinker
\DB::enableQueryLog();

// Run your operations
// Then check logs
\DB::getQueryLog();
```

---

## 📈 Analytics

### Check Platform Stats
```bash
php artisan tinker

// User counts
User::count();
User::where('role', 'creator')->count();
User::where('role', 'customer')->count();

// Order stats
Order::count();
Order::where('status', 'completed')->count();

// Revenue
Order::where('status', 'completed')->sum('total_cents');
```

### Generate Reports
```bash
# Run analytics rollup
php artisan analytics:rollup

# Check manufacturer KPIs
php artisan tinker
use App\Models\ManufacturerKpisDaily;
ManufacturerKpisDaily::latest()->first();
```

---

## 🔐 Security

### Check Security Settings
```bash
# Verify HTTPS redirects
php artisan tinker
config('app.env');
config('session.secure');

# Check rate limiting
php artisan tinker
config('throttle');
```

### Monitor Failed Logins
```bash
# Check failed login attempts
php artisan tinker
use App\Models\User;
User::where('failed_login_attempts', '>', 0)->get();
```

---

## 📞 Emergency Contacts

### Technical Support
- **Development Team**: dev@sneakerplatform.com
- **System Administrator**: sysadmin@sneakerplatform.com
- **Emergency Hotline**: +1-555-EMERGENCY

### Service Providers
- **Stripe Support**: https://support.stripe.com
- **Email Provider**: support@your-email-provider.com
- **Hosting Provider**: support@your-hosting-provider.com

---

## 📋 Daily Checklist

### Morning Tasks
- [ ] Check system uptime and performance
- [ ] Review error logs for issues
- [ ] Check queue worker status
- [ ] Monitor payment processing
- [ ] Review new user registrations

### Weekly Tasks
- [ ] Review analytics and reports
- [ ] Check manufacturer performance
- [ ] Review customer support tickets
- [ ] Update security patches
- [ ] Backup verification

### Monthly Tasks
- [ ] Performance optimization review
- [ ] Security audit
- [ ] User feedback analysis
- [ ] Platform updates
- [ ] Capacity planning

---

*Last Updated: January 2025*
*Document Location: `/docs/admin-quick-reference.md`*
