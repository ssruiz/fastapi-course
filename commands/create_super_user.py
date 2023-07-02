import asyncclick as click

from db import LocalSession
from models import RoleType, User


@click.command()
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-pw", "--password", type=str, required=True)
async def create_user(first_name, last_name, email, phone, iban, password):
    user_data = {"first_name": first_name, "last_name": last_name, "email": email, "iban": iban, "phone": phone,
                 "password": password, "role": RoleType.admin}
    print(user_data)
    with LocalSession() as session:
        user = User(**user_data)
        session.add(user)
        session.commit()


if __name__ == '__main__':
    create_user(_anyio_backend="asyncio")
