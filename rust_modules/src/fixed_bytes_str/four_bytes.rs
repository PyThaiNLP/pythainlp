use bytecount::num_chars;
pub const BYTES_PER_CHAR: usize = 4;
const VALID_ONE_BYTE_UTF8_FIRST_BYTE_MAX_VALUE: u8 = 0b01111111 as u8;

const VALID_TWO_BYTE_UTF8_FIRST_BYTE_RANGE: (u8, u8) = (0b11000000 as u8, 0b11011111 as u8);
const VALID_TWO_BYTE_UTF8_SECOND_BYTE_RANGE: (u8, u8) = (0b10000000 as u8, 0b10111111 as u8);

const VALID_THREE_BYTE_UTF8_FIRST_BYTE_RANGE: (u8, u8) = (0b11100000 as u8, 0b11110111 as u8);
const VALID_THREE_BYTE_UTF8_SECOND_BYTE_RANGE: (u8, u8) = (0b10000000 as u8, 0b10111111 as u8);
const VALID_THREE_BYTE_UTF8_THIRD_BYTE_RANGE: (u8, u8) = (0b10000000 as u8, 0b10111111 as u8);

const VALID_FOUR_BYTE_UTF8_FIRST_BYTE_RANGE: (u8, u8) = (0b11110000 as u8, 0b11110111 as u8);
const VALID_FOUR_BYTE_UTF8_SECOND_BYTE_RANGE: (u8, u8) = (0b10000000 as u8, 0b10111111 as u8);
const VALID_FOUR_BYTE_UTF8_THIRD_BYTE_RANGE: (u8, u8) = (0b10000000 as u8, 0b10111111 as u8);
const VALID_FOUR_BYTE_UTF8_FOURTH_BYTE_RANGE: (u8, u8) = (0b10000000 as u8, 0b10111111 as u8);
const SPACE_BYTE :&[u8] = &[0,0,0,32];
use lazy_static::__Deref;
use smol_str::SmolStr;
use std::{borrow::Borrow, str::from_utf8_unchecked};
fn is_in_range<T: PartialEq + PartialOrd>(value: T, range: (T, T)) -> bool {
    value >= range.0 && value <= range.1
}
/** returns bytes index */
pub fn rfind_space(custom_text:&[u8])->Option<usize>{
    assert_eq!(custom_text.len()%4,0);

    for index in (0..(custom_text.len()/BYTES_PER_CHAR)).rev() {
        match &custom_text[(index)*BYTES_PER_CHAR..(index+1)*BYTES_PER_CHAR] {
            SPACE_BYTE=>{
               return Some((index)*BYTES_PER_CHAR);
            },
            _=>{} 
        }
    }
    None
}
/**
 bytes length = 32, char len = 8
 index 0..8 reverse
 7..=0
 28 ..

*/
fn is_whitespace(custom_bytes:&[u8]) -> bool{
    match custom_bytes {
        | [0,0,0,9]
        | [0,0,0,10]
        | [0,0,0,11]
        | [0,0,0,12]
        | [0,0,0,13]
        | [0,0,0,32]
        | [0,0,194,133]
        | [0,0xe2,0x80,0x8e]
        | [0,0xe2,0x80,0x8f]
        | [0,0xe2,0x80,0xa8]
        | [0,0xe2,0x80,0xa9] => true,
        _=>false
    }
   
}
pub fn to_four_bytes(input: &str) -> Vec<u8> {
    let output_size = num_chars(input.as_bytes());
    let mut output_vec: Vec<u8> = Vec::with_capacity(output_size*4);
    // let mut output:&[u8;4] = &[0;output_size];
    for character in input.chars() {
        let mut bytes_buffer: [u8; 4] = [0; 4];

        character.encode_utf8(&mut bytes_buffer);
        // not leading zero yet
        let arranged_buffer = match bytes_buffer {
            [a, 0, 0, 0] => [0,0,0,a],
            [a, b, 0, 0] => [0, 0, a, b],
            [a, b, c, 0] => [0, a, b, c],
            _ => bytes_buffer,
        };
        // let vec_of_bytes = Vec::with_capacity(4);

        output_vec.extend_from_slice(&arranged_buffer);
    }
    output_vec.shrink_to_fit();
    output_vec
}
pub fn encode_utf8(input: &[u8]) -> SmolStr {
    assert_eq!(input.len(), 4);
    match input {
        [ 0, 0, 0,one_byte_char] if one_byte_char <= &VALID_ONE_BYTE_UTF8_FIRST_BYTE_MAX_VALUE => {
            SmolStr::new(unsafe { from_utf8_unchecked(&[*one_byte_char]) })
        }
        [0, 0,first_byte, second_byte ]
            if is_in_range(*first_byte, VALID_TWO_BYTE_UTF8_FIRST_BYTE_RANGE)
                && is_in_range(*second_byte, VALID_TWO_BYTE_UTF8_SECOND_BYTE_RANGE) =>
        {
            SmolStr::new(unsafe { from_utf8_unchecked(&[*first_byte, *second_byte]) })
        }
        [0,first_byte, second_byte, third_byte]
            if is_in_range(*first_byte, VALID_THREE_BYTE_UTF8_FIRST_BYTE_RANGE)
                && is_in_range(*second_byte, VALID_THREE_BYTE_UTF8_SECOND_BYTE_RANGE)
                && is_in_range(*third_byte, VALID_THREE_BYTE_UTF8_THIRD_BYTE_RANGE) =>
        {
            SmolStr::new(unsafe { from_utf8_unchecked(&[*first_byte, *second_byte, *third_byte]) })
        }
        [first_byte, second_byte, third_byte, fourth_byte]
            if is_in_range(*first_byte, VALID_FOUR_BYTE_UTF8_FIRST_BYTE_RANGE)
                && is_in_range(*second_byte, VALID_FOUR_BYTE_UTF8_SECOND_BYTE_RANGE)
                && is_in_range(*third_byte, VALID_FOUR_BYTE_UTF8_THIRD_BYTE_RANGE)
                && is_in_range(*fourth_byte, VALID_FOUR_BYTE_UTF8_FOURTH_BYTE_RANGE) =>
        {
            SmolStr::new(unsafe { from_utf8_unchecked(input) })
        }
        _ => {
            panic!("not in 4 bytes range")
        }
    }
}
pub fn trim_to_std_utf8(input: &[u8]) -> Box<[u8]> {
    assert_eq!(input.len(), 4);
    match input {
        [ 0, 0, 0,one_byte_char] if one_byte_char <= &VALID_ONE_BYTE_UTF8_FIRST_BYTE_MAX_VALUE => {
            Box::from([*one_byte_char])
        }
        [0, 0,first_byte, second_byte ]
            if is_in_range(*first_byte, VALID_TWO_BYTE_UTF8_FIRST_BYTE_RANGE)
                && is_in_range(*second_byte, VALID_TWO_BYTE_UTF8_SECOND_BYTE_RANGE) =>
        {
            Box::from([*first_byte, *second_byte])
        }
        [0,first_byte, second_byte, third_byte]
            if is_in_range(*first_byte, VALID_THREE_BYTE_UTF8_FIRST_BYTE_RANGE)
                && is_in_range(*second_byte, VALID_THREE_BYTE_UTF8_SECOND_BYTE_RANGE)
                && is_in_range(*third_byte, VALID_THREE_BYTE_UTF8_THIRD_BYTE_RANGE) =>
        {
            Box::from([*first_byte, *second_byte, *third_byte])
        }
        [first_byte, second_byte, third_byte, fourth_byte]
            if is_in_range(*first_byte, VALID_FOUR_BYTE_UTF8_FIRST_BYTE_RANGE)
                && is_in_range(*second_byte, VALID_FOUR_BYTE_UTF8_SECOND_BYTE_RANGE)
                && is_in_range(*third_byte, VALID_FOUR_BYTE_UTF8_THIRD_BYTE_RANGE)
                && is_in_range(*fourth_byte, VALID_FOUR_BYTE_UTF8_FOURTH_BYTE_RANGE) =>
        {
            Box::from(input)
        }
        _ => {
            panic!("not in 4 bytes range")
        }
    }
}
pub fn to_std_string(input:&[u8])->String {
    assert_eq!(input.len()%4, 0);
    let mut output_content:Vec<u8> = Vec::with_capacity(input.len());
    for index in (0..input.len()).step_by(BYTES_PER_CHAR){
        let end_offset = index+BYTES_PER_CHAR;
        for byte in trim_to_std_utf8(&input[index..end_offset]).deref(){

            output_content.push(*byte);
        }
    }
    let mut output = String::from(std::str::from_utf8(output_content.as_slice()).unwrap());
    output.shrink_to_fit();
    output
}
/** The content inside this string is a vector of bytes - ALWAYS with length %4 == 0

    Every character is a valid utf-8 encoded byte padded left with 0 to make every character takes 4 bytes space.

    For example, Thai characters which use 3 bytes are represented by [0,valid_first_byte,valid_second_byte,valid_third_byte].
    
    ***Comparison***
    String "กข " is represented by \[224, 184, 129, 224, 184, 130, 32\].

    CustomString "กข " is represented by \[0, 224, 184, 129, 0, 224, 184, 130, 0, 0, 0, 32\].
*/
#[derive(Clone)]
pub struct CustomString {
    content: Box<[u8]>,
    length: usize,
    
}

impl CustomString{
    pub fn from(slice:&[u8]) -> Self {
        Self{
            content:Box::from(slice),
            length:slice.len() / BYTES_PER_CHAR
        }
    }
    pub fn new(base_string:&str)->Self{
        let content:Box<[u8]> = Box::from(to_four_bytes(base_string));
        let length = content.len() / BYTES_PER_CHAR;
        Self{
            content,
            length
            
        }
    }
    pub fn raw_content(&self)->&[u8]{
        self.content.borrow()
    }
    /** Returns characters length */
    pub fn chars_len(&self)->usize {
        self.length
    }
    /** */
    pub fn len(&self)->usize {
        self.content.len()
    }
    pub fn trim(&self) -> Self {
        let mut new_content:&[u8] = &self.content;
        while is_whitespace(&new_content[0..BYTES_PER_CHAR]){
            // trim left
           new_content =  &new_content[BYTES_PER_CHAR..];
        }
       
        while is_whitespace(&new_content[(new_content.len()-BYTES_PER_CHAR)..]){
            // trim left
            new_content = &new_content[..(new_content.len()-BYTES_PER_CHAR)];
            // new_content.drain((self.content.len()-BYTES_PER_CHAR)..(self.content.len()));
        }
        let length = new_content.len() / BYTES_PER_CHAR;

        Self{
            content:Box::from(new_content),
            length
        }
    }
  
    /** modify this string to only have character from index retain_start to retain_end */
  
    /** modify this string - cut out characters by n characters from front */
 
    /** start and end parameter are character index */
    pub fn to_std_string(&self)->String {
        to_std_string(&self.content)
    }
    pub fn convert_raw_bytes_to_std_string(input:&[u8])->String {
        let mut output_content:Vec<u8> = Vec::with_capacity(input.len());
        for index in (0..input.len()).step_by(BYTES_PER_CHAR){
            let end_offset = index+BYTES_PER_CHAR;
            for byte in trim_to_std_utf8(&input[index..end_offset]).deref(){

                output_content.push(*byte);
            }
        }
        let mut output = String::from(std::str::from_utf8(output_content.as_slice()).unwrap());
        output.shrink_to_fit();
        output
    }
}
// impl PartialEq for CustomString {