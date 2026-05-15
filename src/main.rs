use anyhow::Result;
use clap::Parser;
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use local_ip_address::local_ip;
use ringbuf::HeapRb;
use std::net::UdpSocket;
use std::sync::Arc;
use std::time::Duration;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    mode: String,

    #[arg(short, long)]
    ip: Option<String>,

    #[arg(short, long, default_value_t = 50005)]
    port: u16,
}

const SAMPLE_RATE: u32 = 44100;
const CHANNELS: u16 = 1;
const BUFFER_SIZE: usize = 4096;

fn main() -> Result<()> {
    let args = Args::parse();

    let host = cpal::default_host();
    let input_device = host.default_input_device().expect("No input device found");
    let output_device = host.default_output_device().expect("No output device found");

    let config = cpal::StreamConfig {
        channels: CHANNELS,
        sample_rate: cpal::SampleRate(SAMPLE_RATE),
        buffer_size: cpal::BufferSize::Default,
    };

    let socket = UdpSocket::bind(format!("0.0.0.0:{}", args.port))?;
    socket.set_read_timeout(Some(Duration::from_millis(100)))?;
    let socket = Arc::new(socket);

    println!("--- P2P Rust Voice Chat ---");

    if args.mode == "host" {
        let my_ip = local_ip()?;
        println!("Mode: Host");
        println!("Local IP: {}", my_ip);
        println!("Listening on port: {}", args.port);
        println!("Waiting for a peer to join...");
    } else if let Some(target_ip) = args.ip {
        println!("Mode: Join");
        println!("Connecting to: {}:{}", target_ip, args.port);
        socket.connect(format!("{}:{}", target_ip, args.port))?;
        // Send a dummy packet to let the host know our address
        socket.send(b"ping")?;
    } else {
        anyhow::bail!("IP is required in join mode");
    }

    // Audio Buffer for incoming data
    let rb = HeapRb::<f32>::new(BUFFER_SIZE * 2);
    let (mut prod, mut cons) = rb.split();

    // Receiving thread
    let socket_recv = Arc::clone(&socket);
    std::thread::spawn(move || {
        let mut buf = [0u8; 2048];
        loop {
            match socket_recv.recv_from(&mut buf) {
                Ok((size, addr)) => {
                    if args.mode == "host" {
                        // In host mode, we connect to the first person who pings us
                        let _ = socket_recv.connect(addr);
                    }
                    if size >= 4 {
                        let samples = size / 4;
                        for i in 0..samples {
                            let val = f32::from_le_bytes([
                                buf[i * 4],
                                buf[i * 4 + 1],
                                buf[i * 4 + 2],
                                buf[i * 4 + 3],
                            ]);
                            let _ = prod.push(val);
                        }
                    }
                }
                Err(_) => {}
            }
        }
    });

    // Output Stream
    let output_stream = output_device.build_output_stream(
        &config,
        move |data: &mut [f32], _: &cpal::OutputCallbackInfo| {
            for sample in data.iter_mut() {
                *sample = cons.pop().unwrap_or(0.0);
            }
        },
        |err| eprintln!("Output stream error: {}", err),
        None,
    )?;

    // Input Stream
    let socket_send = Arc::clone(&socket);
    let input_stream = input_device.build_input_stream(
        &config,
        move |data: &[f32], _: &cpal::InputCallbackInfo| {
            let mut byte_buf = Vec::with_capacity(data.len() * 4);
            for &sample in data {
                byte_buf.extend_from_slice(&sample.to_le_bytes());
            }
            let _ = socket_send.send(&byte_buf);
        },
        |err| eprintln!("Input stream error: {}", err),
        None,
    )?;

    input_stream.play()?;
    output_stream.play()?;

    println!("Audio streaming active. Press Ctrl+C to stop.");

    let (tx, rx) = std::sync::mpsc::channel();
    ctrlc::set_handler(move || tx.send(()).expect("Could not send signal on channel."))?;
    rx.recv()?;

    println!("Shutting down...");
    Ok(())
}
