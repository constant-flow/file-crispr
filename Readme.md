# File-Crispr

![assets/logo-file-crispr.svg](assets/logo-file-crispr.svg)

Python library to manipulate files the easy way.

## Features

- find a `string` in file and ...

  - ... ✅ return position (`file_find_string_pos`)
  - ... ✅ erase (`file_erase_string`)
  - ... ✅ replace (`file_replace_string`)
  - ... ✅ prepend (`file_prepend_string_to_string`)
  - ... ✅ append (`file_append_string_to_string`)
  - ... ✅ prepend & append (`file_pre_and_append_string_to_string`)

- specify a `line` in file and ...

  - ... ✅ comment it out (`file_comment_line`)
  - ... ✅ comment it in (`file_uncomment_line`)
  - ... ✅ replace it with a string (`file_replace_line`)

- specify a `file` and

  - ... ✅ replace
  - ... ✅ backup
  - ... move
  - ... ✅ copy it (`file_copy`)
  - ... ✅ write/append a string to a file (`file_write_string`)
  - ... ✅ write/append a range of characters to another file (`file_transfer_bytes_n_to_m`)
  - ... ✅ remove it (`file_remove`)
  - ... ✅ get the extension (`file_get_extension`)

- read in `file ` ...

  - ... ✅ a line (`file_read_line`)
  - ... from char(`x`) an amount of `y` characters
