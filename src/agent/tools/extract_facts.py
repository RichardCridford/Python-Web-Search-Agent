# extract_facts.py

#------------------------------------------------------------------------------------------
# Structured data extraction tool.
# This tool does not perform extraction itself. 
# It packages the unstructured text and the desired JSON schema so the model can perform
# the extraction deterministically in the follow‑up call.

# The model is excellent at filling structured schemas when given both:
# - the raw text
# - the schema describing the desired output
#-------------------------------------------------------------------------------------------


def extract_facts(text: str, schema: str):
    """
    Package text and schema for the model to extract structured facts.

    Parameters
    ----------
    text : str
        The unstructured text to extract information from.
    schema : str
        A JSON schema (as a string) describing the desired output structure.

    Returns
    -------
    dict
        A dictionary containing the text and schema, which the model will
        use to produce structured output in the follow‑up call.
    """
    return {
        "text": text,
        "schema": schema
    }
