


pub mod tokenizer;
pub mod fixed_bytes_str;

use crate::tokenizer::newmm_custom::{Newmm};
use lazy_static::lazy_static;

use pyo3::wrap_pyfunction;
use pyo3::prelude::*;
use tokenizer::tokenizer_trait::Tokenizer;
lazy_static! {
    static ref DEFAULT_DICT:Newmm = Newmm::new(None);
}

/// segment(text, safe, parallel, /)
/// --
///
/// This function is newmm algorithhm.
/// Uses only default dict.
/// Can use multithreading, but takes a lot of memory.

/// ***Should be used to tokenize very, very long text (around 5000*30 Thai words est.)***

/// signature:    (text: str, safe = false, parallel = false) -> List[str]
#[pyfunction]
fn segment(text:&str,safe:Option<bool>,parallel:Option<bool>) -> PyResult<Vec<String>> {
    
    let result = DEFAULT_DICT.segment(text, safe,parallel);
    Ok(result)
}


#[pymodule]
fn oxidized_thainlp(_py: Python, m: &PyModule) -> PyResult<()> {
  
    m.add_function(wrap_pyfunction!(segment, m)?)?;

    Ok(())
}