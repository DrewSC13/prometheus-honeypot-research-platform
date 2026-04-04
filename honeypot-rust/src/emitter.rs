use std::sync::{Arc, OnceLock};

use anyhow::Result;

use crate::amqp::AmqpPublisher;
use crate::event::PrometheusEvent;

static PUBLISHER: OnceLock<Arc<AmqpPublisher>> = OnceLock::new();

pub fn init_publisher(publisher: AmqpPublisher) -> Result<()> {
    PUBLISHER
        .set(Arc::new(publisher))
        .map_err(|_| anyhow::anyhow!("publisher already initialized"))?;
    Ok(())
}

pub fn emit_event(event: &PrometheusEvent) -> Result<()> {
    let json = serde_json::to_string(event)?;
    println!("{json}");

    if let Some(publisher) = PUBLISHER.get() {
        let publisher = Arc::clone(publisher);
        let event = event.clone();

        tokio::spawn(async move {
            if let Err(err) = publisher.publish(&event).await {
                eprintln!("AMQP publish error: {err}");
            }
        });
    }

    Ok(())
}
