
use pyo3::prelude::*;
use pyo3::types::PyDict;
use regex::{Captures, Regex};

#[derive(Debug)]
struct Token {
    name: String,
    value: String,
}

#[pyfunction]
fn tokenize<'py>(
    py: Python<'py>,
    line: &str,
) -> PyResult<Vec<Bound<'py, PyDict>>> {
    let keywords = ["let"];

    let escaped_keywords: Vec<String> = keywords
        .iter()
        .map(|k| regex::escape(k))
        .collect();

    let keyword_pattern =
        format!(r"\b(?:{})\b", escaped_keywords.join("|"));

    let token_rules = vec![
        ("NUMBER", r"\d+(?:\.\d*)?(?:[eE][+-]?\d+)?"),
        ("STRING", r#"(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')"#),
        ("KEYWORD", keyword_pattern.as_str()),
        ("OPERATOR", r"[+\-=*/%^()]"),
        ("IDENTIFIER", r"[A-Za-z_][A-Za-z_0-9]*"),
        ("SEMICOLON", r";"),
    ];

    let combined_pattern = token_rules
        .iter()
        .map(|(name, pattern)| format!("(?P<{}>{})", name, pattern))
        .collect::<Vec<_>>()
        .join("|");

    let token_regex = Regex::new(&combined_pattern)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;

    let mut tokens = Vec::new();

    for caps in token_regex.captures_iter(line) {
        let matched = caps.get(0).unwrap();

        if matched.as_str().trim().is_empty() {
            continue;
        }

        let name = token_rules
            .iter()
            .find_map(|(name, _)| {
                caps.name(name).map(|_| *name)
            })
            .unwrap_or("UNKNOWN");

        let token = PyDict::new(py);
        token.set_item("name", name)?;
        token.set_item("value", matched.as_str())?;

        tokens.push(token);
    }

    Ok(tokens)
}

#[pymodule]
fn mathql_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tokenize, m)?)?;
    Ok(())
}
