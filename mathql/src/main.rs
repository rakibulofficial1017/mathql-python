use regex::{CaptureNames, Captures, Regex};

#[derive(Debug)]
struct Token {
    name: String,
    value: String,
}

fn main() {
    let keywords = vec!["let"];

    
    let escaped_keywords: Vec<String> = keywords.iter().map(|&k| regex::escape(k)).collect();
    let keyword_pattern = format!(r"\b(?:{})\b", escaped_keywords.join("|"));

    
    let token_rules = vec![
        ("NUMBER", r"\d+(?:\.\d*)?(?:e\d+)?"),
        ("STRING", r#"(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')"#),
        ("KEYWORD", &keyword_pattern),
        ("OPERATOR", r"[+\-=*/%^()]"),
        ("IDENTIFIER", r"[A-Za-z_][A-Za-z_0-9]*"),
        ("SEMICOLON", r";"),
    ];

    
    let combined_pattern = token_rules
        .iter()
        .map(|(name, pattern)| format!("(?P<{}>{})", name, pattern))
        .collect::<Vec<String>>()
        .join("|");

    let token_regex = Regex::new(&combined_pattern).expect("Invalid regex pattern");

    
    let line = "let v = 30;";
    let tokens = tokenize(&token_regex, line);

    
    println!("{:#?}", tokens);
}

fn tokenize(regex: &Regex, line: &str) -> Vec<Token> {
    let mut tokens = Vec::new();

    
    for caps in regex.captures_iter(line) {
        
        if caps.get(0).unwrap().as_str().trim().is_empty() {
            continue;
        }

        
        if let Some((name, value)) = get_matched_group_name(regex.capture_names(), &caps) {
            tokens.push(Token {
                name: name.to_string(),
                value: value.to_string(),
            });
        }
    }

    tokens
}


fn get_matched_group_name<'a>(
    mut names: CaptureNames<'a>,
    caps: &Captures<'a>,
) -> Option<(&'a str, &'a str)> {
    
    names.next(); 

    for name_opt in names {
        if let Some(name) = name_opt {
            if let Some(mat) = caps.name(name) {
                return Some((name, mat.as_str()));
            }
        }
    }
    None
}
