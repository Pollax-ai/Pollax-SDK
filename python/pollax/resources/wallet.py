"""Wallet resource"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Pollax


class WalletResource:
    """Wallet / billing balance API resource"""

    def __init__(self, client: "Pollax"):
        self._client = client

    def get(self) -> dict:
        """Get current wallet balance (INR / paise)."""
        return self._client.request("GET", "/api/v1/wallet")

    def retrieve(self) -> dict:
        """Alias for :meth:`get`."""
        return self.get()

    def ledger(self, limit: Optional[int] = None, page: Optional[int] = None) -> dict:
        """List wallet ledger entries."""
        params = {}
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page
        return self._client.request("GET", "/api/v1/wallet/ledger", params=params or None)
