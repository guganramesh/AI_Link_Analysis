import json

from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

from app.schemas import Analysis


client = genai.Client(
    api_key=GEMINI_API_KEY
)


async def analyze_website(website_data):

    prompt = f"""
    You are an expert website business analyst
    and SEO specialist.

    Analyse the following actual website content.

    WEBSITE INFORMATION:

    Title: {website_data['title']}

    Description: {website_data['description']}

    Headings: {website_data['headings']}

    Content: {website_data['content']}

    Generate the following five sections:

    1. Competitor analysis
    2. Five target search queries
    3. SEO improvements
    4. Five important services
    5. Target audience identification

    Rules:

    - Use the actual website content.
    - Do not invent business facts.
    - Do not claim unverified competitors are confirmed.
    - Mark AI-generated competitor suggestions clearly.
    - Do not invent search volume or ranking data.
    - Clearly distinguish extracted facts from inferences.
    - Return valid JSON matching the required schema.
    - Use empty lists for optional information that is genuinely unavailable.
      The two fixed-size lists below must still contain exactly five items.
    - Across the five search queries, cover Google, Facebook,
      Instagram, LinkedIn, and X (Twitter).
    - Return exactly five search queries and exactly five services.
    - For each service, set source_type to "extracted" when found
      in the website or "inferred recommendation" otherwise.
    - Do not describe an inferred service as an existing offering.

    Return JSON with these exact top-level keys:

    competitor_analysis,
    target_search_queries,
    seo_improvements,
    top_services,
    target_audience.

    For competitor_analysis include:
    brand_overview, main_business_category, competitors,
    strengths, opportunities.

    For each competitor include:
    name, overview, strengths, weaknesses, source_type.

    For each search query include:
    query, platforms, intent, business_relevance,
    target_audience.

    For seo_improvements include:
    primary_keyword, secondary_keywords,
    long_tail_keywords, recommended_title,
    meta_description, supporting_content.

    For each service include:
    name, description, target_industry,
    target_customer, main_benefit, source_type.

    For target_audience include:
    primary_audience, secondary_audience,
    industries, business_types, customer_profiles,
    geographical_focus, customer_needs,
    customer_interests, marketing_segments.
    """

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Analysis
        )
    )

    result = json.loads(response.text)

    return Analysis.model_validate(result)