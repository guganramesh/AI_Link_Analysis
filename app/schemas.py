from pydantic import BaseModel, Field
from typing import List


class Competitor(BaseModel):
    name: str
    overview: str
    strengths: List[str]
    weaknesses: List[str]
    source_type: str


class CompetitorAnalysis(BaseModel):
    brand_overview: str
    main_business_category: str
    competitors: List[Competitor]
    strengths: List[str]
    opportunities: List[str]


class SearchQuery(BaseModel):
    query: str
    platforms: List[str]
    intent: str
    business_relevance: str
    target_audience: str


class SEOImprovements(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str]
    long_tail_keywords: List[str]
    recommended_title: str
    meta_description: str
    supporting_content: List[str]


class Service(BaseModel):
    name: str
    description: str
    target_industry: str
    target_customer: str
    main_benefit: str
    source_type: str


class TargetAudience(BaseModel):
    primary_audience: List[str]
    secondary_audience: List[str]
    industries: List[str]
    business_types: List[str]
    customer_profiles: List[str]
    geographical_focus: List[str]
    customer_needs: List[str]
    customer_interests: List[str]
    marketing_segments: List[str]


class Analysis(BaseModel):
    competitor_analysis: CompetitorAnalysis
    target_search_queries: List[SearchQuery] = Field(
        min_length=5,
        max_length=5,
    )
    seo_improvements: SEOImprovements
    top_services: List[Service] = Field(
        min_length=5,
        max_length=5,
    )
    target_audience: TargetAudience


class LinkAnalysisRequest(BaseModel):
    url: str


class LinkAnalysisResponse(BaseModel):
    success: bool
    website: str
    brand: dict
    analysis: Analysis