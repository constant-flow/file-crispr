# File-Crispr

Python library to manipulate files the easy way.

## Features

- find `string` in file and ...

  - ... ✅ return position (`file_find_string_pos`)
  - ... ✅ erase (`file_erase_string`)
  - ... ✅ comment out (`file_comment_line`)
  - ... comment in
  - ... ✅ replace (`file_replace_string`)
  - ... ✅ prepend (`file_prepend_string_to_string`)
  - ... ✅ append (`file_append_string_to_string`)
  - ... ✅ prepend & append (`file_pre_and_append_string_to_string`)

- find `file` and

  - ... replace
  - ... backup and replace
  - ... move

- read in `file ` ...

  - ... ✅ a line (`file_read_line`)
  - ... from char(`x`) an amount of `y` characters

- copy

  - ✅ files (`file_copy`)

- write/append
- ✅ a string to a file (`file_write_string`)
- ✅ a range of characters from one file to another (`file_transfer_bytes_n_to_m`)

- ✅ remove a file (`file_remove`)
- ✅ get extension of file (`file_get_extension`)
