# app/validators/sql_validator.py

import re
import json
from typing import Dict
from app.utils.error import InvalidSQLGenerated


ALLOWED_ACTIONS = {"read", "write"}

FORBIDDEN_KEYWORDS = {
    "DROP",
    "DELETE",
    "ALTER",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
}


# -------------------------
# Parsing Layer
# -------------------------

def parse_model_output(raw_output: str) -> Dict:
    """
    Extracts and parses JSON from raw model output.
    Handles markdown-wrapped or extra-text responses.
    """

    if isinstance(raw_output, dict):
        return raw_output

    if not isinstance(raw_output, str):
        raise InvalidSQLGenerated("Model output must be a string or dict")

    try:
        # Try direct JSON parse first
        return json.loads(raw_output)
    except json.JSONDecodeError:
        # Fallback: extract JSON block
        match = re.search(r"\{.*?\}", raw_output, re.DOTALL)
        if not match:
            raise InvalidSQLGenerated("No valid JSON object found in model output")

        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            raise InvalidSQLGenerated("Extracted JSON is invalid")


# -------------------------
# Structure Validation
# -------------------------

def validate_structure(data: Dict) -> None:
    """
    Validates JSON structure and required fields.
    """

    if not isinstance(data, dict):
        raise InvalidSQLGenerated("Model output must be a JSON object")

    required_fields = {"action", "query"}
    missing = required_fields - data.keys()

    if missing:
        raise InvalidSQLGenerated(f"Missing required fields: {missing}")

    if data["action"] not in ALLOWED_ACTIONS:
        raise InvalidSQLGenerated(f"Invalid action type: {data['action']}")

    if not isinstance(data["query"], str):
        raise InvalidSQLGenerated("Query must be a string")


# -------------------------
# SQL Logic Validation
# -------------------------

def validate_sql_logic(data: Dict) -> None:
    """
    Validates SQL safety and constraints.
    """

    action = data["action"]
    query = data["query"].strip()

    if not query:
        raise InvalidSQLGenerated("SQL query is empty")

    # Must end with semicolon
    if not query.endswith(";"):
        raise InvalidSQLGenerated("SQL query must end with a semicolon")

    upper_query = query.upper()

    # Enforce SELECT for read
    if action == "read" and not upper_query.startswith("SELECT"):
        raise InvalidSQLGenerated("Read action must use SELECT statement")

    # Block forbidden keywords
    for word in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{word}\b", upper_query):
            raise InvalidSQLGenerated(f"Forbidden keyword detected: {word}")


# -------------------------
# Main Entry
# -------------------------

def validate_model_output(raw_output) -> Dict:
    """
    Full validation pipeline.
    Returns parsed and validated JSON.
    Raises InvalidSQLGenerated on failure.
    """

    parsed = parse_model_output(raw_output)

    validate_structure(parsed)
    validate_sql_logic(parsed)

    return parsed