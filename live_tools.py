from ddgs import DDGS


def search_live_information(query: str) -> str:

    print("=" * 60)
    print("LIVE SEARCH TOOL CALLED")
    print("Query:", query)
    print("=" * 60)

    try:

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        print(results)

        if not results:
            return "No live information found."

        output = ""

        for i, r in enumerate(results, start=1):

            output += f"""
Result {i}

Title:
{r.get("title")}

URL:
{r.get("href")}

Summary:
{r.get("body")}

----------------------------------------
"""

        return output

    except Exception as e:

        print(e)

        return f"Search failed: {e}"
