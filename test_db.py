from sqlalchemy import text
from app.db.session import get_session


def main() -> None:
    session = get_session()
    try:
        # SQLAlchemy 2.x: باید از text() استفاده کنیم
        result = session.execute(text("SELECT 1"))
        print("DB OK, result:", list(result))
    finally:
        session.close()


if __name__ == "__main__":
    main()
