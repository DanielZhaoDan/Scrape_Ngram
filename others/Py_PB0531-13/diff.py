import re

a_c_reg = '(\d+),*(\d*)[ac](\d+),*(\d*)'
d_reg = '(\d+),*(\d*)[d](\d+)$'


class DiffCommands:
    '''
    DiffCommand class builds a DiffCommands object to store diff commands from a text file
    '''
    def __init__(self, filename):
        '''
        load commands from filename and check if this command file can be the diff of two files
        :param filename: text filename
        :return:
        '''
        self.filename = filename
        self.commands_list = []
        self.default_exception_msg = 'Cannot possibly be the commands for the diff of two files'

        try:
            with open(filename) as f:
                self.commands_list = [command.strip() for command in f.readlines()]
        except IOError as e:
            raise DiffCommandsError(e)

        self.is_valid = self.__is_valid_diff_file()
        if not self.is_valid:
            raise DiffCommandsError(self.default_exception_msg)

    def __str__(self):
        if self.__is_valid_diff_file():
            return '\n'.join(self.commands_list)
        else:
            raise DiffCommandsError(self.default_exception_msg)

    def __is_valid_diff_file(self):
        '''
        private method to verify if commands can be the diff of two files
        1. one blank line in end of file is regard as valid because there is one blank line in diff_1,
           diff_2 and diff_3 file
        2. two or more blank lines in end of file is invalid (for example wrong_3.txt)
        3. any space is invalid (for example wrong_2.txt)
        4. there should be only one number in right of 'd' command (for example wrong_4 is invalid)
        5. for d command 'n1,n2dn3' and next line 'n4an5' or 'n4cn5' the n5-n3 should > n4-n2, that is why wrong_7 is invalid
        6, for d command 'n1,n2dn3' is invalid if n2-n1 = n3. This command should be 'n1,n2cn1,n3' (for exmaple wrong_5)
        5. for d command 'n1,n2dn3' and next line 'n4an5' or 'n4cn5' the n5 != n3, because the two file is synced in next line of n3
           that is why wrong_6 is invalid
        :return: True if commands can be the diff else False
        '''
        last_left_file_line = -1
        last_right_file_line = -1
        last_command_is_d = False

        for command in self.commands_list:
            line_numbers = re.compile(a_c_reg).findall(command)
            if line_numbers:
                # this command is add or change command
                line_number = line_numbers[0]
                # judge if the line number is larger than previous line number
                if last_command_is_d:
                    if int(line_number[2]) == last_right_file_line + 1:
                        return False
                    last_command_is_d = False
                    left_line_delta = int(line_number[0]) - last_left_file_line
                    right_line_delta = int(line_number[2]) - last_right_file_line
                    if right_line_delta < left_line_delta:
                        return False
                if line_number[1] == '':
                    if int(line_number[0]) <= last_left_file_line:
                        return False
                    last_left_file_line = int(line_number[0])
                else:
                    if int(line_number[1]) <= last_left_file_line:
                        return False
                    last_left_file_line = int(line_number[1])
                if line_number[3] == '':
                    if int(line_number[2]) <= last_right_file_line:
                        return False
                    last_right_file_line = int(line_number[2])
                else:
                    if int(line_number[3]) <= last_right_file_line:
                        return False
                    last_right_file_line = int(line_number[3])
            else:
                line_numbers = re.compile(d_reg).findall(command)
                if not line_numbers or last_command_is_d:
                    # not add, change and delete command, return false(invalid)
                    return False
                else:
                    last_command_is_d = True
                    line_number = line_numbers[0]
                    if line_number[1] == '':
                        if int(line_number[0]) <= last_left_file_line:
                            return False
                        last_left_file_line = int(line_number[0])
                    else:
                        if int(line_number[1]) <= last_left_file_line:
                            return False
                        if int(line_number[1]) - int(line_number[0]) == int(line_number[2]):
                            return False
                        last_left_file_line = int(line_number[1])
                    if int(line_number[2]) <= last_right_file_line:
                        return False
                    last_right_file_line = int(line_number[2])

        return True


class DiffCommandsError(Exception):
    pass


class OriginalNewFiles:
    '''
    OriginalNewFiles class provides a user interface with 4 methods:
    is_a_possible_diff()
    output_diff()
    output_unmodified_from_original()
    output_unmodified_from_new()
    get_all_diff_commands()
    '''
    def __init__(self, filename1, filename2):
        try:
            with open(filename1) as f1:
                self.text_1 = [command.strip() for command in f1.readlines()]
            with open(filename2) as f2:
                self.text_2 = [command.strip() for command in f2.readlines()]
        except IOError as e:
            raise DiffCommandsError(e)

    def is_a_possible_diff(self, diff_commands_obj):
        if not diff_commands_obj.is_valid:
            print False
        try:
            origin_1 = list(filter(lambda x: x != '...', self.do_unmodified_from_original(diff_commands_obj)))
            origin_2 = list(filter(lambda x: x != '...', self.do_unmodified_from_new(diff_commands_obj)))
            if len(origin_1) != len(origin_2):
                print False

            for i in range(len(origin_2)):
                if origin_1[i] != origin_2[i]:
                    print False
            print True
        except IndexError as e:
            print False


    def output_diff(self, diff_commands_obj):
        for line in diff_commands_obj.commands_list:
            print line
            if 'a' in line:
                numbers = re.compile(a_c_reg).findall(line)[0]
                if numbers[3] != '':
                    for i in range(int(numbers[2])-1, int(numbers[3])):
                        print '> ' + self.text_2[i]
                else:
                    print '> ' + self.text_2[int(numbers[2])-1]
            elif 'd' in line:
                numbers = re.compile(d_reg).findall(line)[0]
                if numbers[1] != '':
                    for i in range(int(numbers[0])-1, int(numbers[1])):
                        print '< ' + self.text_1[i]
                else:
                    print '< ' + self.text_1[int(numbers[0])-1]
            else:
                numbers = re.compile(a_c_reg).findall(line)[0]
                if numbers[1] != '':
                    for i in range(int(numbers[0])-1, int(numbers[1])):
                        print '< ' + self.text_1[i]
                else:
                    print '< ' + self.text_1[int(numbers[0])-1]
                print '---'
                if numbers[3] != '':
                    for i in range(int(numbers[2])-1, int(numbers[3])):
                        print '> ' + self.text_2[i]
                else:
                    print '> ' + self.text_2[int(numbers[2])-1]

    def do_unmodified_from_original(self, diff_command_obj):
        origin_file = []
        last_line = 0
        for line in diff_command_obj.commands_list:
            if 'd' in line:
                numbers = re.compile(d_reg).findall(line)[0]
                if last_line != 0:
                    for i in range(last_line, int(numbers[0])-1):
                        origin_file.append(self.text_1[i])
                else:
                    for i in range(0, int(numbers[0])-1):
                        origin_file.append(self.text_1[i])
                origin_file.append('...')
                if numbers[1] != '':
                    last_line = int(numbers[1])
                else:
                    last_line = int(numbers[0])
            elif 'c' in line:
                numbers = re.compile(a_c_reg).findall(line)[0]
                if last_line != 0:
                    for i in range(last_line, int(numbers[0])-1):
                        origin_file.append(self.text_1[i])
                else:
                    for i in range(0, int(numbers[0])-1):
                        origin_file.append(self.text_1[i])
                origin_file.append('...')
                if numbers[1] != '':
                    last_line = int(numbers[1])
                else:
                    last_line = int(numbers[0])
        for i in range(last_line, len(self.text_1)):
            origin_file.append(self.text_1[i])
        return origin_file

    def do_unmodified_from_new(self, diff_commands_obj):
        last_line = 0
        origin_file = []
        for line in diff_commands_obj.commands_list:
            if 'a' in line or 'c' in line:
                numbers = re.compile(a_c_reg).findall(line)[0]
                if last_line != -1:
                    for i in range(last_line, int(numbers[2])-1):
                        origin_file.append(self.text_2[i])
                else:
                    for i in range(0, int(numbers[2])-1):
                        origin_file.append(self.text_2[i])

                origin_file.append('...')
                if numbers[3] != '':
                    last_line = int(numbers[3])
                else:
                    last_line = int(numbers[2])
        for i in range(last_line, len(self.text_2)):
            origin_file.append(self.text_2[i])
        return origin_file

    def output_unmodified_from_original(self, diff_command_obj):
        origin_file = self.do_unmodified_from_original(diff_command_obj)
        for line in origin_file:
            print line

    def output_unmodified_from_new(self, diff_command_obj):
        origin_file = self.do_unmodified_from_new(diff_command_obj)
        for line in origin_file:
            print line


diff_1 = DiffCommands('diff_1.txt')
diff_2 = DiffCommands('diff_2.txt')
diff_3 = DiffCommands('diff_3.txt')

pair_of_files = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')

pair_of_files.is_a_possible_diff(diff_1)
