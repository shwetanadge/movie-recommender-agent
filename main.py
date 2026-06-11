from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import Field, BaseModel
from langchain_core.messages import SystemMessage, HumanMessage
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
    Industry: list[str] = Field(description="Specify which industry does the movie comes from?")
    year_range: list[str] = Field(description="year range in which you want that movie from")

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

