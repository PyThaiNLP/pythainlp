use hashbrown::HashSet;
use lazy_static::lazy_static;
use rayon::prelude::*;
use bytecount::num_chars;
use smol_str::SmolStr;
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
use regex::Regex;

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
        "^เ[ก-ฮ]็[ก-ฮ]",
        "^เ[ก-ฮ][ก-ฮ][่-๋]?าะ",
        "^เ[ก-ฮ][ก-ฮ]ี[่-๋]?ยะ",
        "^เ[ก-ฮ][ก-ฮ]ี[่-๋]?ย[เ-ไก-ฮ]",
        "^เ[ก-ฮ][ก-ฮ]็[ก-ฮ]",
        "^เ[ก-ฮ]ิ[ก-ฮ]์[ก-ฮ]",
        "^เ[ก-ฮ]ิ[่-๋]?[ก-ฮ]",
        "^เ[ก-ฮ]ี[่-๋]?ยะ?",
        "^เ[ก-ฮ]ื[่-๋]?อะ?",
        "^เ[ก-ฮ][ิีุู][่-๋]?ย[เ-ไก-ฮ]",
        "^เ[ก-ฮ][่-๋]?า?ะ?",
        "^[ก-ฮ]ั[่-๋]?วะ",
        "^[ก-ฮ][ัื][่-๋]?[ก-ฮ][ุิะ]?",
        "^[ก-ฮ][ิุู]์",
        "^[ก-ฮ][ะ-ู][่-๋]?",
        "^[ก-ฮ]็",
        "^[ก-ฮ][่-๋]?[ะาำ]?",
        "^แ[ก-ฮ]็[ก-ฮ]",
        "^แ[ก-ฮ][ก-ฮ]์",
        "^แ[ก-ฮ][่-๋]?ะ",
        "^แ[ก-ฮ][ก-ฮ]็[ก-ฮ]",
        "^แ[ก-ฮ][ก-ฮ][ก-ฮ]์",
        "^โ[ก-ฮ][่-๋]?ะ",
        "^[เ-ไ][ก-ฮ][่-๋]?",
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
        "^เ[ก-ฮ][ก-ฮ]ี[่-๋]?ย[เ-ไก-ฮ]",
        "^เ[ก-ฮ][ิีุู][่-๋]?ย[เ-ไก-ฮ]",
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

pub fn tcc_pos<'a, S: Into<Cow<'a, str>>>(input: S) -> HashSet<usize> {
    let text:&str = &input.into();
    let mut set: HashSet<usize> = HashSet::new();
    if text == "" {
        set
    } else {
        let mut position: usize = 0;
        let word_segments = segment(text);
        for segment in word_segments.into_iter() {
            let segment_length = num_chars(segment.as_bytes());
            position += segment_length;
            set.insert(position);
        }
        set
    }
}
#[deprecated()]

pub fn segment<'a, S: Into<Cow<'a, str>>>(text: S) -> Vec<Cow<'a, str>> {
    let mut txt:&str = &text.into();
    let mut tcc_result: Vec<Cow<'a, str>> = Vec::with_capacity(txt.len());
    lazy_static! {
        static ref non_lookahead_tcc: Regex = Regex::new( &[
            "^เ[ก-ฮ]็[ก-ฮ]",
            "^เ[ก-ฮ][ก-ฮ][่-๋]?าะ",
            "^เ[ก-ฮ][ก-ฮ]ี[่-๋]?ยะ",
            "^เ[ก-ฮ][ก-ฮ]ี[่-๋]?ย[เ-ไก-ฮ]",
            "^เ[ก-ฮ][ก-ฮ]็[ก-ฮ]",
            "^เ[ก-ฮ]ิ[ก-ฮ]์[ก-ฮ]",
            "^เ[ก-ฮ]ิ[่-๋]?[ก-ฮ]",
            "^เ[ก-ฮ]ี[่-๋]?ยะ?",
            "^เ[ก-ฮ]ื[่-๋]?อะ?",
            "^เ[ก-ฮ][ิีุู][่-๋]?ย[เ-ไก-ฮ]",
            "^เ[ก-ฮ][่-๋]?า?ะ?",
            "^[ก-ฮ]ั[่-๋]?วะ",
            "^[ก-ฮ][ัื][่-๋]?[ก-ฮ][ุิะ]?",
            "^[ก-ฮ][ิุู]์",
            "^[ก-ฮ][ะ-ู][่-๋]?",
            "^[ก-ฮ]็",
            "^[ก-ฮ][่-๋]?[ะาำ]?",
            "^แ[ก-ฮ]็[ก-ฮ]",
            "^แ[ก-ฮ][ก-ฮ]์",
            "^แ[ก-ฮ][่-๋]?ะ",
            "^แ[ก-ฮ][ก-ฮ]็[ก-ฮ]",
            "^แ[ก-ฮ][ก-ฮ][ก-ฮ]์",
            "^โ[ก-ฮ][่-๋]?ะ",
            "^[เ-ไ][ก-ฮ][่-๋]?",
        ]
        .join("|")).unwrap();
    }
    lazy_static! {
        static ref lookahead_tcc: Regex = Regex::new(&[
            "^เ[ก-ฮ][ก-ฮ]ี[่-๋]?ย[เ-ไก-ฮ]",
            "^เ[ก-ฮ][ิีุู][่-๋]?ย[เ-ไก-ฮ]",
        ]
        .join("|")).unwrap();
    }
    while num_chars(txt.as_bytes()) > 0 {
            let text_length = num_chars(txt.as_bytes());
        if let Some(result) = non_lookahead_tcc.find(&txt) {
            //It's all thai;
            let mut matched = &txt[result.start()..result.end()];
            
            let match_length = num_chars(matched.as_bytes());
            if lookahead_tcc.is_match(matched) {
                let end_thai_bytes_index = (match_length-1)*THAI_BYTES_SIZE;
                matched  = &matched[0..end_thai_bytes_index];
                tcc_result.push(Cow::Owned(matched.to_string()));
                // let txt_iter = &mut txt.chars();
                // let skip = txt_iter.skip(first_match_count);
                txt = &txt[end_thai_bytes_index..]
            }else{
                tcc_result.push(Cow::Owned(matched.to_string()));
                // let txt_iter = &mut txt.chars();
                // let skip = txt_iter.skip(first_match_count);
                let end_thai_bytes_index = (match_length)*THAI_BYTES_SIZE;
                txt = &txt[end_thai_bytes_index..];
            }
            
            // tcc_result.push(Cow::Owned(matched.to_string()));
            // // let txt_iter = &mut txt.chars();
            // // let skip = txt_iter.skip(first_match_count);
            // txt = txt.substring(num_chars(matched.as_bytes()), num_chars(txt.as_bytes()));
            
        } else {
            // not thai
            let first_char = txt.substring(0, 1);
            tcc_result.push(Cow::Owned(first_char.to_string()));
            txt = txt.substring(1, text_length);
         
        }
    }
    tcc_result
}

#[test]
fn test_new_pattern() {
    let tcc_non_lookahead_pattern = pattern_tcc_non_lookahead_part();
    let tcc_lookahead_pattern = pattern_tcc_lookahead_part();
    let string = "ราชวงศ์ชิงพยายามลดการละเมิดสิทธิ์และความไม่ลงรอยกันในพื้นที่โดย
    ออกกฎหมายเพื่อจัดการตรวจ";
// println!("{:?}",tcc_pos(string,&tcc_non_lookahead_pattern));
    assert_eq!(
        segment("ประเทศไทย"),
        vec!["ป", "ระ", "เท", "ศ", "ไท", "ย"]
    );
    assert_eq!(segment("เกกี้ยดด"), vec!["เกกี้ย", "ด", "ด"]);
    assert_eq!(segment("ทดเกี้ยน"), vec!["ท", "ด", "เกี้ย", "น"]);
    assert_eq!(
        segment("เรียนท่านประธานที่ไม่เคารพ"),
        vec![
            "เรีย",
            "น",
            "ท่า",
            "น",
            "ป",
            "ระ",
            "ธา",
            "น",
            "ที่",
            "ไม่",
            "เคา",
            "ร",
            "พ"
        ]
    );
    assert_eq!(
        segment("ฮั่ยเหย่โหว"),
        vec!["ฮั่ย", "เห", "ย่", "โห", "ว"]
    );
    let blank_result: Vec<String> = vec![];
    assert_eq!(segment(""), blank_result);

    let first_tcc_pos = tcc_pos("ประเทศไทย");
    assert_eq!(first_tcc_pos.contains(&1), true);
    assert_eq!(first_tcc_pos.contains(&3), true);
    assert_eq!(first_tcc_pos.contains(&5), true);
    assert_eq!(first_tcc_pos.contains(&6), true);
    assert_eq!(first_tcc_pos.contains(&8), true);
    assert_eq!(first_tcc_pos.contains(&9), true);
  
}
