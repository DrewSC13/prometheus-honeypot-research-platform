#[derive(Debug, Clone)]
pub struct AppConfig {
    pub bind_addr: String,
    pub bind_port: u16,
    pub server_banner: String,
    pub sensor_id: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            bind_addr: "0.0.0.0".to_string(),
            bind_port: 2222,
            server_banner: "SSH-2.0-PrometheusSSH_0.1".to_string(),
            sensor_id: "sensor-ssh-01".to_string(),
        }
    }
}
