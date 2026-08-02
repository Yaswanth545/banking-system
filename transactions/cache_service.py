from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """
    Handles Redis cache operations.
    """

    @staticmethod
    def transaction_history_key(user_id):
        return f"transaction_history_{user_id}"
    

    @staticmethod
    def get_transaction_history(user_id):

        key = CacheService.transaction_history_key(user_id)

        data = cache.get(key)

        if data:
            logger.info(
                "Cache HIT for transaction history. User=%s",
                user_id,
            )
        else:
            logger.info(
                "Cache MISS for transaction history. User=%s",
                user_id,
            )

        return data
    

        
    @staticmethod
    def set_transaction_history(user_id,data,):

        key = CacheService.transaction_history_key(
            user_id
        )

        cache.set(
            key,
            data,
            timeout=300,
        )

    @staticmethod
    def clear_transaction_history(user_id):

        key = CacheService.transaction_history_key(
            user_id
        )

        cache.delete(key)

        logger.info(
            "Transaction history cache cleared. User=%s",
            user_id,
        )