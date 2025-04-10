from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


from mcp.client.sse import sse_client

import os
import json
import asyncio

os.environ["OPENAI_API_KEY"] = ""

client = OpenAI()

# server_params = StdioServerParameters(command="python", args=["mcp_server_demo.py"])
server_url = "http://localhost:8080/sse" 


def llm_client(prompt: str) -> str:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt,
        
        # [
        #     {"role": "system", "content": "You are a helpful assistant.  You will extract task from a user's request."},
        #     {"role": "user", "content": prompt}
        # ],
       max_tokens=250,
       temperature=0.2,
    )
    return response.choices[0].message.content

def get_prompt_tool(query, tools):
    tool_description = "\n".join([f"{tool.name}: {tool.description}, {tool.inputSchema}" for tool in tools])
    return f"""
    You are a helpful assistant.  With Access to the following tools:\n\n
    {tool_description}

    choose appropriate tool based on the user's request.
    
    Here is the user's request:
    {query}

    If no tool is needed reply directly. 

    IMPORTANT: When you need to use a tool, you must ONLY respond with
    the exact JSON object format below, nothing else.
    Keep the values in str

    {{
        "tool": "tool-name",
        "arguments": {{
            "argument-name": "value"
        }}
    }}
    Please use the tools to extract the task from the user's request.
    """

async def run(query: str):
    #async with stdio_client(server_params) as (read, write):
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            prompts_response = await session.list_prompts()
           

            # 1) Generate the SQL via our prompt
            prompt_resp = await session.get_prompt(
                name="generate_sql",
                arguments={"question": query}
            )
            
            messages = [
                {"role": m.role, "content": m.content.text}
                for m in prompt_resp.messages
            ]

            # 2) Send it to OpenAI directly
            sql = llm_client(messages)
            print("🔍 Generated SQL:\n", sql)

            sql = json.loads(sql)

            # 3) Execute it against the database
            exec_resp = await session.call_tool("query_data", {"sql": sql['sql']})
            print("📊 Query Result:\n", exec_resp.content[0].text)

            # # 2) Execute the SQL
            # exec_resp = await session.call_tool(
            #     "query_data",
            #     {"sql": sql}
            # )
            # print("📊 Query Result:\n", exec_resp.content[0].text)


            # resources_response = await session.list_resources()
            # for res in resources_response.resources:
            #     print(f"URI: {res.uri} — {res.name} ({res.description})")

            
            # schema_response = await session.read_resource(uri="schema://main")
            # schema_text = schema_response.contents[0].text
            # print("Database schema:\n", schema_text)            
            # tools = await session.list_tools()
            # print(tools)
            # prompt = get_prompt_tool(query, tools.tools)
            # llm_response = llm_client(prompt)

            # print(llm_response) 
            # tool_call = json.loads(llm_response)

            # result = await session.call_tool(tool_call["tool"], arguments=tool_call["arguments"])
            # print(result.content[0].text)


if __name__ == "__main__":
    # query = "Calculate BMI for a person who is 1.70m tall and weighs 70kg"
    question = "Give me the date of Completed orders"
    asyncio.run(run(question))
    
    
