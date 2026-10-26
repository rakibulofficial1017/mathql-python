use pyo3::prelude::*;
use regex::Regex;
use std::sync::LazyLock;

static TOKEN_REGEX: LazyLock<Regex> = LazyLock::new(||
    Regex::new( r#"(?P<NUMBER>\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)|(?P<STRING>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(?P<KEYWORD>\b(?:let)\b)|(?P<OPERATOR>[+\-=*/%^()])|(?P<IDENTIFIER>[A-Za-z_][A-Za-z_0-9]*)|(?P<SEMICOLON>;)"#) // Regex isn't mean to be readable so just put up with it
        .expect("INVALID REGEX, BLAME THE DEVELOPER")
);

#[pyfunction]
fn tokenize(line: &str) -> Vec<(String, String)> {
    let mut tokens = Vec::new();

    for caps in TOKEN_REGEX.captures_iter(line) {
        let value = caps.get(0).unwrap().as_str();

        let name = [
            "NUMBER",
            "STRING",
            "KEYWORD",
            "OPERATOR",
            "IDENTIFIER",
            "SEMICOLON"
        ]
        .iter()
        .find(|&&name| caps.name(name).is_some())
        .unwrap();

        tokens.push((name.to_string(), value.to_string()));
        

    }
    tokens
}

#[pymodule]
fn mathql_rust(m: &Bound<'_, PyModule>) -> PyResult<()>{
    m.add_function(wrap_pyfunction!(tokenize, m)?)?;
    Ok(())
}