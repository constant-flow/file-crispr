from lib.filecrispr import *

print(file_read_line("lorem.txt", 1))
print(file_read_line("lorem.txt", 4))

file_copy("lorem.txt", "test.txt")

print(file_find_string_pos("test.txt", "lorem"))
print(file_find_string_pos("test.txt", "This is a line to comment out"))

file_transfer_bytes_n_to_m("test.txt", "test2.txt", 2, 4, 0)
file_transfer_bytes_n_to_m("test.txt", "test2.txt", 6, 9)

file_replace_string("test.txt", "This is a line to comment out\nThis",
                    "[multiline replace]")

file_erase_string("test.txt", "comment", 1)
file_copy("lorem.txt", "no-comment.txt")

file_write_string("write-test.txt", "success")
file_prepend_string_to_string("no-comment.txt", "This", "Wahtsasdasd", -1)

file_comment_line("test.txt", 2)
# file_replace_line("test.txt", 2, "˜˜replaced line˜˜")
file_uncomment_line("test.txt", 2)

file_uncomment_line("test.txt", 7, "#")

file_replace("lorem.txt", "tst.txt")

file_backup("lorem.txt")
file_backup("folder/lorem.txt")
