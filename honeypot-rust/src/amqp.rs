use anyhow::Result;
use lapin::{
    options::*, types::FieldTable, BasicProperties, Channel, Connection, ConnectionProperties,
};
use serde_json::to_vec;

use crate::event::PrometheusEvent;

pub struct AmqpPublisher {
    channel: Channel,
    exchange: String,
}

impl AmqpPublisher {
    pub async fn new(uri: &str, exchange: &str) -> Result<Self> {
        let conn = Connection::connect(uri, ConnectionProperties::default()).await?;

        let channel = conn.create_channel().await?;

        // Declarar exchange
        channel
            .exchange_declare(
                exchange.into(),
                lapin::ExchangeKind::Topic,
                ExchangeDeclareOptions::default(),
                FieldTable::default(),
            )
            .await?;

        Ok(Self {
            channel,
            exchange: exchange.to_string(),
        })
    }

    pub async fn publish(&self, event: &PrometheusEvent) -> Result<()> {
        let payload = to_vec(event)?;

        let routing_key = &event.event_type;

        self.channel
            .basic_publish(
                self.exchange.clone().into(),
                routing_key.clone().into(),
                BasicPublishOptions::default(),
                &payload,
                BasicProperties::default(),
            )
            .await?
            .await?;

        Ok(())
    }
}
