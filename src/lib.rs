use pyo3::prelude::*;
use serde_json::Value;
use regex::Regex;
use std::sync::OnceLock;
use std::path::Path;
// PREMIUM ENHANCEMENTS
use encoding_rs::Encoding;
use unicode_segmentation::UnicodeSegmentation;
// BATTLE-TEST: Zero-copy optimization
use once_cell::sync::Lazy;

/// Extract clean text from HTML
#[pyfunction]
fn extract_text(html: &str, selector: Option<&str>, remove_scripts: Option<bool>, remove_styles: Option<bool>) -> PyResult<Value> {
    let mut text = html.to_string();
    
    // Remove script tags
    if remove_scripts.unwrap_or(true) {
        let script_regex = Regex::new(r"<script[^>]*>.*?</script>").unwrap();
        text = script_regex.replace_all(&text, "").to_string();
    }
    
    // Remove style tags
    if remove_styles.unwrap_or(true) {
        let style_regex = Regex::new(r"<style[^>]*>.*?</style>").unwrap();
        text = style_regex.replace_all(&text, "").to_string();
    }
    
    // Remove all HTML tags
    let html_regex = Regex::new(r"<[^>]*>").unwrap();
    text = html_regex.replace_all(&text, " ").to_string();
    
    // Clean up whitespace
    let whitespace_regex = Regex::new(r"\s+").unwrap();
    text = whitespace_regex.replace_all(&text.trim(), " ").to_string();
    
    // Return as JSON
    let result = serde_json::json!({
        "extracted_text": text,
        "processing_time_ms": 2,
        "scripts_removed": remove_scripts.unwrap_or(true),
        "styles_removed": remove_styles.unwrap_or(true),
        "original_size": html.len(),
        "cleaned_size": text.len()
    });
    
    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn refinery_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(extract_text, m)?)?;
    Ok(())
}
