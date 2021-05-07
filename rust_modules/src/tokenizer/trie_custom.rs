use crate::fixed_bytes_str::four_bytes::{CustomString, BYTES_PER_CHAR,FixedCharsLengthByteSlice,CustomStringBytesSlice,CustomStringBytesVec};
use ahash::{AHashMap as HashMap, AHashSet as HashSet};
use std::borrow::{Borrow, BorrowMut};
use std::iter::Iterator;
/**
This module is meant to be a direct implementation of Dict Trie in PythaiNLP.

Many functions are implemented as a recursive function because of the limits imposed by
Rust Borrow Checker and this author's (Thanathip) little experience.

Rust Code: Thanathip Suntorntip (Gorlph)
*/

#[derive(Debug)]
pub struct TrieNode {
    children: HashMap<CustomStringBytesVec, Self>,
    end: bool,
}

/** FOR CUSTOM 4-BYTE TEXT ONLY */
impl TrieNode {
    pub fn new() -> Self {
        Self {
            // text: None,
            children: HashMap::with_capacity(100),
            end: false,
        }
    }
    fn find_child(&self, word: &CustomStringBytesSlice) -> Option<&Self> {
        self.children.get(word)
    }
    fn remove_child(&mut self, word: &CustomStringBytesSlice) {
        self.children.remove(word);
    }
    fn find_mut_child(&mut self, word: &CustomStringBytesSlice) -> Option<&mut Self> {
        self.children.get_mut(word)
    }
    fn set_not_end(&mut self) {
        self.end = false;
    }
    fn add_word(&mut self, input_word: &CustomStringBytesSlice) {
        // thanks to https://stackoverflow.com/questions/36957286/how-do-you-implement-this-simple-trie-node-in-rust
        if input_word.len() == 0 {
            self.end = true;
            return;
        }
        self.children
            .entry((&input_word[0..BYTES_PER_CHAR]).into())
            .or_insert(TrieNode::new())
            .add_word(&input_word[BYTES_PER_CHAR..]);
    }
    fn remove_word_from_node(&mut self, input_word: &CustomStringBytesSlice) {
        let mut word = input_word.clone();
        let char_count = word.len() / BYTES_PER_CHAR;
        // if has atleast 1 char
        if word.len() >= BYTES_PER_CHAR {
            let character = &word.slice_by_char_indice(0,1);
            if let Some(child) = self.find_mut_child(character) {
                // move 1 character
                word = &word[BYTES_PER_CHAR..];
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
    pub fn list_prefix(&self, prefix: &CustomStringBytesSlice) -> Vec<CustomStringBytesVec> {
        let mut result: Vec<CustomStringBytesVec> = Vec::with_capacity(100);
        let prefix_cpy = prefix;
        let mut current_index = 0;
        let mut current_node_wrap = Some(self);
        while (current_index) * BYTES_PER_CHAR <  prefix_cpy.len()   {
            let character = &prefix_cpy[(current_index * BYTES_PER_CHAR)..((current_index+1)*BYTES_PER_CHAR)];
            if let Some(current_node) = current_node_wrap {
                if let Some(child) = current_node.find_child(character) {
                    if child.end {
                        let substring_of_prefix = &prefix_cpy[0..(current_index+1)*BYTES_PER_CHAR];
                        result.push(substring_of_prefix.to_owned());
                    }
                    current_node_wrap = Some(child);
                } else {
                    break;
                }
            }
            current_index = current_index + 1;
        }
        result.shrink_to_fit();
        result
    }
}
#[derive(Debug)]
pub struct Trie {
    words: HashSet<CustomStringBytesVec>,
    root: TrieNode,
}
impl Trie {
    pub fn new(words: &Vec<CustomString>) -> Self {
        let mut instance = Self {
            words: HashSet::with_capacity(words.len()/10),
            root: TrieNode::new(),
        };
        for word in words.into_iter() {
            instance.add(&word);
        }
        instance
    }
    fn remove_word_from_set(&mut self, word: &CustomStringBytesVec) {
        self.words.remove(word);
    }
    pub fn add(&mut self, word: &CustomString) {
        let stripped_word = word.trim();
        self.words.insert(stripped_word.raw_content().into());
        let current_cursor = self.root.borrow_mut();
        current_cursor.add_word(&stripped_word.raw_content());
    }
    pub fn remove(&mut self, word: &CustomString) {
        let stripped_word = word.trim();
        let stripped_word_raw = &stripped_word.raw_content().into();
        if self.words.contains(stripped_word_raw) {
            self.remove_word_from_set(stripped_word_raw);
            self.root.remove_word_from_node(stripped_word_raw);
        }
    }
    pub fn prefix(&self, prefix: &CustomStringBytesSlice) -> Vec<Vec<u8>> {
        self.root.list_prefix(prefix)
    }
    pub fn contain(&self, word: &CustomStringBytesVec) -> bool {
        self.words.contains(word)
    }
    pub fn iterate(&self) -> std::collections::hash_set::Iter<'_, Vec<u8>> {
        self.words.iter()
    }
    pub fn amount_of_words(&self) -> usize {
        self.words.iter().count()
    }
}
