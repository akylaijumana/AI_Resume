# Database Schema

## Tables

### resumes
| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment |
| name | TEXT | NOT NULL | Full name |
| email | TEXT | | Email address |
| phone | TEXT | | Phone number |
| education | TEXT | | Education details |
| skills | TEXT | | Skills list |
| experience | TEXT | | Work experience |
| created_at | TEXT | | Timestamp |
| updated_at | TEXT | | Timestamp |

### generated_resumes
| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment |
| title | TEXT | NOT NULL | Resume title |
| content | TEXT | NOT NULL | Full resume text |
| mode | TEXT | | 'template' or 'ai' |
| created_at | TEXT | | Timestamp |

## ER Diagram

```
┌─────────────────────┐
│     resumes         │
├─────────────────────┤
│ • id (PK)           │
│   name *            │
│   email             │
│   phone             │
│   education         │
│   skills            │
│   experience        │
│   created_at        │
│   updated_at        │
└─────────────────────┘

┌─────────────────────┐
│ generated_resumes   │
├─────────────────────┤
│ • id (PK)           │
│   title *           │
│   content *         │
│   mode              │
│   created_at        │
└─────────────────────┘
```

**Legend:** • = Primary Key, * = NOT NULL

**Relationship:** No foreign keys (independent tables)

## SQL

```sql
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    education TEXT,
    skills TEXT,
    experience TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE generated_resumes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    mode TEXT,
    created_at TEXT
);
```

