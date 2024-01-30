# helpers/serializers.py
from rest_framework import serializers


class CustomDecimalField2f(serializers.DecimalField):
    # usage example: balance_usd_24h_change_percent = CustomDecimalField2f(max_digits=None, decimal_places=None)

    def to_representation(self, value):
        return float(f"{value:.2f}")


class CustomDecimalField6f(serializers.DecimalField):
    def to_representation(self, value):
        return float(f"{value:.6f}")
