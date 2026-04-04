use crate::event::PrometheusEvent;
use anyhow::Result;

pub fn emit_event(event: &PrometheusEvent) -> Result<()> {
    let json = serde_json::to_string(event)?;
    println!("{json}");
    Ok(())
}
