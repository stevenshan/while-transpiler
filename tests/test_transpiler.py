import os
import sys
import pytest
import stat
import uuid
import subprocess

TEST_DIR = "test_programs"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR + '/../')

test_programs = [x for x in os.listdir(os.path.join(BASE_DIR, TEST_DIR))
        if x[-7:] != ".answer" and x[-2:] == ".w"]

from whiletranspiler import lexer, parser, utils

@pytest.mark.parametrize('source_file', test_programs)
def test_transpiler(source_file, tmp_path):

    source_file_path = os.path.join(BASE_DIR, TEST_DIR, source_file)
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

