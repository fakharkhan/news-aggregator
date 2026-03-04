<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Admin Configuration
    |--------------------------------------------------------------------------
    |
    | Configuration settings for admin functionality including SLA thresholds
    | for order management and exception flagging.
    |
    */

    'sla_days' => [
        'in_production' => 7,
        'qa' => 3,
        'shipped' => 14,
    ],

    'flags' => [
        'awaiting_assignment' => [
            'label' => 'Awaiting Assignment',
            'description' => 'Order is paid but has no manufacturer assignment or assignment is pending/rejected',
            'color' => 'warning',
        ],
        'gate_failed' => [
            'label' => 'Gate Failed',
            'description' => 'Design failed IP or manufacturing gate validation',
            'color' => 'destructive',
        ],
        'overdue_milestone' => [
            'label' => 'Overdue Milestone',
            'description' => 'Next expected milestone is past due based on SLA',
            'color' => 'destructive',
        ],
        'refund_pending' => [
            'label' => 'Refund Pending',
            'description' => 'Order has pending refunds or refund requests',
            'color' => 'warning',
        ],
        'issue_open' => [
            'label' => 'Issue Open',
            'description' => 'Order has open or under review issues',
            'color' => 'destructive',
        ],
    ],
];
