import httpx

from bs4 import BeautifulSoup

from app.utils.validators import validate_website_url


async def extract_website_content(url: str):

    if not validate_website_url(url):
        raise ValueError("Invalid or unsafe website URL")

    try:

        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=False
        ) as client:

            response = await client.get(
                url,
                headers={
                    "User-Agent": "LinkAnalysisBot/1.0"
                }
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "content-type", ""
            )

            if "text/html" not in content_type.lower():
                raise ValueError("Website must return HTML")

            if len(response.content) > 2_000_000:
                raise ValueError("Website content is too large")

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for tag in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "noscript"
            ]):
                tag.decompose()

            title = (
                soup.title.get_text(strip=True)
                if soup.title else ""
            )

            description_tag = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            description = ""

            if description_tag:
                description = description_tag.get(
                    "content", ""
                )

            headings = [
                heading.get_text(" ", strip=True)
                for heading in soup.find_all(
                    ["h1", "h2", "h3"]
                )
            ]

            paragraphs = [
                paragraph.get_text(" ", strip=True)
                for paragraph in soup.find_all("p")
            ]

            text = " ".join(
                headings + paragraphs
            )

            return {
                "url": url,
                "title": title,
                "description": description,
                "headings": headings[:30],
                "content": text[:12000]
            }

    except httpx.HTTPError as error:
        raise ValueError(
            f"Unable to access website: {error}"
        )