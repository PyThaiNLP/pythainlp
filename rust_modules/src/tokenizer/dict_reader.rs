use std::{error::Error, fs::File, path::PathBuf};
use std::io::prelude::*;
use std::io::BufReader;
use rayon::prelude::*;
use super::trie::Trie;
pub enum DictSource {
    WordList(Vec<String>),
    FilePath(PathBuf)
}
pub fn create_dict_trie(source:DictSource) -> Trie {
    match source {

        DictSource::FilePath(single_source) => {
            println!("{:?}",single_source);
            let file = File::open(single_source.as_path()).unwrap();

            let mut reader = BufReader::new(file);
            let mut line = String::with_capacity(1000);
            let mut dict:Vec<String> = Vec::with_capacity(60000);
            while reader.read_line(&mut line).unwrap() != 0 {
                dict.push(line.clone());
                line.clear();
            }
            Trie::new(&dict) 
        },

        DictSource::WordList(word_list)=>{
           
            Trie::new(&word_list)
        }
    }
  

}