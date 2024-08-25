from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)  # Menyertakan panjang maksimum 255 karakter untuk title
    description = Column(String(1000))  # Menyertakan panjang maksimum 1000 karakter untuk description
    publish_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "publish_date": self.publish_date.isoformat() if self.publish_date else None,
            "author_id": self.author_id
        }
