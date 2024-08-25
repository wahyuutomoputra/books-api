from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    # Menyertakan panjang maksimum 255 karakter untuk nama
    name = Column(String(255), index=True)
    # Menggunakan tipe Text untuk bio, tanpa panjang maksimum yang diperlukan
    bio = Column(Text)
    birth_date = Column(Date)

    books = relationship("Book", back_populates="author")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None
        }
