use std::{ fs::{File, canonicalize}, path::PathBuf};
use crate::fixed_bytes_str::four_bytes::CustomString;

use std::io::prelude::*;
use std::io::BufReader;
use super::trie_custom::Trie;
const CARGO_PATH:&str = env!("CARGO_MANIFEST_DIR");
const DEFAULT_DICT_PATH_RELATIVE_CARGO:&str = "pythainlp/corpus/words_th.txt"; 
pub enum DictSource {
    WordList(Vec<String>),
    FilePath(PathBuf)
}

pub fn create_default_dict() -> Trie {


    let dict_path = PathBuf::from(DEFAULT_DICT_PATH_RELATIVE_CARGO);
    let cargo_path = PathBuf::from(CARGO_PATH);
    let default_dict_path = cargo_path.join(dict_path);
    let canon_path = canonicalize(&default_dict_path);
   match canon_path {
       Ok(canon_dict_pathbuf)=>{
        let file = File::open(canon_dict_pathbuf).unwrap();

        let mut reader = BufReader::new(file);
        let mut line = String::with_capacity(50);
        let mut dict:Vec<CustomString> = Vec::with_capacity(600);
        while reader.read_line(&mut line).unwrap() != 0 {
            dict.push(CustomString::new(line.clone()));
            line.clear();
        }
        dict.shrink_to_fit();
        Trie::new(&dict) 
       }
       Err(unknown)=>{
        panic!("{:?}",unknown);
       }
       
    }

}

pub fn create_dict_trie(source:DictSource) -> Trie {
    match source {

        DictSource::FilePath(single_source) => {
            let file = File::open(single_source.as_path()).unwrap();

            let mut reader = BufReader::new(file);
            let mut line = String::with_capacity(50);
            let mut dict:Vec<CustomString> = Vec::with_capacity(600);
            while reader.read_line(&mut line).unwrap() != 0 {
                dict.push(CustomString::new(line.clone()));
                line.clear();
            }
            dict.shrink_to_fit();
            Trie::new(&dict) 
        },

        DictSource::WordList(word_list)=>{
            let custom_word_list:Vec<CustomString> = word_list.into_iter().map(|word| {CustomString::new(word)}).collect();
            Trie::new(&custom_word_list)
        }
    }
  

}