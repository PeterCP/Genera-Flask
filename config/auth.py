"""
Permission keys should follow these guidelines:
- Resources should be pluralized. (e.g. users, events, etc.)
- Verbs regarding resources should be as follows:
    - view:   View either a single resource or an index of resources.
    - create: Create a new resource.
    - update: Update an existing resource.
    - delete: Delete a resource.
- Any other verb should be in infinitive form (e.g. enroll, subscribe, etc.).
"""

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
