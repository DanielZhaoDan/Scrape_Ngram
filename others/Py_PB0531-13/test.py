from diff import *

diff_1 = DiffCommands('diff_1.txt')
diff_2 = DiffCommands('diff_2.txt')
diff_3 = DiffCommands('diff_3.txt')

pair_of_files_1 = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
pair_of_files_2 = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')
pair_of_files_3 = OriginalNewFiles('file_3_1.txt', 'file_3_2.txt')

pair_of_files_1.is_a_possible_diff(diff_1)
pair_of_files_1.is_a_possible_diff(diff_2)
pair_of_files_1.is_a_possible_diff(diff_3)

pair_of_files_2.is_a_possible_diff(diff_1)
pair_of_files_2.is_a_possible_diff(diff_2)
pair_of_files_2.is_a_possible_diff(diff_3)

pair_of_files_3.is_a_possible_diff(diff_1)
pair_of_files_3.is_a_possible_diff(diff_2)
pair_of_files_3.is_a_possible_diff(diff_3)

pair_of_files_1.output_diff(diff_1)
pair_of_files_2.output_diff(diff_2)
pair_of_files_3.output_diff(diff_3)


pair_of_files_1.output_unmodified_from_original(diff_1)
pair_of_files_1.output_unmodified_from_new(diff_1)
pair_of_files_1.get_all_diff_commands()

pair_of_files_2.output_unmodified_from_original(diff_2)
pair_of_files_2.output_unmodified_from_new(diff_2)
pair_of_files_2.get_all_diff_commands()

pair_of_files_3.output_unmodified_from_original(diff_3)
pair_of_files_3.output_unmodified_from_new(diff_3)
pair_of_files_3.get_all_diff_commands()
