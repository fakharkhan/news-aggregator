<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Banned Terms
    |--------------------------------------------------------------------------
    |
    | List of brand names and terms that should not appear in designs.
    | These will be checked against OCR text from artworks and design metadata.
    |
    */
    'banned_terms' => [
        'NIKE',
        'ADIDAS',
        'JORDAN',
        'CONVERSE',
        'GUCCI',
        'PUMA',
        'REEBOK',
        'NEW BALANCE',
        'VANS',
        'UNDER ARMOUR',
        'YEEZY',
        'BALENCIAGA',
        'OFF-WHITE',
        'SUPREME',
        'BAPE',
    ],

    /*
    |--------------------------------------------------------------------------
    | Protected Shapes
    |--------------------------------------------------------------------------
    |
    | List of protected design elements and shapes that indicate
    | potential trademark infringement.
    |
    */
    'protected_shapes' => [
        'swoosh',
        'three stripes',
        'trefoil',
        'jumpman',
        'star chevron',
        'cat logo',
        'vector logo',
        'side stripe',
        'heel tab',
        'air bubble',
        'boost sole',
        'waffle pattern',
    ],

    /*
    |--------------------------------------------------------------------------
    | Logo Hashes
    |--------------------------------------------------------------------------
    |
    | Perceptual hashes of known protected logos for similarity detection.
    | Format: ['label' => 'hash_string']
    |
    */
    'logo_hashes' => [
        'nike_swoosh' => 'a1b2c3d4e5f6g7h8', // Placeholder - replace with actual pHash
        'adidas_stripes' => 'b2c3d4e5f6g7h8i9', // Placeholder - replace with actual pHash
        'jordan_jumpman' => 'c3d4e5f6g7h8i9j0', // Placeholder - replace with actual pHash
        'converse_star' => 'd4e5f6g7h8i9j0k1', // Placeholder - replace with actual pHash
        'puma_cat' => 'e5f6g7h8i9j0k1l2', // Placeholder - replace with actual pHash
    ],

    /*
    |--------------------------------------------------------------------------
    | Perceptual Hash Threshold
    |--------------------------------------------------------------------------
    |
    | Maximum Hamming distance for perceptual hash comparison.
    | Lower values = stricter matching. 12 is a reasonable default.
    |
    */
    'phash_threshold' => 12,

    /*
    |--------------------------------------------------------------------------
    | Score Multipliers (Legacy)
    |--------------------------------------------------------------------------
    |
    | Legacy scoring system for backward compatibility.
    |
    */
    'score_multipliers' => [
        'ocr' => 3,
        'logo' => 5,
        'shape' => 2,
    ],

    /*
    |--------------------------------------------------------------------------
    | Clear Score Threshold (Legacy)
    |--------------------------------------------------------------------------
    |
    | Legacy threshold for backward compatibility.
    |
    */
    'clear_score_threshold' => 5,

    /*
    |--------------------------------------------------------------------------
    | Risk Score Threshold
    |--------------------------------------------------------------------------
    |
    | Maximum allowed IP risk score for a design to pass Gate A.
    | Each violation adds to the score based on severity.
    |
    */
    'risk_threshold' => 5,

    /*
    |--------------------------------------------------------------------------
    | Scoring Weights
    |--------------------------------------------------------------------------
    |
    | Point values for different types of IP violations.
    |
    */
    'scoring' => [
        'banned_term' => 3,
        'logo_match' => 5,
        'protected_shape' => 2,
    ],
];
