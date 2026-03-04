# RBAC (Role-Based Access Control) Usage Guide

## Overview

The Custom Sneaker Platform implements a comprehensive RBAC system with three main user roles and detailed authorization policies.

## User Roles

### 1. Customer (`UserRole::CUSTOMER`)
- Can create and manage their own orders
- Can view public designs
- Can report issues on their orders
- Cannot create designs

### 2. Creator (`UserRole::CREATOR`)
- Can create, update, and delete their own designs
- Can view orders for their designs (read-only)
- Can view public designs and their own private designs
- Cannot create orders or manage other users' content

### 3. Admin (`UserRole::ADMIN`)
- Full access to all resources
- Can manage all designs, orders, and issues
- Can resolve issues
- Can restore and permanently delete soft-deleted resources

## Policies

### DesignPolicy
- **Creators**: CRUD access to their own designs
- **Public visibility**: Anyone can view public designs
- **Private visibility**: Only owner or admin can view
- **Admins**: Full access to all designs

### OrderPolicy
- **Customers**: CRUD access to their own orders
- **Creators**: Read-only access to orders for their designs
- **Admins**: Full access to all orders

### IssuePolicy
- **Reporters**: CRUD access to their own issues
- **Admins**: Full access and can resolve issues
- **Future**: Manufacturers will have access via partner portal

## Usage Examples

### In Controllers

```php
// Using policies
public function show(Design $design)
{
    $this->authorize('view', $design);
    return response()->json($design);
}

public function update(Request $request, Order $order)
{
    $this->authorize('update', $order);
    // Update logic...
}
```

### In Routes

```php
// Using role middleware
Route::middleware(['auth', 'role:creator,admin'])->group(function () {
    Route::post('/designs', [DesignController::class, 'store']);
});

Route::middleware(['auth', 'role:customer,admin'])->group(function () {
    Route::post('/orders', [OrderController::class, 'store']);
});

Route::middleware(['auth', 'role:admin'])->group(function () {
    Route::post('/issues/{issue}/resolve', [IssueController::class, 'resolve']);
});
```

### Using Gates

```php
// Check role-based access
if (Gate::allows('admin-access')) {
    // Admin-only functionality
}

if (Gate::allows('creator-access')) {
    // Creator or admin functionality
}

if (Gate::allows('customer-access')) {
    // Customer or admin functionality
}
```

### In Blade Templates (if using)

```blade
@can('view', $design)
    <!-- Show design details -->
@endcan

@can('admin-access')
    <!-- Show admin controls -->
@endcan

@cannot('update', $order)
    <!-- Show read-only view -->
@endcannot
```

### In API Resources

```php
public function toArray($request)
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'description' => $this->description,
        'can_edit' => $request->user()?->can('update', $this),
        'can_delete' => $request->user()?->can('delete', $this),
    ];
}
```

## Quality Gates Integration

The RBAC system integrates with the quality gates system:

- **Gate A (IP Compliance)**: Checked before saving design to ready status
- **Gate B (Manufacturability)**: Checked before allowing order creation
- **Gate C (Production Package)**: Checked before payment capture
- **Gate D (Manufacturer Acceptance)**: Checked before production starts

```php
// Example: Only admins can override quality gates
if (Gate::allows('admin-access')) {
    $order->passGate('A'); // Override IP compliance
}
```

## Error Handling

The system returns appropriate HTTP status codes:

- **401 Unauthorized**: User not authenticated
- **403 Forbidden**: User authenticated but lacks permission
- **404 Not Found**: Resource doesn't exist or user can't view it

## Testing

Use the provided `PolicyTest` class to verify authorization logic:

```bash
php artisan test tests/Feature/PolicyTest.php
```

## Future Enhancements

1. **Manufacturer Portal**: Add manufacturer role and partner access
2. **Team Management**: Allow creators to have team members
3. **Granular Permissions**: More specific permissions beyond basic CRUD
4. **Audit Logging**: Track authorization decisions for compliance
