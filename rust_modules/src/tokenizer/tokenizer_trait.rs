use super::trie_custom::Trie;
use pyo3::{Py, PyResult, prelude, types::PyList};
use pyo3::types::PyString;
/**
    This should be the only part exposed to lib.rs
 */
pub trait Tokenizer {
    fn segment(&self,text:String,safe:Option<bool>)->Vec<String>;

}