from extensions import db
from models.category import Category


class SeedService:

    @staticmethod
    def seed_categories():

        if Category.query.count() > 0:
            return

        categories = [

            Category(
                name="Power Supply",
                description="Power outage, blackout, voltage fluctuation"
            ),

            Category(
                name="Meter Fault",
                description="Damaged meter, blank display, burnt meter"
            ),

            Category(
                name="Token Issues",
                description="Recharge token and credit problems"
            ),

            Category(
                name="Installation",
                description="New meter installation or replacement"
            ),

            Category(
                name="Billing",
                description="Billing and charging complaints"
            ),

            Category(
                name="Connectivity",
                description="Communication and network problems"
            ),

            Category(
                name="Meter Tampering",
                description="Meter bypass or tampering"
            ),

            Category(
                name="Customer Service",
                description="Staff and service complaints"
            )

        ]

        db.session.add_all(categories)
        db.session.commit()

        print("✓ Default complaint categories created.")