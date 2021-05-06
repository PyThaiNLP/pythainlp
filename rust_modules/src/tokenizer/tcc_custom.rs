use ahash::{AHashMap as HashMap, AHashSet as HashSet};
use lazy_static::lazy_static;
use rayon::prelude::*;
use bytecount::num_chars;
use smol_str::SmolStr;
use regex::bytes::Regex;
use crate::fixed_bytes_str::four_bytes::{self, CustomString};

use super::super::fixed_bytes_str::four_bytes::{BYTES_PER_CHAR,encode_utf8,to_four_bytes};


lazy_static! {
    static ref NON_LOOKAHEAD_TCC: Regex = Regex::new( &[
        r"^\x00เ\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ](\x00[่-๋])?\x00า\x00ะ",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย\x00ะ",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00ิ\x00[ก-ฮ]\x00์\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00ิ(\x00[่-๋])?\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย(\x00ะ)?",
        r"^\x00เ\x00[ก-ฮ]\x00ื(\x00[่-๋])?\x00อ(\x00ะ)?",
        r"^\x00เ\x00[ก-ฮ](\x00[่-๋])?(\x00า)?(\x00ะ)?",
        r"^\x00[ก-ฮ]\x00ั(\x00[่-๋])?\x00ว\x00ะ",
        r"^\x00[ก-ฮ]\x00[ัื](\x00[่-๋])?\x00[ก-ฮ](\x00[ุิะ])?",
        r"^\x00[ก-ฮ]\x00[ิุู]\x00์",
        r"^\x00[ก-ฮ]\x00[ะ-ู](\x00[่-๋])?",
        r"^\x00[ก-ฮ]\x00็",
        r"^\x00[ก-ฮ](\x00[่-๋])?(\x00[ะาำ])?",
        r"^\x00แ\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00แ\x00[ก-ฮ]\x00[ก-ฮ]\x00์",
        r"^\x00แ\x00[ก-ฮ](\x00[่-๋])?\x00ะ",
        r"^\x00แ\x00[ก-ฮ]\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00แ\x00[ก-ฮ]\x00[ก-ฮ]\x00[ก-ฮ]\x00์",
        r"^\x00โ\x00[ก-ฮ](\x00[่-๋])?\x00ะ",
        r"^\x00[เ-ไ]\x00[ก-ฮ](\x00[่-๋])?",
        r"^\x00เ\x00[ก-ฮ]\x00[ิีุู](\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
    ]
    .join("|")).unwrap();
}
lazy_static! {
    static ref LOOKAHEAD_TCC: Regex = Regex::new(&[
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00[ิีุู](\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
    ]
    .join("|")).unwrap();
}
/**
The implementation of tokenizer accorinding to Thai Character Clusters (TCCs)
rules purposed by `Theeramunkong et al. 2000. \
    <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.2548>`_

Credits:
    * TCC: Jakkrit TeCho
    * Grammar: Wittawat Jitkrittum (`link to the source file \
      <https://github.com/wittawatj/jtcc/blob/master/TCC.g>`_)
    * Python code: Korakot Chaovavanich
    * Rust Code Translation: Thanathip Suntorntip
*/


use std::{borrow::Cow, time::{Instant,Duration}};
use substring::Substring;
// to be re-implement
const THAI_BYTES_SIZE:usize = 3;
#[deprecated()]
fn pattern_tcc() -> Regex {
    // Regex crate does not support look-any-direction

    let reg_tcc = &[
        "^(เ[ก-ฮ]็[ก-ฮ])",
        "^(เ[ก-ฮ][ก-ฮ][่-๋]?าะ)",
        "^(เ[ก-ฮ][ก-ฮ]ี[่-๋]?ยะ)",
        "^(เ[ก-ฮ][ก-ฮ]ี[่-๋]?ย)(?:[เ-ไก-ฮ]|$)",
        "^(เ[ก-ฮ][ก-ฮ]็[ก-ฮ])",
        "^(เ[ก-ฮ]ิ[ก-ฮ]์[ก-ฮ])",
        "^(เ[ก-ฮ]ิ[่-๋]?[ก-ฮ])",
        "^(เ[ก-ฮ]ี[่-๋]?ยะ?)",
        "^(เ[ก-ฮ]ื[่-๋]?อะ?)",
        "^(เ[ก-ฮ][ิีุู][่-๋]?ย)(?:[เ-ไก-ฮ]|$)",
        "^(เ[ก-ฮ][่-๋]?า?ะ?)",
        "^([ก-ฮ]ั[่-๋]?วะ)",
        "^([ก-ฮ][ัื][่-๋]?[ก-ฮ][ุิะ]?)",
        "^([ก-ฮ][ิุู]์)",
        "^([ก-ฮ][ะ-ู][่-๋]?)",
        "^([ก-ฮ]็)",
        "^([ก-ฮ][่-๋]?[ะาำ]?)",
        "^(แ[ก-ฮ]็[ก-ฮ])",
        "^(แ[ก-ฮ][ก-ฮ]์)",
        "^(แ[ก-ฮ][่-๋]?ะ)",
        "^(แ[ก-ฮ][ก-ฮ]็[ก-ฮ])",
        "^(แ[ก-ฮ][ก-ฮ][ก-ฮ]์)",
        "^(โ[ก-ฮ][่-๋]?ะ)",
        "^([เ-ไ][ก-ฮ][่-๋]?)",
    ]
    .join("|");
    match Regex::new(reg_tcc) {
        Ok(tcc_regex) => tcc_regex,
        Err(err) => {
            println!("{}", err);
            panic!("incorrect regex");
        }
    }
}

pub fn pattern_tcc_non_lookahead_part() -> Regex {

    // Regex crate does not support look-any-direction

    let reg_tcc_no_lookahead = &[
        r"^\x00เ\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ](\x00[่-๋])?\x00า\x00ะ",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย\x00ะ",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00ิ\x00[ก-ฮ]\x00์\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00ิ(\x00[่-๋])?\x00[ก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย(\x00ะ)?",
        r"^\x00เ\x00[ก-ฮ]\x00ื(\x00[่-๋])?\x00อ(\x00ะ)?",
        r"^\x00เ\x00[ก-ฮ](\x00[่-๋])?(\x00า)?(\x00ะ)?",
        r"^\x00[ก-ฮ]\x00ั(\x00[่-๋])?\x00ว\x00ะ",
        r"^[\x00ก-ฮ]\x00[ัื](\x00[่-๋])?\x00[ก-ฮ](\x00[ุิะ])?",
        r"^[\x00ก-ฮ]\x00[ิุู]\x00์",
        r"^[\x00ก-ฮ]\x00[ะ-ู](\x00[่-๋])?",
        r"^\x00[ก-ฮ]\x00็",
        r"^\x00[ก-ฮ](\x00[่-๋])?(\x00[ะาำ])?",
        r"^\x00แ\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00แ\x00[ก-ฮ]\x00[ก-ฮ]\x00์",
        r"^\x00แ\x00[ก-ฮ](\x00[่-๋])?\x00ะ",
        r"^\x00แ\x00[ก-ฮ]\x00[ก-ฮ]\x00็\x00[ก-ฮ]",
        r"^\x00แ\x00[ก-ฮ]\x00[ก-ฮ]\x00[ก-ฮ]\x00์",
        r"^\x00โ\x00[ก-ฮ](\x00[่-๋]?)\x00ะ",
        r"^\x00[เ-ไ]\x00[ก-ฮ](\x00[่-๋])?",
        r"^\x00เ\x00[ก-ฮ]\x00[ิีุู](\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
    ]
    .join("|");
    match Regex::new(reg_tcc_no_lookahead) {
        Ok(tcc_regex) => tcc_regex,
        Err(err) => {
            println!("{}", err);
            panic!("incorrect regex");
        }
    }
}

pub fn pattern_tcc_lookahead_part() -> Regex {

    // Regex crate does not support look-any-direction

    let reg_tcc_lookahead = &[
        r"^\x00เ\x00[ก-ฮ]\x00[ก-ฮ]\x00ี(\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
        r"^\x00เ\x00[ก-ฮ]\x00[ิีุู](\x00[่-๋])?\x00ย\x00[เ-ไก-ฮ]",
    ]
    .join("|");
    match Regex::new(reg_tcc_lookahead) {
        Ok(tcc_regex) => tcc_regex,
        Err(err) => {
            println!("{}", err);
            panic!("incorrect regex");
        }
    }
}

pub fn tcc_pos(custom_text_type:&[u8]) -> HashSet<usize> {
    let mut set: HashSet<usize> = HashSet::with_capacity(custom_text_type.len() / BYTES_PER_CHAR);
    if custom_text_type.len() == 0 {
        set
    } else {
        let mut position: usize = 0;
        let four_bytes_chars_segment = segment(custom_text_type);
        for segment in four_bytes_chars_segment.into_iter() {
            let segment_size = segment.len() / BYTES_PER_CHAR;
            position += segment_size;
            set.insert(position);
        }
        set.shrink_to_fit();
        set
    }
}

pub fn segment(custom_text_type:&[u8]) -> Vec<&[u8]> {
    // todo!();
    let mut txt  = custom_text_type.clone();
    let mut tcc_result: Vec<&[u8]> = Vec::with_capacity(txt.len()*4/5);
    while txt.len() > 0 {
        if let Some(result) = NON_LOOKAHEAD_TCC.find(&txt) {
            //It's all thai;
            let mut matched = &txt[result.start()..result.end()];
            
            let match_length = matched.len();
            if LOOKAHEAD_TCC.is_match(matched) {
                // trim one more char
                let end_bytes_index = (match_length-(1*BYTES_PER_CHAR));
                matched  = &matched[0..end_bytes_index];
                tcc_result.push(matched);
                // let txt_iter = &mut txt.chars();
                // let skip = txt_iter.skip(first_match_count);
                txt = &txt[end_bytes_index..];
            }else{
                tcc_result.push(matched);
                // let txt_iter = &mut txt.chars();
                // let skip = txt_iter.skip(first_match_count);
                let end_bytes_index = (match_length);
                txt = &txt[end_bytes_index..];
            }
            
            // tcc_result.push(Cow::Owned(matched.to_string()));
            // // let txt_iter = &mut txt.chars();
            // // let skip = txt_iter.skip(first_match_count);
            // txt = txt.substring(num_chars(matched.as_bytes()), num_chars(txt.as_bytes()));
            
        } else {
            // not thai
            // println!("{:?}",&txt);
            let first_char = &txt[0..BYTES_PER_CHAR];
            // println!("{:?}",first_char);
            tcc_result.push(first_char);
            txt = &txt[BYTES_PER_CHAR..];
         
        }
    }
    tcc_result
}

#[test]
fn test_new_pattern() {
    let tcc_non_lookahead_pattern = pattern_tcc_non_lookahead_part();
    // tcc_non_lookahead_pattern.find(text)
    // let tcc_lookahead_pattern = pattern_tcc_lookahead_part();
    // let string =four_bytes::to_four_bytes("ประเทศไทย");
    // println!("{:?}",tcc_non_lookahead_pattern.find(&string));
    
// // println!("{:?}",tcc_pos(string,&tcc_non_lookahead_pattern));
    let test_1=four_bytes::to_four_bytes("ประเทศไทย");
    
    let result = segment(&test_1);

    for outer in 0..result.len(){
        for index in (0..result[outer].len()).step_by(BYTES_PER_CHAR){
        print!("{:?}",encode_utf8(&result[outer][index..index+BYTES_PER_CHAR]));
        }
        println!();
    }
      
   
//     assert_eq!(segment("เกกี้ยดด"), vec!["เกกี้ย", "ด", "ด"]);
//     assert_eq!(segment("ทดเกี้ยน"), vec!["ท", "ด", "เกี้ย", "น"]);
//     assert_eq!(
//         segment("เรียนท่านประธานที่ไม่เคารพ"),
//         vec![
//             "เรีย",
//             "น",
//             "ท่า",
//             "น",
//             "ป",
//             "ระ",
//             "ธา",
//             "น",
//             "ที่",
//             "ไม่",
//             "เคา",
//             "ร",
//             "พ"
//         ]
//     );
//     assert_eq!(
//         segment("ฮั่ยเหย่โหว"),
//         vec!["ฮั่ย", "เห", "ย่", "โห", "ว"]
//     );
//     let blank_result: Vec<String> = vec![];
//     assert_eq!(segment(""), blank_result);

//     let first_tcc_pos = tcc_pos("ประเทศไทย");
//     assert_eq!(first_tcc_pos.contains(&1), true);
//     assert_eq!(first_tcc_pos.contains(&3), true);
//     assert_eq!(first_tcc_pos.contains(&5), true);
//     assert_eq!(first_tcc_pos.contains(&6), true);
//     assert_eq!(first_tcc_pos.contains(&8), true);
//     assert_eq!(first_tcc_pos.contains(&9), true);
  
}
