import re

from random import randint
from brutils.assets import legal_process_ids
from datetime import datetime

# FORMATTING
############


def sieve(dirty):  # type: (str) -> list
    """
    Filters out CPF formatting symbols.

    Symbols that are not used in the Legal Process ID number formatting are left
    unfiltered on purpose so that if fails other tests,
    because their presence indicate that the input was somehow corrupted.
    """

    return re.findall(r"[^\w\s\-.]", dirty)


def remove_symbols(dirty):  # type: (str) -> str
    """Alias to the function `sieve`. Better naming."""
    return sieve(dirty)


def display(legal_process_id):
    """
    Format an adequately formatted numbers-only Legal Process ID number string,
    adding in standard formatting visual aid symbols for display.
    """

    if (
        not legal_process_id.isdigit()
        or len(legal_process_id) != 11
        or len(set(legal_process_id)) == 1
    ):
        return None
    return format_processo_juridico(legal_process_id)


def format_processo_juridico(legal_process_id):  # type: (int) -> (str)
    """
    Format an adequately formatted numbers-only Legal Process ID number,
    Returns a cpf formatted with standard visual aid symbols.
    Returns None if cpf is invalid.
    """
    if is_valid(legal_process_id):
        capture_fields = r"(\d{7})(\d{2})(\d{4})(\d)(\d{2})(\d{4})"
        include_chars = r"\1-\2.\3.\4.\5.\6"
        return re.sub(capture_fields, include_chars, legal_process_id)
    return None


# OPERATIONS
############


def validate(legal_process_id):  # type: (str) -> bool
    """
    Returns whether or not the verifying checksum digits of the given Legal
    Process ID number match it's varification digit.
    """
    match_dd_pattern = r"-(.*?)\."
    match = re.search(match_dd_pattern, legal_process_id)
    DD = match.group(1)
    clean_legal_process_id = int(
        re.sub(
            r"[^\w\s]", "", re.sub(match_dd_pattern, "", legal_process_id, 1)
        )
    )
    return _checksum(clean_legal_process_id) == DD


def is_valid(legal_process_id):  # type: (str) -> bool
    """
    Evaluates if the Legal Process ID number is String and calls validate.
    """
    return isinstance(legal_process_id, str) and validate(legal_process_id)


def generate():  # type: () -> str
    """
    Generates a random valid number of a Legal Process ID number.
    """
    J = randint(4, 9)
    _ = legal_process_ids[f"orgao_{J}"]
    TR = str(_["id_tribunal"][randint(0, (len(_["id_tribunal"]) - 1))]).zfill(2)
    OOOO = str(_["id_foro"][randint(0, (len(_["id_foro"])) - 1)]).zfill(4)
    AAAA = _generate_random_year()
    NNNNNNN = randint(0, 9999999)
    DD = _checksum(f"{NNNNNNN}{AAAA}{J}{TR}{OOOO}")
    return f"{NNNNNNN}{DD}{AAAA}{J}{TR}{OOOO}"


def _generate_random_year():  # type: () -> int
    """
    Generates a random year as YYYY format from 1970 until the present year.
    """
    current_year = datetime.now().year
    return randint(1970, current_year)


def _checksum(basenum):  # type: (int) -> str
    """
    Will compute the checksum of the verification digit for a given Legal Process ID number.
    `basenum` needs to be a digit without the verification id.
    """
    return str(97 - ((basenum * 100) % 97)).zfill(2)
