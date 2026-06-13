from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from datetime import datetime

#This is the search tool
search_tool = DuckDuckGoSearchRun()

#custom tool to get the word count
@tool
def get_word_count(text: str) -> int:
    """
    Counts the number of words present in the given text.
    Use this when you need to know how long a piece of text is.
    """
    return len(text.split())