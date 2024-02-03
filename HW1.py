import subprocess
import string

def check_text(comand, text):
    result = subprocess.run(comand, shell=True, stdout=subprocess.PIPE, encoding="utf-8")

    if result.returncode == 0 and text in result.stdout:
        return True
    else:
        return False
if check_text("cat /etc/os-release", 'PRETTY_NAME="Ubuntu 22.04.1 LTS"'):
    print("SUCCESS")
else:
    print("FAIL")

# check 2 texts
def both_texts(comand, text1, text2):
    result = subprocess.run(comand, shell=True, stdout=subprocess.PIPE, encoding="utf-8")

    if result.returncode == 0 and text1 in result.stdout and text2 in result.stdout:
        return True
    else:
        return False
command_to_run = "cat /etc/os-release"
text1_to_find = 'PRETTY_NAME="Ubuntu 22.04.1 LTS"'
text2_to_find = 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'
if both_texts(command_to_run, text1_to_find, text2_to_find):
    print("SUCCESS")
else:
    print("FAIL")

# difficult HW
def difficult(command, text, split_by_words=False):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")

    if result.returncode == 0:
        output = result.stdout
        if split_by_words:
            words = [''.join(char for char in word if char not in string.punctuation) for word in output.split()]
            if text in words:
                return True
        else:
            if text in output:
                return True

        return False

text_to_find_word = 'Jammy'
if difficult(command_to_run, text_to_find_word, split_by_words=True):
    print("SUCCESS (Word found)")
else:
    print("FAIL (Word not found)")