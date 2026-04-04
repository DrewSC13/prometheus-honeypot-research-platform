mod amqp;
mod config;
mod emitter;
mod event;
mod ssh;

use amqp::AmqpPublisher;
use anyhow::Result;
use config::AppConfig;
use emitter::init_publisher;
use ssh::server::run_ssh_server;

#[tokio::main]
async fn main() -> Result<()> {
    let config = AppConfig::default();

    println!("[INFO] Prometheus SSH honeypot starting...");
    println!(
        "[INFO] Bind address: {}:{}",
        config.bind_addr, config.bind_port
    );
    println!("[INFO] Sensor ID: {}", config.sensor_id);

    let amqp_uri = "amqp://prom_bus:Popete13@127.0.0.1:5672/%2f";
    let publisher = AmqpPublisher::new(amqp_uri, "prometheus.events").await?;
    init_publisher(publisher)?;

    run_ssh_server(config).await
}
