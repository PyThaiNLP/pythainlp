# Why Use Handroll Bytes Slice As "CustomString" Instead of Rust String?

Rust String (and &str) is actually a slice of valid UTF-8 bytes which is variable-length. It has no way of accessing a random index UTF-8 "character" with O(1) time complexity. 

This means any algorithm with operations based on "character" index position will be horribly slow on Rust String.

Hence; "fixed_bytes_str" which is transformed from a slice of valid UTF-8 bytes into a slice of 4-bytes length - padded left with 0.

Consequently, regular expressions must be padded with \x00 for each unicode character to have 4 bytes

Thai characters are 3-bytes length, so every thai char in regex is padded with \x00 one time.

For "space" in regex, it is padded with \x00\x00\x00.


[More on UTF-8](https://en.wikipedia.org/wiki/UTF-8)


*** ALL Vec<u8> or &[u8] operated in tcc_custom, trie_custom and newmm_custom 