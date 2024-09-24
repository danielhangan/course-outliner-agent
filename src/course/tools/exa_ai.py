from crewai_tools import tool
from exa_py import Exa
import os

exa_api_key = os.getenv("EXA_API_KEY")

@tool("Exa search and get contents")
def search_and_get_contents_tool(question: str) -> str:
    """Tool using Exa's Python SDK to run semantic search and return result highlights."""

    exa = Exa(exa_api_key)

    response = exa.search_and_contents(
        question,
        type="neural",
        use_autoprompt=True,
        num_results=3,
        highlights=True
    )

    return ''.join([f'<Title id={idx}>{eachResult.title}</Title><URL id={idx}>{eachResult.url}</URL><Highlight id={idx}>{"".join(eachResult.highlights)}</Highlight>' for (idx, eachResult) in enumerate(response.results)])