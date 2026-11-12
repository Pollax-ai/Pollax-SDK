"""Knowledge resource"""

from typing import List, Optional, TYPE_CHECKING, Union, BinaryIO, Any
from ..models import KnowledgeDocument

if TYPE_CHECKING:
    from ..client import Pollax


class KnowledgeResource:
    """Knowledge Base API resource"""

    def __init__(self, client: "Pollax"):
        self._client = client

    def create(
        self,
        name: str,
        content: str,
        doc_type: str = "txt",
        agent_id: Optional[str] = None,
    ) -> KnowledgeDocument:
        """Create a knowledge document from plain text (JSON body)."""
        data: dict = {"name": name, "content": content, "type": doc_type}
        if agent_id:
            data["agent_id"] = agent_id
        response = self._client.request("POST", "/api/v1/knowledge", json=data)
        return KnowledgeDocument(**response)

    def upload(
        self,
        name: str,
        file: Optional[Union[BinaryIO, bytes]] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        doc_type: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> KnowledgeDocument:
        """Upload a document via multipart POST /knowledge."""
        files = {}
        data: dict = {"name": name}

        if file is not None:
            files["file"] = file
        if content:
            data["content"] = content
        if url:
            data["url"] = url
        if doc_type:
            data["type"] = doc_type
        if agent_id:
            data["agent_id"] = agent_id

        response = self._client.request(
            "POST",
            "/api/v1/knowledge",
            files=files if files else None,
            data=data,
        )
        return KnowledgeDocument(**response)

    def upload_file(
        self,
        file: Union[BinaryIO, bytes, tuple],
        *,
        filename: Optional[str] = None,
        name: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> KnowledgeDocument:
        """Upload a file via POST /knowledge/upload."""
        data: dict = {}
        if name:
            data["name"] = name
        if agent_id:
            data["agent_id"] = agent_id

        if isinstance(file, tuple):
            files = {"file": file}
        elif filename:
            files = {"file": (filename, file)}
        else:
            files = {"file": file}

        response = self._client.request(
            "POST",
            "/api/v1/knowledge/upload",
            files=files,
            data=data or None,
        )
        return KnowledgeDocument(**response)

    def add_url(
        self,
        url: str,
        name: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> KnowledgeDocument:
        """Ingest knowledge from a public URL."""
        body: dict = {"url": url}
        if name:
            body["name"] = name
        if agent_id:
            body["agent_id"] = agent_id
        response = self._client.request("POST", "/api/v1/knowledge/url", json=body)
        return KnowledgeDocument(**response)

    def stats(self) -> dict:
        """Knowledge base aggregate stats for the account."""
        return self._client.request("GET", "/api/v1/knowledge/stats")

    def list(self) -> List[KnowledgeDocument]:
        """List all knowledge documents."""
        response = self._client.request("GET", "/api/v1/knowledge")
        items = response if isinstance(response, list) else (response.get("data") or [])
        return [KnowledgeDocument(**item) for item in items]

    def retrieve(self, document_id: str) -> KnowledgeDocument:
        """Get a single document by ID (includes readable content when available)."""
        response = self._client.request("GET", f"/api/v1/knowledge/{document_id}")
        return KnowledgeDocument(**response)

    def delete(self, document_id: str) -> dict:
        """Delete a document."""
        return self._client.request("DELETE", f"/api/v1/knowledge/{document_id}")

    def search(self, query: str, limit: int = 5) -> dict:
        """Search the knowledge base."""
        return self._client.request(
            "POST",
            "/api/v1/knowledge/search",
            json={"query": query, "limit": limit},
        )
