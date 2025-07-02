class ProductFinanceSystem:
    """Integrate inflation and currency mechanics with products."""

    def __init__(self, inflation, currency, display_currency="Base"):
        self.inflation = inflation
        self.currency = currency
        self.display_currency = display_currency

    def advance_day(self, products, shock=False, promotion_effect=0.0):
        """Advance one day applying inflation to given products."""
        self.inflation.apply_inflation(products, shock=shock, promotion_effect=promotion_effect)

    def product_price(self, product, from_currency="Base"):
        """Return product price converted to the display currency."""
        return self.currency.convert(product.price, from_currency, self.display_currency)
