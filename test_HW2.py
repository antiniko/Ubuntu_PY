import subprocess
import os
import binascii

tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"


def checkout(cmd, text, cwd=None):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', cwd=cwd)

    print("Command output:")
    print(result.stdout)

    if text in result.stdout and result.returncode == 0:
        return result, result.stdout
    else:
        print("Command failed with error:")
        print(result.stderr)
        return result, result.stderr


def test_step1():
    res1 = checkout(f"cd {tst}; 7z a {out}/arx2", "Everything is Ok")
    res2 = checkout(f"ls {out}", "arx2.7z")
    print("Test Step 1 Result:", "PASS" if res1 and res2 else "FAIL")
    assert res1 and res2, "test1 FAIL"


def test_step2():
    res1 = checkout(f"cd {out}; 7z e arx2.7z -o{folder1} -y", "Everything is Ok")
    res2 = checkout(f"ls {folder1}", "test.txt")
    print("Test Step 2 Result:", "PASS" if res1 and res2 else "FAIL")
    assert res1 and res2, "test2 FAIL"


def test_step3():
    result = checkout(f"cd {out}; 7z t arx2.7z", "Everything is Ok")
    print("Test Step 3 Result:", "PASS" if result else "FAIL")
    assert result, "test3 FAIL"


def test_step4():
    result = checkout(f"cd {out}; 7z d arx2.7z", "Everything is Ok")
    print("Test Step 4 Result:", "PASS" if result else "FAIL")
    assert result, "test4 FAIL"


def test_step5():
    result = checkout(f"cd {out}; 7z u arx2.7z", "Everything is Ok")
    print("Test Step 5 Result:", "PASS" if result else "FAIL")
    assert result, "test5 FAIL"

# HW_part1

def test_list_files_before_compression():
    result = checkout(f"cd {tst}; ls", "test.txt")
    print("Test List Files Before Compression Result:", "PASS" if result else "FAIL")
    assert result, "list_files_before_compression FAIL"


def test_list_files_after_compression():
    result = checkout(f"cd {out}; ls", "arx2.7z")
    print("Test List Files After Compression Result:", "PASS" if result else "FAIL")
    assert result, "list_files_after_compression FAIL"


def test_list_files_in_extracted_folder():
    result = checkout(f"cd {folder1}; ls", "test.txt")
    print("Test List Files in Extracted Folder Result:", "PASS" if result else "FAIL")
    assert result, "list_files_in_extracted_folder FAIL"

def test_list_files_after_extraction():
    extraction_path = os.path.join(out, folder1)
    result = checkout(f"cd {extraction_path}; ls", "test.txt")
    print("Test List Files After Extraction Result:", "PASS" if result else "FAIL")
    assert result, "list_files_after_extraction FAIL"

def test_extract_with_paths():
    result = checkout(f"cd {out}; 7z x arx2.7z -o{folder1} -y", "Everything is Ok")
    res2 = checkout(f"ls {folder1}", "test.txt")
    print("Test Extract with Paths Result:", "PASS" if result and res2 else "FAIL")
    assert result and res2, "extract_with_paths FAIL"

# difficult part


def test_calculate_hash():
    file_path = os.path.join(out, folder1, "test.txt")

    with open(file_path, 'rb') as file:
        content = file.read()
        expected_hash = binascii.crc32(content) & 0xFFFFFFFF

    result, actual_hash = checkout(f"crc32 {file_path}", str(expected_hash))

    if result.stdout is not None:
        actual_hash = result.stdout.strip()
    elif result.stderr is not None:
        actual_hash = result.stderr.strip()
    else:
        actual_hash = None

    print(f"Expected Hash: {expected_hash}, Actual Hash: {actual_hash}")

    print("Test Calculate Hash Result:", "PASS" if result else "FAIL")
    assert result, "calculate_hash FAIL"


# Existing test functions ...

def test_list_files_after_extraction():
    result = checkout(f"cd {out}/{folder1}; ls", "test.txt")
    print("Test List Files After Extraction Result:", "PASS" if result else "FAIL")
    assert result, "list_files_after_extraction FAIL"
