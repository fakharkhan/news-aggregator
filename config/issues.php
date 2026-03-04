<?php

return [
    'sla_days' => [
        'open' => 2,              // first response SLA
        'under_review' => 5,      // investigation SLA
        'awaiting_manufacturer' => 7,
    ],
    'max_photos' => 6,
    'max_photo_size' => 10 * 1024 * 1024, // 10MB
    'allowed_photo_types' => ['image/jpeg', 'image/png', 'image/webp'],
    'rate_limits' => [
        'create' => ['throttle:5,10'], // 5 issues per 10 minutes
        'comment' => ['throttle:10,5'], // 10 comments per 5 minutes
    ],
];
