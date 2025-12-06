# core/management/commands/load_ohlc.py
import json
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models.game import Asset, ChartSnapshot

class Command(BaseCommand):
    help = "Load OHLC JSON and create ChartSnapshot entries. Usage: python manage.py load_ohlc --file=./data/ohlc.json --count=200"

    def add_arguments(self, parser):
        parser.add_argument("--file", "-f", required=True, help="Path to OHLC JSON file")
        parser.add_argument("--count", "-c", type=int, default=200, help="Number of snapshots to create")
        parser.add_argument("--visible_min", type=int, default=50)
        parser.add_argument("--visible_max", type=int, default=100)
        parser.add_argument("--outcome_min", type=int, default=10)
        parser.add_argument("--outcome_max", type=int, default=20)

    def handle(self, *args, **options):
        file_path = options["file"]
        count = options["count"]
        visible_min = options["visible_min"]
        visible_max = options["visible_max"]
        outcome_min = options["outcome_min"]
        outcome_max = options["outcome_max"]

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to open JSON file: {e}"))
            return

        symbols = [s for s, arr in data.items() if isinstance(arr, list) and len(arr) >= (visible_min + outcome_min)]
        if not symbols:
            self.stderr.write(self.style.ERROR("No symbols with enough candles found in JSON."))
            return

        created = 0
        with transaction.atomic():
            for _ in range(count):
                symbol = random.choice(symbols)
                series = data[symbol]
                # choose lens
                visible_len = random.randint(visible_min, visible_max)
                outcome_len = random.randint(outcome_min, outcome_max)
                max_start = len(series) - visible_len - outcome_len
                if max_start <= 0:
                    continue
                start = random.randint(0, max_start - 1) if max_start > 1 else 0

                visible = series[start:start+visible_len]
                outcome = series[start+visible_len:start+visible_len+outcome_len]

                # Ensure asset exists
                asset, _ = Asset.objects.get_or_create(symbol=symbol)

                ChartSnapshot.objects.create(
                    asset=asset,
                    visible_candles=visible,
                    outcome_candles=outcome,
                    timeframe="1h",  # если у тебя в данных разный timeframe — можно добавить поле в JSON и брать оттуда
                    visible_len=len(visible),
                    outcome_len=len(outcome),
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} ChartSnapshot(s)"))
