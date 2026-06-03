## DB 구조

### users
- _id (ObjectId)
- username (string)
- email (string)
- password (hashed_string)
- created_at (datetime)

### rooms
- _id (ObjectId)
- room_name (string)
- owner_id (string)
- created_at (datetime)

### room_members
- _id (ObjectId)
- room_id (ObjectId)
- user_id (ObjectId)
- joined_at (datetime)

### room_invites
- _id (ObjectId)
- room_id (ObjectId)
- user_id (ObjectId)
- status (string)
- invited_at (datetime)

### posts
- _id (ObjectId)
- room_id (ObjectId)
- title (string)
- content (string)
- author_id (ObjectId)
- author_name (string)
- emotion (string)
- views (int)
- created_at (datetime)
- updated_at (datetime)