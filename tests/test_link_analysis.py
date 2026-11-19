import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from google.genai.errors import APIError

from app.main import app
from app.schemas import Analysis


class LinkAnalysisErrorTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.payload = {"url": "https://example.com"}

    def test_website_extraction_error_returns_400(self):
        with patch(
            "app.main.extract_website_content",
            new_callable=AsyncMock,
            side_effect=ValueError("Unable to access website"),
        ):
            response = self.client.post(
                "/link-analysis",
                json=self.payload,
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Unable to access website")

    def test_success_response_uses_business_category(self):
        website_data = {
            "url": self.payload["url"],
            "title": "Example Software",
            "description": "Software for small businesses.",
            "headings": [],
            "content": "Business software",
        }
        analysis = Analysis.model_validate({
            "competitor_analysis": {
                "brand_overview": "A software company for small businesses.",
                "main_business_category": "Business software",
                "competitors": [],
                "strengths": [],
                "opportunities": [],
            },
            "target_search_queries": [
                {
                    "query": f"example service {index}",
                    "platforms": [
                        ["Google"],
                        ["Facebook"],
                        ["Instagram"],
                        ["LinkedIn"],
                        ["X"],
                    ][index],
                    "intent": "Service discovery",
                    "business_relevance": "Relevant service",
                    "target_audience": "Small businesses",
                }
                for index in range(5)
            ],
            "seo_improvements": {
                "primary_keyword": "business software",
                "secondary_keywords": [],
                "long_tail_keywords": [],
                "recommended_title": "Business Software",
                "meta_description": "Software for small businesses.",
                "supporting_content": [],
            },
            "top_services": [
                {
                    "name": f"Example service {index}",
                    "description": "Example description",
                    "target_industry": "Technology",
                    "target_customer": "Small businesses",
                    "main_benefit": "Saves time",
                    "source_type": "inferred recommendation",
                }
                for index in range(5)
            ],
            "target_audience": {
                "primary_audience": [],
                "secondary_audience": [],
                "industries": [],
                "business_types": [],
                "customer_profiles": [],
                "geographical_focus": [],
                "customer_needs": [],
                "customer_interests": [],
                "marketing_segments": [],
            },
        })

        with patch(
            "app.main.extract_website_content",
            new_callable=AsyncMock,
            return_value=website_data,
        ):
            with patch(
                "app.main.analyze_website",
                new_callable=AsyncMock,
                return_value=analysis,
            ):
                response = self.client.post(
                    "/link-analysis",
                    json=self.payload,
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["brand"]["category"],
            "Business software",
        )
        self.assertEqual(
            response.json()["analysis"]["competitor_analysis"][
                "main_business_category"
            ],
            "Business software",
        )
        self.assertEqual(
            len(response.json()["analysis"]["target_search_queries"]),
            5,
        )
        self.assertEqual(
            len(response.json()["analysis"]["top_services"]),
            5,
        )

    def test_gemini_error_returns_logged_502(self):
        website_data = {
            "url": self.payload["url"],
            "title": "Example",
            "description": "",
            "headings": [],
            "content": "",
        }
        with patch(
            "app.main.extract_website_content",
            new_callable=AsyncMock,
            return_value=website_data,
        ):
            with patch(
                "app.main.analyze_website",
                new_callable=AsyncMock,
                side_effect=APIError(503, {}),
            ):
                with self.assertLogs("app.main", level="ERROR"):
                    response = self.client.post(
                        "/link-analysis",
                        json=self.payload,
                    )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.json()["detail"],
            "Website analysis failed. Please try again.",
        )

    def test_openapi_documents_error_responses(self):
        openapi = self.client.get("/openapi.json").json()
        responses = openapi["paths"]["/link-analysis"]["post"]["responses"]

        self.assertIn("400", responses)
        self.assertIn("502", responses)
        self.assertIn("422", responses)


if __name__ == "__main__":
    unittest.main()