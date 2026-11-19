import logging
from json import JSONDecodeError

from fastapi import FastAPI, HTTPException
from google.genai.errors import APIError
from pydantic import ValidationError

from app.schemas import (
    LinkAnalysisRequest,
    LinkAnalysisResponse
)

from app.services.website_extractor import (
    extract_website_content
)

from app.services.llm_service import (
    analyze_website
)


logger = logging.getLogger(__name__)


app = FastAPI(
    title="AI Website Link Analysis API",
    description="AI-powered website business and SEO analysis",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "AI Link Analysis API is running!"
    }


@app.post(
    "/link-analysis",
    response_model=LinkAnalysisResponse,
    responses={
        400: {
            "description": "The website URL is invalid or the website cannot be accessed.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Unable to access website."
                    }
                }
            },
        },
        502: {
            "description": "The AI analysis service failed or returned invalid data.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Website analysis failed. Please try again."
                    }
                }
            },
        },
    },
)
async def link_analysis(request: LinkAnalysisRequest):

    try:
        website_data = await extract_website_content(
            str(request.url)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    try:
        analysis = await analyze_website(
            website_data
        )

    except (APIError, JSONDecodeError, ValidationError):
        logger.exception("Gemini website analysis failed")
        raise HTTPException(
            status_code=502,
            detail="Website analysis failed. Please try again."
        )

    return {
        "success": True,
        "website": website_data["url"],
        "brand": {
            "name": website_data["title"],
            "category": analysis.competitor_analysis.main_business_category,
            "summary": website_data["description"]
        },
        "analysis": analysis
    }