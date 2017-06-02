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
        :return: True if commands can be the diff else False
        '''

        return False


class DiffCommandsError(Exception):
    pass

class OriginalNewFiles:
    pass
