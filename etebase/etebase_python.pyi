import typing as t

from enum import Enum

class Utils:
    @classmethod
    def from_base64(cls, value: str) -> bytes: ...

    @classmethod
    def to_base64(cls, value: bytes) -> str: ...

    @classmethod
    def randombytes(cls, value: int) -> bytes: ...

    @classmethod
    def pretty_fingerprint(cls, value: bytes) -> str: ...


class Client:
    @classmethod
    def new(cls, client_name: str, server_url: str) -> "Client": ...

    def set_server_url(self, server_url: str): ...

    @classmethod
    def get_default_server_url(cls) -> str: ...


class User:
    def __init__(self, username: str, email: str) -> "User": ...

    def set_username(self, username: str): ...
    def get_username(self) -> str: ...

    def set_email(self, email: str): ...
    def get_email(self) -> str: ...


class Account:
    @classmethod
    def is_etebase_server(cls, client: Client) -> bool: ...

    @classmethod
    def login(cls, client: Client, username: str, password: str) -> Account: ...
    @classmethod
    def login_key(cls, client: Client, username: str, main_key: bytes) -> Account: ...
    @classmethod
    def signup(cls, client: Client, user: User, password: str) -> Account: ...
    @classmethod
    def signup_key(cls, client: Client, user: User, main_key: bytes) -> Account: ...

    def fetch_token(self): ...
    def force_server_url(self, api_base: str): ...

    def change_password(self, password: str): ...
    def logout(self): ...
    def get_collection_manager(self) -> "CollectionManager": ...
    def get_invitation_manager(self) -> "CollectionInvitationManager": ...

    def save(self, encryption_key: t.Optional[bytes]) -> str: ...
    @classmethod
    def restore(cls, client: Client, account_data_stored: str, encryption_key: t.Optional[bytes]) -> Account: ...


class RemovedCollection:
    def get_uid(self) -> str: ...

class CollectionListResponse:
    def get_stoken(self) -> str: ...
    def get_data(self) -> t.List["Collection"]: ...
    def is_done(self) -> bool: ...
    def get_removed_memberships(self) -> t.List[RemovedCollection]: ...


class ItemListResponse:
    def get_stoken(self) -> str: ...
    def get_data(self) -> t.List["Item"]: ...
    def is_done(self) -> bool: ...


class ItemRevisionsListResponse:
    def get_iterator(self) -> str: ...
    def get_data(self) -> t.List["Item"]: ...
    def is_done(self) -> bool: ...


class PrefetchOption(str, Enum):
    Auto: str
    Medium: str


class FetchOptions:
    def limit(self, limit: int): ...
    def prefetch(self, prefetch: PrefetchOption): ...
    def with_collection(self, with_collection: bool): ...
    def iterator(self, iterator: t.Optional[str]): ...
    def stoken(self, stoken: t.Optional[str]): ...


class ItemMetadata:
    def set_item_type(self, type_: t.Optional[str]): ...
    def set_name(self, name: t.Optional[str]): ...
    def set_mtime(self, mtime: t.Optional[int]): ...
    def get_item_type(self) -> t.Optional[str]: ...
    def get_name(self) -> t.Optional[str]: ...
    def get_mtime(self) -> t.Optional[int]: ...
    def set_description(self, description: t.Optional[str]): ...
    def set_color(self, color: t.Optional[str]): ...
    def get_description(self) -> t.Optional[str]: ...
    def get_color(self) -> t.Optional[str]: ...


class CollectionManager:
    def fetch(self, col_uid: str, fetch_options: t.Optional[FetchOptions]) -> "Collection": ...
    def create(self, collection_type: str, meta: ItemMetadata, content: bytes) -> "Collection": ...
    def create_raw(self, collection_type: str, meta: bytes, content: bytes) -> "Collection": ...
    def get_item_manager(self, col: "Collection") -> "ItemManager": ...
    def list(self, collection_type: str, fetch_options: t.Optional[FetchOptions]) -> CollectionListResponse: ...
    def list_multi(self, collection_types: t.List[str], fetch_options: t.Optional[FetchOptions]) -> CollectionListResponse: ...
    def upload(self, collection: "Collection", fetch_options: t.Optional[FetchOptions]): ...
    def transaction(self, collection: "Collection", fetch_options: t.Optional[FetchOptions]): ...
    def cache_load(self, cached: bytes) -> "Collection": ...
    def cache_save(self, collection: "Collection") -> bytes: ...
    def cache_save_with_content(self, collection: "Collection") -> bytes: ...

    def get_member_manager(self, col: "Collection") -> "CollectionMemberManager": ...


class ItemManager:
    def fetch(self, item_uid: str, fetch_options: t.Optional[FetchOptions]) -> "Item": ...
    def create(self, meta: ItemMetadata, content: bytes) -> "Item": ...
    def create_raw(self, meta: bytes, content: bytes) -> "Item": ...
    def list(self, fetch_options: t.Optional[FetchOptions]) -> ItemListResponse: ...
    def item_revisions(self, item: "Item", fetch_options: t.Optional[FetchOptions]) -> ItemRevisionsListResponse: ...
    def fetch_updates(self, items: t.List["Item"], fetch_options: t.Optional[FetchOptions]) -> ItemListResponse: ...
    def fetch_multi(self, items: t.List[str], fetch_options: t.Optional[FetchOptions]) -> ItemListResponse: ...
    def batch(self, items: t.List["Item"], deps: t.Optional[t.List["Item"]], fetch_options: t.Optional[FetchOptions]): ...
    def transaction(self, items: t.List["Item"], deps: t.Optional[t.List["Item"]], fetch_options: t.Optional[FetchOptions]): ...
    def download_content(self, item: "Item"): ...
    def upload_content(self, item: "Item"): ...
    def cache_load(self, cached: bytes) -> "Item": ...
    def cache_save(self, item: "Item") -> bytes: ...
    def cache_save_with_content(self, item: "Item") -> bytes: ...


class CollectionAccessLevel(int, Enum):
    ReadOnly: int
    Admin: int
    ReadWrite: int


class Collection:
    def verify(self) -> bool: ...

    def set_meta(self, meta: ItemMetadata): ...
    def get_meta(self) -> ItemMetadata: ...
    def set_meta_raw(self, meta: bytes): ...
    def get_meta_raw(self) -> bytes: ...
    def set_content(self, content: bytes): ...
    def get_content(self) -> bytes: ...
    def delete(self): ...
    def is_deleted(self) -> bool: ...
    def get_uid(self) -> str: ...
    def get_etag(self) -> str: ...
    def get_stoken(self) -> t.Optional[str]: ...
    def get_access_level(self) -> CollectionAccessLevel: ...
    def get_item(self) -> "Item": ...
    def get_collection_type(self) -> str: ...


class Item:
    def verify(self) -> bool: ...

    def set_meta(self, meta: ItemMetadata): ...
    def get_meta(self) -> ItemMetadata: ...
    def set_meta_raw(self, meta: bytes): ...
    def get_meta_raw(self) -> bytes: ...
    def set_content(self, content: bytes): ...
    def get_content(self) -> bytes: ...
    def delete(self): ...
    def is_deleted(self) -> bool: ...
    def is_missing_content(self) -> bool: ...
    def get_uid(self) -> str: ...
    def get_etag(self) -> str: ...


class UserProfile:
    def get_pubkey(self) -> bytes: ...


class InvitationListResponse:
    def get_iterator(self) -> str: ...
    def get_data(self) -> t.List["SignedInvitation"]: ...
    def is_done(self) -> bool: ...


class CollectionInvitationManager:
    def list_incoming(self, options: t.Optional[FetchOptions]) -> InvitationListResponse: ...
    def list_outgoing(self, options: t.Optional[FetchOptions]) -> InvitationListResponse: ...
    def accept(self, invitation: "SignedInvitation"): ...
    def reject(self, invitation: "SignedInvitation"): ...
    def fetch_user_profile(self, username: str) -> UserProfile: ...
    def invite(self, collection: Collection, username: str, pubkey: bytes, access_level: CollectionAccessLevel): ...
    def disinvite(self, invitation: "SignedInvitation"): ...
    def get_pubkey(self) -> bytes: ...


class SignedInvitation:
    def get_uid(self) -> str: ...
    def get_username(self) -> str: ...
    def get_collection(self) -> str: ...
    def get_access_level(self) -> CollectionAccessLevel: ...
    def get_from_pubkey(self) -> bytes: ...


class CollectionMember:
    def get_username(self) -> str: ...
    def get_access_level(self) -> CollectionAccessLevel: ...


class MemberListResponse:
    def get_iterator(self) -> str: ...
    def get_data(self) -> t.List["CollectionMember"]: ...
    def is_done(self) -> bool: ...


class CollectionMemberManager:
    def list(self, fetch_options: t.Optional[FetchOptions]) -> MemberListResponse: ...
    def remove(self, username: str): ...
    def leave(self): ...
    def modify_access_level(self, username: str, access_level: CollectionAccessLevel): ...
