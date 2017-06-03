import re

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
                self.commands_list = f.readlines()
        except IOError as e:
            raise DiffCommandsError(e)
        if not self.__is_valid_diff_file():
            raise DiffCommandsError(self.default_exception_msg)

    def __str__(self):
        if self.__is_valid_diff_file():
            print '\n'.join(self.commands_list)
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
        a_c_reg = '(\d+),*(\d*)[ac](\d+),*(\d*)'
        d_reg = '(\d+),*(\d*)[d](\d+)$'
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
    pass
