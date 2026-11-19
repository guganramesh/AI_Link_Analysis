# AI Website Link Analysis API

A FastAPI service that fetches a public website, extracts its visible page content, and uses Gemini to return structured business, competitor, search-query, SEO, service, and audience analysis.

## Requirements

- Python 3.10+
- A Google Gemini API key

## Run locally

From the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `GEMINI_API_KEY` in `.env` to a key from Google AI Studio. `GEMINI_MODEL` is optional and defaults to `gemini-3.8-flash`.

Start the API:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

- Health check: <http://localhost:4000/>
- Interactive API docs: <http://localhost:4000/docs>

## API

`POST /link-analysis`

Request:

```json
{
  "url": "https://example.com"
}
```

Example request using curl:

```bash
curl -X POST http://localhost:4000/link-analysis \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://example.com\"}"
```

The successful response has `success`, `website`, `brand`, and `analysis` fields. `analysis` contains:

- `competitor_analysis`: overview, main business category, competitors, strengths, and opportunities
- `target_search_queries`: five suggested queries covering Google, Facebook, Instagram, LinkedIn, and X
- `seo_improvements`: keyword suggestions, title, meta description, and supporting content
- `top_services`: five services
- `target_audience`: audience and marketing segments

Competitor information is labeled as an AI-generated suggestion when it has not been independently verified. Search volume and ranking data are not fabricated. Website access/URL errors return HTTP 400, and LLM failures return HTTP 502.

## Model selection and cost

Comparison checked against provider documentation on **November 19, 2026**. Prices are standard API rates in USD per million tokens, before discounts, caching, or taxes. Provider descriptions of speed are qualitative; latency and task accuracy have **not** been benchmarked by this project.

| Provider / model | Input / output price | Context | JSON output | Speed / accuracy notes |
|---|---:|---:|---|---|
| Google Gemini 3.8 Flash (configured) | $0.75 / $3.75 | 1,048,576 input tokens | Structured output supported | Vendor positions it as a fast, efficient Flash model; accuracy not independently measured |
| OpenAI GPT-5.4 mini | $0.75 / $4.50 | 400,000 context; 272,000 max input | Structured outputs supported | Vendor describes it as faster and efficient for high-volume workloads; accuracy not independently measured |
| Anthropic Claude Haiku 5.5 | $0.10 / $0.50 for prompts up to 100,000 tokens | 1,000,000 tokens | Structured outputs supported | Vendor describes it as its fastest model; accuracy not independently measured |

For an illustrative request of **4,000 input tokens and 1,000 output tokens**, standard paid pricing is approximately:

- Gemini 3.8 Flash: **$0.00675**
- GPT-5.4 mini: **$0.00750**
- Claude Haiku 5.5: **$0.00090** (within its up-to-100K-token price tier)

These are token-price calculations, not measured per-request bills or response-time results. Gemini 3.8 Flash is the implementation choice because the Google GenAI SDK supports Pydantic response schemas used by this project, and the model offers a large context window at a low standard rate. Haiku 5.5 is the lower-cost candidate; run a representative evaluation before switching, especially for competitor suggestions and evidence fidelity.

Cost controls in this implementation include removing non-content HTML elements, limiting extracted text, and making one structured LLM request per analysis. For production, consider caching by normalized URL plus content hash and monitoring actual token usage.

Official references:

- [Gemini 3.8 Flash model details](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [GPT-5.4 mini details and pricing](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
- [Claude model overview](https://platform.claude.com/docs/en/models/overview)
- [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

## Tests

Run the API tests with:

```powershell
python -m unittest discover -s tests -v
```

The tests cover successful response mapping, extraction and LLM error handling, and OpenAPI response documentation. They mock network and LLM calls; a successful test run does not verify a live Gemini key or a deployed service.

## Deployment and submission

Deploy the service to a public host, configure `GEMINI_API_KEY` and (optionally) `GEMINI_MODEL` as host environment variables, and verify the live `/`, `/docs`, and `POST /link-analysis` endpoints. Do not commit `.env` or credentials. Capture a real `/docs` screenshot or request/response log after deployment; none is included until a live deployment exists.

Before submitting, make the GitHub repository public and email the live demo URL, `/docs` URL, public repository URL, and the requested applicant/contact details to the recruiter.