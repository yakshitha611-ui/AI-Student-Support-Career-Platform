import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_student_profile_columns() -> None:
    """Apply a safe SQLite migration for the final Phase 2 student profile schema.

    This is intentionally idempotent and preserves all existing rows and user records.
    It adds only the columns required by the current StudentProfile model, without
    resetting or recreating the database.
    """
    with engine.begin() as conn:
        result = conn.execute(text("PRAGMA table_info(student_profiles)"))
        existing_columns = {row[1] for row in result.fetchall()}

        required_columns = {
            "full_name": "TEXT",
            "email": "TEXT",
            "phone_number": "TEXT",
            "university": "TEXT",
            "branch": "TEXT",
            "year_of_study": "TEXT",
            "current_semester": "TEXT",
            "cgpa_percentage": "TEXT",
        }

        for column_name, column_type in required_columns.items():
            if column_name not in existing_columns:
                conn.execute(
                    text(f"ALTER TABLE student_profiles ADD COLUMN {column_name} {column_type}")
                )


def ensure_student_skills_user_id() -> None:
    """Safely migrate legacy student_skills rows to the current user-based schema.

    Older SQLite databases may contain student_skills with a legacy NOT NULL "name" column
    while the app expects a nullable "skill_name" field tied to the current user/profile model.
    This migration preserves all existing rows, repairs the legacy schema, and ensures each
    skill row is associated with a valid user_id and profile_id.
    """
    with engine.begin() as conn:
        columns = conn.execute(text("PRAGMA table_info(student_skills)")).fetchall()
        if not columns:
            return

        existing_columns = {row[1] for row in columns}
        has_legacy_name_column = "name" in existing_columns
        has_skill_name_column = "skill_name" in existing_columns
        legacy_name_not_null = any(row[1] == "name" and row[3] == 1 for row in columns)

        for column_name, column_type in {
            "user_id": "INTEGER",
            "profile_id": "INTEGER",
            "skill_name": "VARCHAR",
            "proficiency": "VARCHAR",
        }.items():
            if column_name not in existing_columns:
                conn.execute(text(f"ALTER TABLE student_skills ADD COLUMN {column_name} {column_type}"))

        refreshed_columns = {row[1] for row in conn.execute(text("PRAGMA table_info(student_skills)")).fetchall()}

        if has_legacy_name_column and has_skill_name_column and legacy_name_not_null:
            legacy_rows = conn.execute(
                text(
                    "SELECT id, user_id, profile_id, skill_name, name, proficiency, level, created_at FROM student_skills"
                )
            ).fetchall()

            conn.execute(text("ALTER TABLE student_skills RENAME TO student_skills_legacy"))
            conn.execute(
                text(
                    """
                    CREATE TABLE student_skills (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        profile_id INTEGER NOT NULL,
                        skill_name VARCHAR NOT NULL,
                        proficiency VARCHAR,
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
            )

            for row in legacy_rows:
                row_id, user_id, profile_id, skill_name, legacy_name, proficiency, level, created_at = row
                resolved_user_id = user_id
                resolved_profile_id = profile_id

                if resolved_user_id is None and resolved_profile_id is not None:
                    resolved_user_id = conn.execute(
                        text("SELECT user_id FROM student_profiles WHERE id = :profile_id"),
                        {"profile_id": resolved_profile_id},
                    ).scalar()

                if resolved_profile_id is None and resolved_user_id is not None:
                    resolved_profile_id = conn.execute(
                        text("SELECT id FROM student_profiles WHERE user_id = :user_id"),
                        {"user_id": resolved_user_id},
                    ).scalar()

                if resolved_user_id is None and resolved_profile_id is None:
                    continue

                if resolved_user_id is None and resolved_profile_id is not None:
                    resolved_user_id = conn.execute(
                        text("SELECT user_id FROM student_profiles WHERE id = :profile_id"),
                        {"profile_id": resolved_profile_id},
                    ).scalar()

                if resolved_profile_id is None and resolved_user_id is not None:
                    resolved_profile_id = conn.execute(
                        text("SELECT id FROM student_profiles WHERE user_id = :user_id"),
                        {"user_id": resolved_user_id},
                    ).scalar()

                if resolved_user_id is None or resolved_profile_id is None:
                    continue

                final_skill_name = skill_name or legacy_name or "Untitled skill"
                final_proficiency = proficiency or level or "Intermediate"
                final_created_at = created_at or "CURRENT_TIMESTAMP"

                conn.execute(
                    text(
                        """
                        INSERT INTO student_skills (id, user_id, profile_id, skill_name, proficiency, created_at)
                        VALUES (:id, :user_id, :profile_id, :skill_name, :proficiency, :created_at)
                        """
                    ),
                    {
                        "id": row_id,
                        "user_id": resolved_user_id,
                        "profile_id": resolved_profile_id,
                        "skill_name": final_skill_name,
                        "proficiency": final_proficiency,
                        "created_at": final_created_at,
                    },
                )

            conn.execute(text("DROP TABLE student_skills_legacy"))
            refreshed_columns = {row[1] for row in conn.execute(text("PRAGMA table_info(student_skills)")).fetchall()}

        elif "profile_id" in refreshed_columns and "user_id" in refreshed_columns:
            conn.execute(
                text(
                    """
                    UPDATE student_skills
                    SET user_id = (
                        SELECT sp.user_id
                        FROM student_profiles sp
                        WHERE sp.id = student_skills.profile_id
                    )
                    WHERE user_id IS NULL AND profile_id IS NOT NULL
                    """
                )
            )

            conn.execute(
                text(
                    """
                    UPDATE student_skills
                    SET profile_id = (
                        SELECT sp.id
                        FROM student_profiles sp
                        WHERE sp.user_id = student_skills.user_id
                    )
                    WHERE profile_id IS NULL AND user_id IS NOT NULL
                    """
                )
            )

        if "name" in refreshed_columns and "skill_name" in refreshed_columns:
            conn.execute(
                text(
                    "UPDATE student_skills SET skill_name = name WHERE skill_name IS NULL AND name IS NOT NULL"
                )
            )

        if "level" in refreshed_columns and "proficiency" in refreshed_columns:
            conn.execute(
                text(
                    "UPDATE student_skills SET proficiency = level WHERE proficiency IS NULL AND level IS NOT NULL"
                )
            )

        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_student_skills_user_id ON student_skills (user_id)"))


def ensure_student_projects_user_id() -> None:
    """Safely migrate legacy student_projects rows to the current user-based schema.

    Older SQLite databases may store project records using profile_id and title columns.
    This migration adds the required current columns only if they are missing and backfills
    user_id from the related student profile when that mapping is available.
    """
    with engine.begin() as conn:
        result = conn.execute(text("PRAGMA table_info(student_projects)"))
        existing_columns = {row[1] for row in result.fetchall()}

        for column_name, column_type in {
            "user_id": "INTEGER",
            "project_name": "VARCHAR",
            "description": "TEXT",
            "technologies_used": "TEXT",
            "skills_used": "TEXT",
            "student_role": "VARCHAR",
            "project_duration": "VARCHAR",
            "project_link": "VARCHAR",
        }.items():
            if column_name not in existing_columns:
                conn.execute(text(f"ALTER TABLE student_projects ADD COLUMN {column_name} {column_type}"))

        refreshed_columns = {row[1] for row in conn.execute(text("PRAGMA table_info(student_projects)")).fetchall()}

        if "profile_id" in refreshed_columns and "user_id" in refreshed_columns:
            conn.execute(
                text(
                    """
                    UPDATE student_projects
                    SET user_id = (
                        SELECT sp.user_id
                        FROM student_profiles sp
                        WHERE sp.id = student_projects.profile_id
                    )
                    WHERE user_id IS NULL AND profile_id IS NOT NULL
                    """
                )
            )

        if "title" in refreshed_columns and "project_name" in refreshed_columns:
            conn.execute(
                text(
                    "UPDATE student_projects SET project_name = title WHERE project_name IS NULL AND title IS NOT NULL"
                )
            )

        if "technologies" in refreshed_columns and "technologies_used" in refreshed_columns:
            conn.execute(
                text(
                    "UPDATE student_projects SET technologies_used = technologies WHERE technologies_used IS NULL AND technologies IS NOT NULL"
                )
            )

        if "project_url" in refreshed_columns and "project_link" in refreshed_columns:
            conn.execute(
                text(
                    "UPDATE student_projects SET project_link = project_url WHERE project_link IS NULL AND project_url IS NOT NULL"
                )
            )

        if "github_url" in refreshed_columns and "project_link" in refreshed_columns:
            conn.execute(
                text(
                    "UPDATE student_projects SET project_link = github_url WHERE project_link IS NULL AND github_url IS NOT NULL"
                )
            )

        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_student_projects_user_id ON student_projects (user_id)"))
