"""Phone numbers resource"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from ..models import PhoneNumber

if TYPE_CHECKING:
    from ..client import Pollax


def _as_phone_list(response) -> List[PhoneNumber]:
    if isinstance(response, list):
        items = response
    elif isinstance(response, dict):
        items = response.get("numbers") or response.get("data") or []
    else:
        items = []
    return [PhoneNumber(**item) if isinstance(item, dict) else item for item in items]


class PhoneNumbersResource:
    """Phone Numbers API resource"""

    def __init__(self, client: "Pollax"):
        self._client = client

    def list(self) -> List[PhoneNumber]:
        """List all phone numbers."""
        response = self._client.request("GET", "/api/v1/phone-numbers")
        return _as_phone_list(response)

    def search(
        self,
        country_code: Optional[str] = None,
        area_code: Optional[str] = None,
        contains: Optional[str] = None,
        limit: int = 10,
    ) -> List[PhoneNumber]:
        """Search available phone numbers."""
        params: Dict[str, Any] = {"limit": limit}
        if country_code:
            params["country_code"] = country_code
        if area_code:
            params["area_code"] = area_code
        if contains:
            params["contains"] = contains

        response = self._client.request("GET", "/api/v1/phone-numbers/search", params=params)
        return _as_phone_list(response)

    def purchase(self, phone_number: str) -> PhoneNumber:
        """Purchase a phone number."""
        response = self._client.request(
            "POST",
            "/api/v1/phone-numbers",
            json={"phone_number": phone_number},
        )
        return PhoneNumber(**response)

    def update(self, number_id: str, **kwargs) -> PhoneNumber:
        """Update a owned phone number (e.g. auto_renew=True/False)."""
        response = self._client.request(
            "PUT",
            f"/api/v1/phone-numbers/{number_id}",
            json=kwargs,
        )
        return PhoneNumber(**response)

    def release(self, number_id: str) -> dict:
        """Release a phone number."""
        return self._client.request("DELETE", f"/api/v1/phone-numbers/{number_id}")

    def get_number_request(self) -> Optional[dict]:
        """Get the open dedicated-number request for this account, if any."""
        response = self._client.request("GET", "/api/v1/phone-numbers/number-request")
        if isinstance(response, dict):
            return response.get("request")
        return None

    def request_number(self, **kwargs) -> dict:
        """Ask Pollax for a dedicated inbound number.

        Common fields: name, email, phone, note, requested_via.
        Returns ``{"created": bool, "request": dict|None}``.
        """
        response = self._client.request(
            "POST",
            "/api/v1/phone-numbers/number-request",
            json=kwargs or {},
        )
        return {
            "created": bool(response.get("created")) if isinstance(response, dict) else False,
            "request": (response.get("request") if isinstance(response, dict) else None),
        }

    def assign(self, number_id: str, agent_id: str) -> PhoneNumber:
        """Assign a phone number to an agent."""
        response = self._client.request(
            "POST",
            f"/api/v1/phone-numbers/{number_id}/assign",
            json={"agent_id": agent_id},
        )
        return PhoneNumber(**response)

    def unassign(self, number_id: str) -> PhoneNumber:
        """Unassign a phone number from its agent."""
        response = self._client.request(
            "POST",
            f"/api/v1/phone-numbers/{number_id}/unassign",
        )
        return PhoneNumber(**response)

    def provision(self, number_id: str, inbound_provider: Optional[str] = None, **kwargs) -> dict:
        """Provision inbound telephony for a number."""
        body = dict(kwargs)
        if inbound_provider:
            body["inbound_provider"] = inbound_provider
        return self._client.request(
            "POST",
            f"/api/v1/phone-numbers/{number_id}/provision",
            json=body,
        )

    def deprovision(self, number_id: str) -> dict:
        """Deprovision inbound telephony for a number."""
        return self._client.request(
            "POST",
            f"/api/v1/phone-numbers/{number_id}/deprovision",
        )
