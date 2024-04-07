from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Machine


async def orm_add_machine(session: AsyncSession, data: dict):

    obj = (Machine(name=data["machine_title"],
                   description=data['machine_desc'],
                   price=data['machine_price'],
                   image=data['machine_image'],
                   url=data['machine_url']))

    session.add(obj)
    await session.commit()


async def orm_get_machines(session: AsyncSession):
    query = select(Machine)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_machine(session: AsyncSession, machine_id: int):
    query = select(Machine).where(Machine.id == machine_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_machine(session: AsyncSession, machine_id: int, data):
    query = update(Machine).where(Machine.id == machine_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"], )
    await session.execute(query)
    await session.commit()


async def orm_delete_machine(session: AsyncSession, machine_id: int):
    query = delete(Machine).where(Machine.id == machine_id)
    await session.execute(query)
    await session.commit()


async def orm_delete_machines(session: AsyncSession):
    query = delete(Machine)
    await session.execute(query)
    await session.commit()


async def orm_exist(session: AsyncSession, name):
    query = select(Machine).where(Machine.name == name)
    result = await session.execute(query)
    existing_user = result.scalar()
    print(result.scalar())

    if existing_user is not None:
        print("Запись существует.")
        return existing_user
    else:
        print("Запись не найдена.")
        return




