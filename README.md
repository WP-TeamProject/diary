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


## 주요 기능 (CRUD)

### 사용자 관리
- Create: 회원 가입
- Read: 로그인 시 사용자 정보 조회, 프로필 조회
- Update: 아이디 변경, 비밀번호 변경
- Delete: 회원 탈퇴

### 방 관리
- Create: 새로운 방 생성
- Read: 참여 중인 방 목록 조회, 방 상세 정보 조회
- Update: 방 이름 수정
- Delete: 방 삭제

### 초대 관리
- Create: 사용자 초대, 초대 정보 생성
- Read: 받은 초대 목록 조회
- Update: 초대 수락, 초대 거절
- Delete: 처리 완료된 초대 삭제

### 게시글 관리
- Create: 게시글 작성 및 저장
- Read: 게시글 목록 조회, 게시글 상세 조회, 과거 게시글 검색, 조회수 확인
- Update: 게시글 수정
- Delete: 게시글 삭제

### 댓글 관리
- Create: 댓글 작성
- Read: 게시글 댓글 조회
- Update: 댓글 수정
- Delete: 댓글 삭제