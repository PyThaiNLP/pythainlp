/**
Dictionary-based maximal matching word segmentation, constrained with
Thai Character Cluster (TCC) boundaries.

The code is based on the notebooks created by Korakot Chaovavanich,
with heuristic graph size limit added to avoid exponential wait time.

:See Also:
    * \
        https://colab.research.google.com/notebook#fileId=1V1Z657_5eSWPo8rLfVRwA0A5E4vkg7SI
    * \
        https://colab.research.google.com/drive/14Ibg-ngZXj15RKwjNwoZlOT32fQBOrBx#scrollTo=MYZ7NzAR7Dmw

Rust implementation: ["Thanathip Suntorntip"]
*/
// TODO: use slice_by_chars_indice on &[u8]
use crate::fixed_bytes_str::four_bytes::{
    rfind_space_char_index, CustomString, FixedCharsLengthByteSlice, BYTES_PER_CHAR,
};

use super::super::fixed_bytes_str::four_bytes::{
    CustomStringBytesSlice, CustomStringBytesVec, ValidUTF8BytesSlice, ValidUTF8BytesVec,
};
use super::{
    dict_reader_custom::{create_default_dict, create_dict_trie, DictSource},
    tcc_custom,
    tokenizer_trait::Tokenizer,
    trie_custom::Trie,
};
use ahash::{AHashMap as HashMap, AHashSet as HashSet};
use binary_heap_plus::{BinaryHeap, MinComparator};
use lazy_static::lazy_static;
use rayon::prelude::*;
use regex::bytes::Regex;
use std::{collections::VecDeque, path::PathBuf};
const MAX_GRAPH_SIZE: usize = 50;
const USE_MULTITHREAD_THRESHOLD: usize = 100;

// Window size for safe mode
const TEXT_SCAN_POINT: usize = 120;
const TEXT_SCAN_LEFT: usize = 20;
const TEXT_SCAN_RIGHT: usize = 20;
const TEXT_SCAN_BEGIN: usize = TEXT_SCAN_POINT - TEXT_SCAN_LEFT;
const TEXT_SCAN_END: usize = TEXT_SCAN_POINT + TEXT_SCAN_RIGHT;

type CharacterIndex = usize;

lazy_static! {
    static ref NON_THAI_PATTERN: Regex = Regex::new(
        r"^(\x00\x00\x00[-a-zA-Z])+|^\x00\x00\x00\d(\x00\x00\x00[\d,\.])*|^(\x00\x00\x00[ \t])+|^(\x00\x00\x00\r)?\x00\x00\x00\n"
    )
    .unwrap();
}

lazy_static! {
    static ref THAI_TWOCHARS_PATTERN: Regex = Regex::new(r"^(\x00[ก-ฮ]){0,2}$").unwrap();
}
pub struct Newmm {
    dict: Box<Trie>,
}

impl Newmm {
    pub fn new(dict_path: Option<&str>) -> Self {
        match dict_path {
            None => Self {
                dict: Box::from(create_default_dict()),
            },
            Some(path) => Self {
                dict: Box::from(create_dict_trie(DictSource::FilePath(PathBuf::from(path))).unwrap()),
            },
        }
    }
    #[inline]
    fn bfs_paths_graph(
        graph: &HashMap<CharacterIndex, Vec<CharacterIndex>>,
        start: CharacterIndex,
        goal: CharacterIndex,
    ) -> Vec<CharacterIndex> {
        let mut current_queue: VecDeque<(usize, Vec<usize>)> = VecDeque::with_capacity(graph.len());
        let mut init_path: Vec<usize> = Vec::with_capacity(goal - start);
        init_path.push(start);
        current_queue.push_back((start, init_path));
        while current_queue.len() > 0 {
            let (vertex, path) = current_queue.pop_front().unwrap();
            if let Some(idk) = graph.get(&vertex) {
                for position in idk {
                    if *position != goal {
                        let mut appended_path = path.clone();
                        appended_path.push(*position);
                        current_queue.push_back((*position, appended_path));
                    } else {
                        let mut appended_path = path.clone();
                        appended_path.push(*position);

                        return appended_path;
                    };
                }
            };
        }
        panic!("something wrong");
    }
    #[inline]
    fn one_cut(input: &CustomStringBytesSlice, custom_dict: &Trie) -> Vec<CustomStringBytesVec> {
        let text = input;
        let input_char_len = text.len() / BYTES_PER_CHAR;
        let mut graph_size: usize = 0;
        let mut graph: HashMap<CharacterIndex, Vec<CharacterIndex>> =
            HashMap::with_capacity(input_char_len / 100);
        let mut result_str: Vec<CustomStringBytesVec> = Vec::with_capacity(input_char_len / 100);

        // all position should be refered as character index
        let valid_position = tcc_custom::tcc_pos(input);
        let text_length = input_char_len;
        let mut position_list: BinaryHeap<CharacterIndex, MinComparator> = BinaryHeap::new_min();
        let mut existing_candidate: HashSet<CharacterIndex> = HashSet::with_capacity(50);
        position_list.push(0);
        existing_candidate.insert(0);
        let mut end_position: usize = 0;
        // as long as there is a value in the position_list priority queue
        // AND its value is less than text_length
        while match position_list.peek() {
            std::option::Option::Some(position) if *position < text_length => true,
            std::option::Option::None => false,
            _ => false,
        } {
            if let Some(begin_position) = position_list.pop() {
                let byte_index_of_begin_char = begin_position * BYTES_PER_CHAR;
                let sub_text_prefix = &text[byte_index_of_begin_char..];
                let prefixes = custom_dict.prefix(sub_text_prefix);
                for word in prefixes {
                    let word_length = word.len() / BYTES_PER_CHAR;
                    let end_position_candidate = begin_position + word_length;
                    if valid_position.contains(&end_position_candidate) {
                        let target_graph = graph.get_mut(&begin_position);
                        match target_graph {
                            Some(existing_path) => {
                                existing_path.push(end_position_candidate);
                            }
                            None => {
                                graph.insert(begin_position, vec![end_position_candidate]);
                            }
                        }

                        graph_size += 1;
                        if !existing_candidate.contains(&end_position_candidate) {
                            existing_candidate.insert(end_position_candidate);
                            position_list.push(end_position_candidate);
                        }
                        if graph_size > MAX_GRAPH_SIZE {
                            break;
                        }
                    }
                }
                let position_list_length = position_list.len();
                if position_list_length == 1 {
                    //only one candidate!
                    if let Some(first_position_list) = position_list.peek() {
                        let group_of_end_position_candidate =
                            Self::bfs_paths_graph(&graph, end_position, *first_position_list);
                        graph_size = 0; // reset our graph

                        for position in group_of_end_position_candidate.iter().skip(1) {
                            let token = &text
                                [(end_position * BYTES_PER_CHAR)..(*position * BYTES_PER_CHAR)];
                            result_str.push(Vec::from(token));
                            end_position = *position;
                        }
                    } else {
                        panic!("incorrect position list");
                    }
                } else if position_list_length == 0 {
                    // no candidate, deal with non-dict word
                    match NON_THAI_PATTERN.find(sub_text_prefix) {
                        Some(match_point) => {
                            //  non thai -> skip to the end of match - this is byte index not char index...
                            end_position = begin_position
                                + sub_text_prefix[match_point.start()..match_point.end()].len()
                                    / BYTES_PER_CHAR;
                        }
                        None => {
                            // Is thai -> find min skip
                            let mut finish_without_break = true;
                            for position in begin_position + 1..text_length {
                                if valid_position.contains(&position) {
                                    // let (prefix_byte_index,_) = text.char_indices().nth(position).unwrap();
                                    // let prefix = text.substring(position, text_length);
                                    let prefix = &text
                                        [position * BYTES_PER_CHAR..text_length * BYTES_PER_CHAR];
                                    let list_of_prefixes = custom_dict.prefix(&prefix);
                                    let valid_word_filter = |word: &Vec<u8>| {
                                        let new_position = position + (word.len() / BYTES_PER_CHAR);
                                        let is_valid = valid_position.contains(&new_position);
                                        let is_two_thai_chars =
                                            THAI_TWOCHARS_PATTERN.is_match(&word);
                                        is_valid && !is_two_thai_chars
                                    };
                                    let valid_words: Vec<Vec<u8>> =
                                        if list_of_prefixes.len() >= USE_MULTITHREAD_THRESHOLD {
                                            list_of_prefixes
                                                .into_par_iter()
                                                .filter(valid_word_filter)
                                                .collect()
                                        } else {
                                            list_of_prefixes
                                                .into_iter()
                                                .filter(valid_word_filter)
                                                .collect()
                                        };

                                    if valid_words.len() > 0 {
                                        end_position = position;
                                        finish_without_break = false;
                                        break;
                                    };
                                    if NON_THAI_PATTERN.is_match(&prefix) {
                                        end_position = position;
                                        finish_without_break = false;
                                        break;
                                    }
                                }
                            }
                            if finish_without_break {
                                end_position = text_length;
                            }
                        }
                    }
                    let current_graph_opt = graph.get_mut(&begin_position);
                    match current_graph_opt {
                        Some(existing_path) => {
                            existing_path.push(end_position);
                            graph_size += 1;
                            let token = &text
                                [begin_position * BYTES_PER_CHAR..end_position * BYTES_PER_CHAR];
                            result_str.push(Vec::from(token));
                            position_list.push(end_position);
                            existing_candidate.insert(end_position);
                        }
                        None => {
                            let mut graph_elem: Vec<usize> = Vec::with_capacity(10);
                            graph_elem.push(end_position);
                            graph.insert(begin_position, graph_elem);
                            graph_size += 1;
                            let token = &text
                                [begin_position * BYTES_PER_CHAR..end_position * BYTES_PER_CHAR];
                            result_str.push(Vec::from(token));
                            position_list.push(end_position);
                            existing_candidate.insert(end_position);
                        }
                    }
                }
            }
        }

        result_str.shrink_to_fit();
        result_str
    }
    pub fn internal_segment(
        input: &CustomString,
        custom_dict: &Trie,
        safe: bool,
        parallel: bool,
    ) -> Vec<CustomStringBytesVec> {
        if input.len() == 0 {
            return vec![];
        }
        if !safe || input.chars_len() < TEXT_SCAN_END {
            let result = Self::one_cut(input.raw_content(), custom_dict);
            return if parallel {
                result
                    .into_par_iter()
                    .map(|custom_string_bytes| {
                        CustomString::convert_raw_bytes_to_utf8_bytes(&custom_string_bytes)
                    })
                    .collect()
            } else {
                result
                    .into_iter()
                    .map(|custom_string_bytes| {
                        CustomString::convert_raw_bytes_to_utf8_bytes(&custom_string_bytes)
                    })
                    .collect()
            };
        } else {
            let mut txt = input.raw_content();
            let mut txt_parts: Vec<CustomStringBytesVec> = Vec::with_capacity(txt.len() / 10);
            while txt.chars_len() >= TEXT_SCAN_END {
                let sample: &[u8] = txt.slice_by_char_indice(TEXT_SCAN_BEGIN, TEXT_SCAN_END);

                let mut cut_pos = TEXT_SCAN_END;

                let space_char_index = rfind_space_char_index(sample);
                // there is a space
                if let Some(space_char_index) = space_char_index {
                    cut_pos = space_char_index + 1;
                } else {
                    let word_tokens = Self::one_cut(sample, &custom_dict);
                    let mut token_max_index = 0;
                    for (idx, token) in word_tokens.iter().enumerate() {
                        let mut token_max_length = 0;

                        if token.as_slice().chars_len() > token_max_length {
                            token_max_length = token.as_slice().chars_len();
                            token_max_index = idx;
                        }
                    }
                    // choose the position that covers longest token
                    cut_pos = TEXT_SCAN_BEGIN;
                    for i in 0..token_max_index {
                        cut_pos = cut_pos + word_tokens.get(i).unwrap().as_slice().chars_len();
                    }
                }
                txt_parts.push(txt.slice_by_char_indice(0, cut_pos).to_owned());
                txt = txt.slice_by_char_indice(cut_pos, txt.chars_len());
            }
            if txt.len() > 0 {
                txt_parts.push(txt.to_owned());
            }

            if parallel {
                txt_parts
                    .into_par_iter()
                    .flat_map(|part| {
                        Self::one_cut(&part, &custom_dict)
                            .into_par_iter()
                            .map(|word| CustomString::convert_raw_bytes_to_utf8_bytes(&word))
                            .collect::<Vec<ValidUTF8BytesVec>>()
                    })
                    .collect::<Vec<ValidUTF8BytesVec>>()
            } else {
                txt_parts
                    .iter()
                    .flat_map(|part| {
                        Self::one_cut(&part, &custom_dict)
                            .iter()
                            .map(|word| CustomString::convert_raw_bytes_to_utf8_bytes(&word))
                            .collect::<Vec<ValidUTF8BytesVec>>()
                    })
                    .collect::<Vec<ValidUTF8BytesVec>>()
            }
        }
    }
}

impl Tokenizer for Newmm {
    fn segment(
        &self,
        text: &str,
        safe: Option<bool>,
        parallel: Option<bool>,
    ) -> Vec<ValidUTF8BytesVec> {
        let safe_flag = match safe {
            Some(val) => val,
            None => false,
        };
        let parallel_flag = match parallel {
            Some(val) => val,
            _ => false,
        };
        let custom_string = CustomString::new(text);
        let tokens = Self::internal_segment(&custom_string, &self.dict, safe_flag, parallel_flag);
        tokens
    }
}
