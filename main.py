from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import Field, BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from tools import search_tool, get_word_count
import os

#load env file
load_dotenv()

#Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("YOUR_GROQ_API_KEY")
)

#Give structure to llm
class MovieRecommender(BaseModel):
    movie_names: list[str] = Field(description = "Movie Name")
    genre: str = Field(description = "Movie Genre")
    Industry: list[str] = Field(description="List of Film industries. e.g. ['Hollywood']")
    year_range: list[str] = Field(description="year range in which you want that movie from")
    description: str = Field(description = "Add the outline of the movie")

# All available tools
tools = [search_tool, get_word_count]

#Bind tools with LLM
llm_with_tools = llm.bind_tools(tools)

#System prompt
system_prompt = """
You are a movie recommender.
You will search across the internet the list of movies with reference to the given input by the user.
    """

#messages
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content="Find me a movie from hollywood with thriller genre between 2000 to 2010")
]

#Agent Loop

print("Agent starting...")

while True:

    response = llm_with_tools.invoke(messages)

    messages.append(response)

    if not response.tool_calls:
        print("The agent has the answer, No need of tools..")
        break #exit the loop

    for tool_call in response.tool_calls:
        print(f"Agent using tool: {tool_call['name']}")
        print(f"With input: {tool_call['args']}\n")

    #which tool to run
    if tool_call["name"] == "duckduckgo_search":
        tool_result = search_tool.invoke(tool_call["args"])

    elif tool_call["name"] == "get_word_count":
        tool_result = get_word_count.invoke(tool_call["args"])

    #Append tool result to messages
    messages.append(ToolMessage(
        content = str(tool_result),
        tool_call_id=tool_call["id"]
    ))

#Final instruction
messages.append(HumanMessage(
    content = "Based on your research, provide the final structured response"
))


#Attach structure to the output
structured_llm = llm.with_structured_output(MovieRecommender)
response = structured_llm.invoke(messages)

# Print results
print("---------- SEARCH RESULTS ----------")
print(response.movie_names)
print(response.genre)
print(response.Industry)
print(response.year_range)
print(response.description)
