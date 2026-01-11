from app import db
from app import GovRecord

def seed_government_database():

    dummy_records = [
        GovRecord(
            name="Jane Doe",
            email="jane@example.com",
            phone="9876543210",
            pan="ABCDE1234F",
            aadhar="123412341234",
            age=25
        ),
        GovRecord(
            name="Rahul Sharma",
            email="rahul@example.com",
            phone="9123456789",
            pan="BCDEA4321H",
            aadhar="567856785678",
            age=28
        ),
        GovRecord(
            name="Aarav Mehta",
            email="aarav.mehta@example.com",
            phone="9081726354",
            pan="AAAAE1234K",
            aadhar="111122223333",
            age=30
        ),
        GovRecord(
            name="Priya Nair",
            email="priya.nair@example.com",
            phone="9988776655",
            pan="PQRSX6789Z",
            aadhar="444455556666",
            age=27
        ),
        GovRecord(
            name="Vikram Singh",
            email="vikram.singh@example.com",
            phone="9090909090",
            pan="MNOPQ3456R",
            aadhar="777788889999",
            age=32
        ),
        GovRecord(
            name="Sara Thomas",
            email="sara.t@example.com",
            phone="9876501234",
            pan="LMNOP9876T",
            aadhar="222233334444",
            age=29
        )
    ]

    db.session.bulk_save_objects(dummy_records)
    db.session.commit()
    print("Government database seeded successfully.")
