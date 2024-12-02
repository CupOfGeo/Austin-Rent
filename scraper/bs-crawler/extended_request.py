from crawlee import Request
from typing import Any, Dict
from crawlee._types import HttpHeaders, HttpMethod, HttpPayload

class ExtendedRequest(Request):
    @classmethod
    def from_url(
        cls,
        url: str,
        *,
        method: HttpMethod = 'GET',
        headers: HttpHeaders | dict[str, str] | None = None,
        payload: HttpPayload | str | None = None,
        label: str | None = None,
        unique_key: str | None = None,
        id: str | None = None,
        keep_url_fragment: bool = False,
        use_extended_unique_key: bool = False,
        always_enqueue: bool = False,
        metadata: Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> 'ExtendedRequest':
        request = Request.from_url(
            url=url,
            method=method,
            headers=headers,
            payload=payload,
            label=label,
            unique_key=unique_key,
            id=id,
            keep_url_fragment=keep_url_fragment,
            use_extended_unique_key=use_extended_unique_key,
            always_enqueue=always_enqueue,
            metadata=metadata,
            **kwargs,
        )
        request.user_data.update(metadata)
        return request