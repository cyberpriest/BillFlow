from database import Base,engine,SessonLocal
from sqlalchemy.orm import Session
import faker,models
from collections import deque

fake = faker.Faker()

def run():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print('Database tables created successfully.')


def seed_Business(db,count:int = 10):
    b = deque()
    for _ in range(count):
        business = models.Business(
            name=fake.company(),
            email=fake.email(),
            phone=fake.phone_number(),
            owner_id=fake.random_int(min=1, max=5)
        )
        db.add(business)
        b.append(business)

    db.commit()
    print(" successfully seeded Business")
    return b



def seed_Client(db,count:int=10):
    c = deque()
    for _ in range(count):
        client = models.Client(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            business_id=fake.random_int(min=1, max=10)
        )
        db.add(client)
        c.append(client)

    db.commit()
    print(" successfully seeded Client")
    return c

def seed_Invoice(db,count:int=10):
    i = deque()
    for _ in range(count):
        invoice = models.Invoice(
            amount=fake.random_number(digits=5),
            status=fake.random_element(elements=('paid', 'unpaid', 'overdue')),
            business_id=fake.random_int(min=1, max=10)
        )
        db.add(invoice)
        i.append(invoice)


    db.commit()
    print(" successfully seeded Invoice")
    return i

def execute():
    run()
    db: Session = SessonLocal()
    try:

        seed_Business(db)
        seed_Client(db)
        seed_Invoice(db)
    finally:
        db.close()

if __name__ == '__main__':
    execute()