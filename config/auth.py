roles = [
    dict(
        key = 'admin',
        permissions = [
            '*'
        ]
    ),
    dict(
        key = 'coordinator',
        permissions = [
            'events.*'
        ]
    ),
    dict(
        key = 'member',
        permissions = [
            'events.view',
            'events.enroll'
        ]
    ),
]
