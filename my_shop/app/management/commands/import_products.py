import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Product


class Command(BaseCommand):
    help = "Import products from a CSV file using pandas"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file to import")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        df = pd.read_csv(csv_file)

        for index, row in df.iterrows():
            name = row["name"]
            price = row["price"]
            digital = row["digital"]
            image = row["image"] if pd.notna(row["image"]) else None

            product = Product(
                name=name,
                price=price,
                digital=digital,
            )

            if image:
                product.image = image

            product.save()

            self.stdout.write(self.style.SUCCESS(f'Product "{name}" has been added.'))
