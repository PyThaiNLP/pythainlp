use hashbrown::{HashMap, HashSet};
use substring::Substring;
use std::borrow::BorrowMut;
use std::iter::Iterator;
use rayon::prelude::*;
use bytecount::num_chars;
use lazy_static::lazy_static;
use regex::Regex;
/**
This module is meant to be a direct implementation of Dict Trie in PythaiNLP.

Many functions are implemented as a recursive function because of the limits imposed by
Rust Borrow Checker and this author's (Thanathip) little experience.

Rust Code: Thanathip Suntorntip (Gorlph)
*/

const THAI_BYTES_SIZE:usize =3;
#[derive(Debug)]
pub struct TrieNode {
    // text: Option<String>,
    children: HashMap<char, Self>,
    end: bool,
}

/** FOR THAI ONLY */
impl TrieNode {
    pub fn new() -> Self {
        Self {
            // text: None,
            children: HashMap::with_capacity(100),
            end: false,
        }
    }
    fn find_child(&self, word: char) -> Option<&Self> {
        self.children.get(&word)
    }
    fn remove_child(&mut self, word: char) {
        self.children.remove(&word);
    }
    fn find_mut_child(&mut self, word: char) -> Option<&mut Self> {
        self.children.get_mut(&word)
    }
    fn add_child(&mut self, word: char, child: Self) {
        self.children.insert(word, child);
    }
    fn set_not_end(&mut self) {
        self.end = false;
    }

    fn add_word(&mut self, input_word: &str) {
        let mut word = input_word.to_string();
        // self should be root node
        if let Some(character) = word.chars().nth(0) {
            if let Some(child) = self.find_mut_child(character) {
                word.remove(0);
                child.add_word(&word);
            } else {
                let child = TrieNode::new();
                self.add_child(character, child);
                if let Some(the_child) = self.find_mut_child(character) {
                    word.remove(0);
                    the_child.add_word(&word);
                }
            }
        } else {
            self.end = true;
        }
    }
    fn remove_word_from_node(&mut self, input_word: &str) {

        let mut word = input_word.to_string();
        let char_count = num_chars(word.as_bytes());
        if let Some(character) = word.chars().nth(0) {
            if let Some(child) = self.find_mut_child(character) {
                word.remove(0);
                if char_count == 1 {
                    child.set_not_end();
                }
                child.remove_word_from_node(&word);

                if !child.end && child.children.is_empty() {
                    self.remove_child(character);
                }
            };
        }
    }
    //TODO: fix this method!
    pub fn list_from_prefix(
        &self,
        prefix: &str,
        index: usize,
        mut accumulate_result: Vec<String>,
    ) -> Vec<String> {
        lazy_static! {
            static ref all_thai: Regex = Regex::new(r"^[\u0E00-\u0E7F]+$").unwrap();
        }
        if all_thai.is_match(prefix) {
            if let Some((_, character)) = prefix.char_indices().nth(index) {
                if let Some(child) = self.find_child(character) {
                    if child.end {
                        let substring_of_prefix: &str =  &prefix[0..(index+1)*THAI_BYTES_SIZE];
                            // prefix.chars().take(index + 1).collect();
                        accumulate_result.push(substring_of_prefix.to_string());
                    }
                    child.list_from_prefix(prefix, index + 1, accumulate_result)
                } else {
                    accumulate_result
                }
            } else {
                accumulate_result
            }
        }else {
        if let Some((_, character)) = prefix.char_indices().nth(index) {
            if let Some(child) = self.find_child(character) {
                if child.end {
                    let substring_of_prefix: &str = prefix.substring(0, index + 1);
                        // prefix.chars().take(index + 1).collect();
                    accumulate_result.push(substring_of_prefix.to_string());
                }
                child.list_from_prefix(prefix, index + 1, accumulate_result)
            } else {
                accumulate_result
            }
        } else {
            accumulate_result
        }
    }
}
}
#[derive(Debug)]
pub struct Trie {
    words: HashSet<String>,
    root: TrieNode,
}
impl Trie {
    pub fn new(words: &[String]) -> Self {
        let mut instance = Self {
            words: HashSet::with_capacity(100),
            root: TrieNode::new(),
        };
        for word in words.into_iter() {
            instance.add(&word);
        }
        instance
    }
    fn remove_word_from_set(&mut self, word: &str) {
        self.words.remove(word);
    }
    pub fn add(&mut self, word: &str) {
        let stripped_word = word.trim();
        self.words.insert(stripped_word.to_string());
        let current_cursor = self.root.borrow_mut();
        current_cursor.add_word(&stripped_word.to_string());
    }
    pub fn remove(&mut self, word: &str) {
        let stripped_word = word.trim().to_string();
        if self.words.contains(&stripped_word) {
            self.remove_word_from_set(&stripped_word);
            self.root.remove_word_from_node(word);
        }
    }
    pub fn prefix(&self, prefix: &str) -> Vec<String> {
        self.root.list_from_prefix(prefix, 0, Vec::with_capacity(100))
    }
    pub fn contain(&self, word: String) -> bool {
        self.words.contains(&word)
    }
    pub fn iterate(&self) -> hashbrown::hash_set::Iter<'_, String> {
        self.words.iter()
    }
    pub fn amount_of_words(&self) -> usize {
        self.words.iter().count()
    }
}
