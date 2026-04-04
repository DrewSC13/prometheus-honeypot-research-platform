use std::net::SocketAddr;
use std::sync::{Arc, Mutex};

use anyhow::{anyhow, Result};
use async_trait::async_trait;
use russh::server::Server as _;
use russh::server::{self, Auth, Msg, Session};
use russh::{Channel, ChannelId};
use russh_keys::key;
use serde_json::json;
use uuid::Uuid;

use crate::config::AppConfig;
use crate::emitter::emit_event;
use crate::event::{EventMetadata, PrometheusEvent};

#[derive(Clone)]
pub struct Server {
    pub config: AppConfig,
}

#[derive(Clone)]
pub struct ClientHandler {
    pub app_config: AppConfig,
    pub peer_addr: Option<SocketAddr>,
    pub session_id: Uuid,
    pub event_sequence: Arc<Mutex<u64>>,
}

impl ClientHandler {
    fn next_sequence(&self) -> u64 {
        let mut guard = self.event_sequence.lock().expect("event_sequence poisoned");
        *guard += 1;
        *guard
    }

    fn peer_ip(&self) -> String {
        self.peer_addr
            .map(|addr| addr.ip().to_string())
            .unwrap_or_else(|| "0.0.0.0".to_string())
    }

    fn peer_port(&self) -> u16 {
        self.peer_addr.map(|addr| addr.port()).unwrap_or(0)
    }

    fn emit(&self, event_type: &str, payload: serde_json::Value, ingest_source: &str) {
        let event = PrometheusEvent::new(
            self.peer_ip(),
            self.peer_port(),
            self.app_config.bind_port,
            self.session_id,
            self.next_sequence(),
            event_type,
            payload,
            EventMetadata::new(&self.app_config.sensor_id, ingest_source),
        );

        if let Err(err) = emit_event(&event) {
            eprintln!("[ERROR] failed to emit event: {err}");
        }
    }
}

impl server::Server for Server {
    type Handler = ClientHandler;

    fn new_client(&mut self, peer_addr: Option<SocketAddr>) -> Self::Handler {
        let handler = ClientHandler {
            app_config: self.config.clone(),
            peer_addr,
            session_id: Uuid::new_v4(),
            event_sequence: Arc::new(Mutex::new(0)),
        };

        handler.emit(
            "ssh.session_start",
            json!({
                "connection_state": "opened",
                "client_banner": null,
                "server_banner": self.config.server_banner
            }),
            "ssh-listener",
        );

        handler
    }
}

#[async_trait]
impl server::Handler for ClientHandler {
    type Error = anyhow::Error;

    async fn auth_password(&mut self, user: &str, password: &str) -> Result<Auth, Self::Error> {
        self.emit(
            "ssh.auth_attempt",
            json!({
                "username": user,
                "password": password,
                "auth_method": "password"
            }),
            "ssh-auth-handler",
        );

        self.emit(
            "ssh.auth_result",
            json!({
                "success": false,
                "reason": "invalid_credentials"
            }),
            "ssh-auth-handler",
        );

        Ok(Auth::Reject {
            proceed_with_methods: None,
        })
    }

    async fn channel_open_session(
        &mut self,
        _channel: Channel<Msg>,
        _session: &mut Session,
    ) -> Result<bool, Self::Error> {
        Ok(true)
    }

    async fn channel_close(
        &mut self,
        _channel: ChannelId,
        _session: &mut Session,
    ) -> Result<(), Self::Error> {
        self.emit(
            "ssh.connection_closed",
            json!({
                "reason": "channel_closed",
                "had_authenticated_session": false
            }),
            "ssh-connection-handler",
        );

        Ok(())
    }
}

#[allow(clippy::field_reassign_with_default)]
pub async fn run_ssh_server(config: AppConfig) -> Result<()> {
    let mut server_config = russh::server::Config::default();
    server_config.inactivity_timeout = Some(std::time::Duration::from_secs(30));
    server_config.auth_rejection_time = std::time::Duration::from_secs(1);

    let keypair = key::KeyPair::generate_ed25519()
        .ok_or_else(|| anyhow!("failed to generate ed25519 host key"))?;
    server_config.keys.push(keypair);

    let server_config = Arc::new(server_config);
    let mut server = Server {
        config: config.clone(),
    };

    let bind_addr = format!("{}:{}", config.bind_addr, config.bind_port);
    println!("[INFO] Starting SSH honeypot on {bind_addr}");

    server.run_on_address(server_config, bind_addr).await?;
    Ok(())
}
