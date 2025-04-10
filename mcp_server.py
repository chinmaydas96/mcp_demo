import httpx
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import sqlite3
from mcp.server.fastmcp.prompts import base

mcp = FastMCP(
    "Your MCP tool",
    dependencies=['beautifulsoup4'],
    port=8080,
    sse_path="/sse"    
)

@mcp.tool(
        name="extract_web_content",
        description="Extract text content from a website",
)
def extract_web_content(url: str) -> str | None:
    try:
        response = httpx.get(url,
                             headers={
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                             },
                             timeout=10.0,
                             follow_redirects=True,
                             )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text().replace('\n', ' ').replace('\r', ' ').strip()
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return None
    
@mcp.tool(
    name="bmi_calculator",
    description="Calculate BMI (Body Mass Index) given weight in kilograms and height in meters",
)
def bmi_calculator(weight_kg: float, height_m: float) -> float:
    """Calculate BMI (Body Mass Index) given weight in kilograms and height in meters"""

    if weight_kg <= 0 or height_m <= 0:
        return "Invalid input: weight and height must be positive numbers"
    
    bmi = weight_kg / (height_m ** 2)
    return bmi



@mcp.resource(
    "schema://main",
    description="DDL for ecommerce.db"
)
def get_schema() -> str:
    """Provide the database schema as a resource"""
    conn = sqlite3.connect("ecommerce.db")
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(sql[0] for sql in schema if sql[0])


@mcp.tool(
    name="query_data",
    description="Execute SQL queries safely"
)
def query_data(sql: str) -> str:
    """Execute SQL queries safely"""
    print(sql)
    conn = sqlite3.connect("ecommerce.db")
    try:
        result = conn.execute(sql).fetchall()
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.prompt(
    name="generate_sql",
    description="Generate a single SQL query given a natural‑language question and the ecommerce schema, Only return the SQL query, nothing else."
)
def generate_sql(question: str) -> list[base.Message]:
    schema = get_schema()
    return [
        base.UserMessage(
            f"Given the following database schema:\n\n{schema}\n\n"
            f"Write a single valid SQL query to {question}"
            f"Only return the SQL query, nothing else."
            f"Do not include any other text or comments."
            f"IMPORTANT: When you need to use a tool, you must ONLY respond with"
            f"the exact JSON object format below, nothing else."
            f"Keep the values in str"

            f"{{"
            f"        \"sql\": \"{question}\""
            f"}}"
        )
    ]





        

if __name__ == "__main__":
    #mcp.run(transport="stdio")
    mcp.run(transport="sse")


