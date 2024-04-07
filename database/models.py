from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Machine(Base):
    __tablename__ = 'machine'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # - первичный ключ с автоинкрементом
    name: Mapped[str] = mapped_column(String(300), nullable=False)  # - не может быть пустым и более 300 символов
    description: Mapped[str] = mapped_column(Text)  # - класс Текст (не varchar), в котором может быть большой текст
    price: Mapped[str] = mapped_column(
        String(150))  # можно было бы парсить до float и mapped_column(Float(asdecimal=True), nullable=False)
    image: Mapped[str] = mapped_column(String(150))  # может быть varchar
    url: Mapped[str] = mapped_column(Text)  # - класс Текст (не varchar), в котором может быть большой текст
