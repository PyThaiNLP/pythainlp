use crate::fixed_bytes_str::four_bytes::ValidUTF8BytesVec;


/**
    This should be the only part exposed to lib.rs
 */
pub trait Tokenizer {
    fn segment(&self,text:&str,safe:Option<bool>,parallel:Option<bool>)->Vec<ValidUTF8BytesVec>;

}