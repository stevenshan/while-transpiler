import os
import sys
import pytest
import stat
import uuid
import subprocess

TEST_PROGRAMS = "test_programs"
TEST_INVALID_PROGRAMS = "test_invalid_programs"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR + '/../')

from whiletranspiler import lexer, parser, utils

test_programs = [x for x in os.listdir(os.path.join(BASE_DIR, TEST_PROGRAMS))
        if x[-7:] != ".answer" and x[-2:] == ".w"]
@pytest.mark.parametrize('source_file', test_programs)
def test_transpiler_correct_programs(source_file, tmp_path):
    """
    Make sure transpiling valid programs gives correct output.
    """

    source_file_path = os.path.join(BASE_DIR, TEST_PROGRAMS, source_file)
    with open(source_file_path, "r") as file_obj:
        token_stream = lexer.get_token_stream(file_obj)
        parse_result = parser.parse(token_stream)

    temp_filename = str(uuid.uuid4())
    temp_file = tmp_path / temp_filename
    temp_file_path = str(temp_file.absolute())
    utils.c_compile(parse_result, temp_file_path)

    st = os.stat(temp_file_path)
    os.chmod(temp_file_path, st.st_mode | stat.S_IEXEC)

    timeout = False
    try:
        output = utils.exec_file(
                temp_file_path, capture_output=True, timeout=3)
    except subprocess.TimeoutExpired:
        timeout = True

    if timeout:
        raise AssertionError("Program timed out.")

    with open(f"{source_file_path}.answer", "r") as answer_file:
        answer = answer_file.read()

    assert output.strip(" \n") == answer.strip(" \n")

test_invalid_programs = [x
        for x in os.listdir(os.path.join(BASE_DIR, TEST_INVALID_PROGRAMS))
        if x[-7:] != ".answer" and x[-2:] == ".w"]
@pytest.mark.parametrize('source_file', test_invalid_programs)
def test_transpiler_invalid_programs(source_file, tmp_path):
    """
    Make sure transpiling invalid programs with syntax error raises ParseError
    """

    source_file_path = os.path.join(
            BASE_DIR, TEST_INVALID_PROGRAMS, source_file)
    with open(source_file_path, "r") as file_obj:
        token_stream = lexer.get_token_stream(file_obj)
        try:
            parse_result = parser.parse(token_stream)
        except parser.ParseError:
            pass
        else:
            raise AssertionError("Expected parse to fail.")

