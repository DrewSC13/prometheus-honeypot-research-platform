mod config;
mod emitter;
mod event;
mod ssh;

use anyhow::Result;
use config::AppConfig;
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

    run_ssh_server(config).await
}
