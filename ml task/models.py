class PricingLogic:
    base_price = 500  # Example base price

    @staticmethod
    def get_initial_price(product_id):
        # In a real-world app, you'd fetch this from a database or external service
        return PricingLogic.base_price

    @staticmethod
    def handle_user_offer(user_id, offer_price):
        min_price = 450  # Minimum price the bot will accept
        if offer_price >= PricingLogic.base_price:
            return offer_price  # Accept the user's offer
        elif offer_price >= min_price:
            return offer_price + 20  # Counter slightly above the user's offer
        else:
            return min_price  # Offer the minimum acceptable price
