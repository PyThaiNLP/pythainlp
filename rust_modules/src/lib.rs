pub mod fixed_bytes_str;
pub mod tokenizer;

use crate::tokenizer::newmm_custom::Newmm;
use ahash::AHashMap as HashMap;
use fixed_bytes_str::four_bytes::ValidUTF8BytesVec;
use lazy_static::lazy_static;
use std::sync::Mutex;
use pyo3::prelude::*;
use pyo3::{exceptions, wrap_pyfunction};
use tokenizer::tokenizer_trait::Tokenizer;
lazy_static! {
    static ref  DICT_COLLECTION:Mutex<HashMap<String,Box<Newmm>>> = Mutex::new(HashMap::new());
    // static ref DEFAULT_DICT:Newmm = Newmm::new(None);
}

/// segment(text,dict_name, safe, parallel, /)
/// --
///
/// This function is newmm algorithhm.
/// Uses only default dict.
/// Can use multithreading, but takes a lot of memory.

/// returns list of valid utf-8 bytes list
/// signature:    (text: str, safe = false, parallel = false) -> List[List[u8]]
#[pyfunction]
fn segment(
    text: &str,
    dict_name: &str,
    safe: Option<bool>,
    parallel: Option<bool>,
) -> PyResult<Vec<ValidUTF8BytesVec>> {
    if let Some(loaded_dict) = DICT_COLLECTION.lock().unwrap().get(dict_name) {
        let result = loaded_dict.segment(text, safe, parallel);
        Ok(result)
    } else {
        Err(exceptions::PyRuntimeError::new_err(format!(
            "Dictinary {} does not exist.",
            dict_name
        )))
    }
}

/// load_dict(file_path,dict_name /)
/// --
///
/// This function loads a dictionary file and add it to dict collection
/// Dict file must be a file of words seperate by line.

/// returns a string of loading result
#[pyfunction]
fn load_dict(file_path: &str, dict_name: &str) -> PyResult<String> {
    let mut dict_col_lock = DICT_COLLECTION.lock().unwrap();
    if dict_name == "default" {
        Ok(format!("Failed: 'default' dictionary name is reserved"))
    } else if let Some(_) = dict_col_lock.get(dict_name) {
        Ok(format!(
            "Failed: dictionary {} exists, please use another name.",
            dict_name
        ))
    } else {
        let newmm_dict = Newmm::new(Some(file_path));
        dict_col_lock.insert(dict_name.to_owned(), Box::new(newmm_dict));

        Ok(format!(
            "Successful: dictionary name {} from file {} has been successfully loaded",
            dict_name, file_path
        ))
    }
}
#[pymodule]
fn oxidized_thainlp(_py: Python, m: &PyModule) -> PyResult<()> {
    {
    let mut dict_collect = DICT_COLLECTION.lock().unwrap();
    dict_collect.insert("default".to_string(), Box::from(Newmm::new(None)));
    }
    m.add_function(wrap_pyfunction!(load_dict,m)?)?;
    m.add_function(wrap_pyfunction!(segment, m)?)?;
    Ok(())
}
