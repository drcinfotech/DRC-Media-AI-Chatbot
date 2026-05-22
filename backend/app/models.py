"""Pydantic models for the Media AI Chatbot."""
from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None


class TextBlock(BaseModel):
    type: Literal["text"] = "text"
    content: str


class DisclaimerBlock(BaseModel):
    type: Literal["disclaimer"] = "disclaimer"
    content: str


class ContentSafetyBlock(BaseModel):
    type: Literal["content_safety"] = "content_safety"
    headline: str
    message: str
    indicators: list[str]
    offer: str


class TitleListBlock(BaseModel):
    type: Literal["title_list"] = "title_list"
    title: Optional[str] = None
    items: list[dict]
    total: int


class TitleDetailBlock(BaseModel):
    type: Literal["title_detail"] = "title_detail"
    title: dict


class TrailerBlock(BaseModel):
    type: Literal["trailer"] = "trailer"
    title_id: str
    title: str
    duration_seconds: int
    note: str


class ContinueWatchingBlock(BaseModel):
    type: Literal["continue_watching"] = "continue_watching"
    items: list[dict]


class WatchlistBlock(BaseModel):
    type: Literal["watchlist"] = "watchlist"
    items: list[dict]


class DownloadsBlock(BaseModel):
    type: Literal["downloads"] = "downloads"
    items: list[dict]


class RecommendationBlock(BaseModel):
    type: Literal["recommendation"] = "recommendation"
    rationale: str
    items: list[dict]


class ProfilesBlock(BaseModel):
    type: Literal["profiles"] = "profiles"
    items: list[dict]
    active_profile: Optional[str] = None


class PlansBlock(BaseModel):
    type: Literal["plans"] = "plans"
    items: list[dict]
    current_plan_id: Optional[str] = None


class SubscriptionBlock(BaseModel):
    type: Literal["subscription"] = "subscription"
    plan: dict
    subscription: dict


class DevicesBlock(BaseModel):
    type: Literal["devices"] = "devices"
    items: list[dict]


class ParentalControlsBlock(BaseModel):
    type: Literal["parental_controls"] = "parental_controls"
    kids_profile: dict
    age_ratings_blocked: list[str]
    note: str


MessageBlock = (
    TextBlock | DisclaimerBlock | ContentSafetyBlock
    | TitleListBlock | TitleDetailBlock | TrailerBlock
    | ContinueWatchingBlock | WatchlistBlock | DownloadsBlock
    | RecommendationBlock | ProfilesBlock | PlansBlock
    | SubscriptionBlock | DevicesBlock | ParentalControlsBlock
)


class ChatResponse(BaseModel):
    session_id: str
    intent: str
    confidence: float
    blocks: list[MessageBlock]
    suggestions: list[str] = []
    safety_flag: Optional[str] = None
