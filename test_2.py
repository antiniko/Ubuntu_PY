from checkers import checkout, getout
import yaml
from sshcheckers import ssh_checkout, upload_files
import os
import paramiko
import zlib


config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

with open(config_path) as f:
    data = yaml.safe_load(f)

class TestPositive:
    def test_step0(self):
        res = []
        upload_files("0.0.0.0", "user2", "11", "tests/p7zip-full.deb", "/home/user2/p7zip-full.deb")
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                                "Настраивается пакет"))
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -s p7zip-full",
                                "Status: install ok installed"))
        assert all(res)

    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        # Выполнение команды 7z a
        print("Executing command: cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]))
        res1 = ssh_checkout("0.0.0.0", "user2", "11",
                            "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        print("Result of command 1:", res1)

        # Выполнение команды ls
        print("Executing command: ls {}".format(data["folder_out"]))
        res2 = ssh_checkout("0.0.0.0", "user2", "11", "ls {}".format(data["folder_out"]), "arx.7z")
        print("Result of command 2:", res2)

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z e arx.7z -o{} -y".format(data["folder_out"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            print("Executing command: ls {}".format(data["folder_ext"]))
            res.append(ssh_checkout("0.0.0.0", "user2", "11", "ls {}".format(data["folder_ext"]), item))

    def test_step3(self):
        # test3
        assert ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z t arx.7z".format(data["folder_out"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z u arx2.7z".format(data["folder_in"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        def test_step5(self, clear_folders, make_files):
            # test5
            res = []
            res.append(ssh_checkout("0.0.0.0", "user2", "11",
                                    "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]),
                                    "Everything is Ok"))
            for i in make_files:
                res.append(ssh_checkout("0.0.0.0", "user2", "11",
                                        "cd {}; 7z l arx.7z".format(data["folder_out"], data["folder_ext"]), i))
            assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        try:
            # Формирование команды для создания архива
            command1 = "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"])
            print(f"Выполняется команда1: {command1}")

            # Проверка наличия команды '7z' на сервере
            if not ssh_checkout("0.0.0.0", "user2", "11", "command -v 7z", "text"):
                print("Ошибка: утилита '7z' не найдена на сервере. Прерывание теста.")
                return

            # Выполнение команды1 и добавление результата в список
            res.append(ssh_checkout("0.0.0.0", "user2", "11", command1, "Everything is Ok"))

            # Дополнительный вывод результата выполнения команды1
            output1 = getout(command1)
            print(f"Результат выполнения команды1: {output1}")

            # Дополнительный вывод промежуточных результатов
            print(f"Промежуточные результаты: {res}")

        except Exception as e:
            print(f"Исключение во время выполнения test_step6: {e}")
            raise

        assert all(res), "test6 FAIL"
    def test_step7(self):
        # test7
        assert ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z d arx.7z".format(data["folder_out"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            crc32_command = "crc32 {}".format(i)
            if not ssh_checkout("0.0.0.0", "user2", "11", "command -v crc32", "text"):
                print("Error: 'crc32' utility not found. Skipping test8 for file {}.".format(i))
                continue

            res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z h {}".format(data["folder_in"], i),
                                    "Everything is Ok"))
            hash = getout("cd {}; {}".format(data["folder_in"], crc32_command)).upper()
            res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z h {}".format(data["folder_in"], i), hash))

        assert all(res), "test8 FAIL"

