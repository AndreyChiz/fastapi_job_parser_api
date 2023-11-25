from dataclasses import dataclass, field
from typing import Dict, Optional, List


@dataclass
class Page:
    """Содержит данные для выполнения запроса"""
    url: str
    params: Optional[Dict] = field(default_factory=dict)


@dataclass
class OrderData:
    """
    Содержит данные заказ
    """
    id: int
    url: str
    title: Optional[str] = None
    post_date: Optional[str] = None
    price: Optional[int] = None
    location: Optional[str] = None
    seller: Optional[str] = None
    description: Optional[str] = None
    views: Optional[int] = None
    expiration_date: Optional[str] = None
    categories: Optional[str] = None
    images: Optional[List] = field(default_factory=list)
