#test_summariser 
from agent.dispatcher import dispatch_tool_call

#---------------------------------------------------------------------------------------
# This is a short script to test that the summariser tool is working.  
#
# There's a pathing issue where the test script can't find the agent folder 
# Use the code below to point to the right folder (this is just a quick fix) 
"""env:PYTHONPATH="src"
python tests/test_summariser.py"""
#----------------------------------------------------------------------------------------

result = dispatch_tool_call(
    "summariser",
    {"text": "The sky is blue because of Rayleigh scattering.", "max_points": 3}
)

# Gives each section of the summary a bullet point (just a quick fix in this test script).
for point in result["summary"]:
    print("-", point)


# Later create a reusable helper to get all the tools to have a more readable output.


