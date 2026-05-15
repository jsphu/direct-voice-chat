import argparse
import threading
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box

from network import UDPSocketManager, get_local_ips
from audio import AudioManager

console = Console()


def capture_and_send(audio_manager, network_manager, stop_event):
    """Thread function to capture audio from mic and send via UDP."""
    while not stop_event.is_set():
        data = audio_manager.read_chunk()
        if data:
            network_manager.send(data)


def receive_and_play(audio_manager, network_manager, stop_event):
    """Thread function to receive audio via UDP and play to speakers."""
    while not stop_event.is_set():
        data, addr = network_manager.receive()
        if data:
            audio_manager.write_chunk(data)


def main():
    parser = argparse.ArgumentParser(description="P2P Terminal Voice Chat")
    parser.add_argument(
        "--mode",
        choices=["host", "join"],
        required=True,
        help="Run as host or join a session",
    )
    parser.add_argument(
        "--ip", help="Host IP address to connect to (required for join mode)"
    )
    parser.add_argument(
        "--port", type=int, default=50005, help="UDP port (default: 50005)"
    )
    args = parser.parse_args()

    if args.mode == "join" and not args.ip:
        console.print("[red]Error: --ip is required in join mode.[/red]")
        sys.exit(1)

    network_manager = UDPSocketManager(port=args.port)
    audio_manager = AudioManager()

    # Display Welcome Banner
    console.print(
        Panel.fit(
            "[bold cyan]P2P Terminal Voice Chat[/bold cyan]\n[italic white]Cross-platform, low-latency audio over UDP[/italic white]",
            box=box.DOUBLE,
            border_style="bright_blue",
        )
    )

    if args.mode == "host":
        ips = get_local_ips()
        ips_str = ", ".join(ips) if ips else "None found"
        console.print(f"[bold green]Mode:[/bold green] Host")
        console.print(f"[bold green]Local IPs:[/bold green] {ips_str}")
        console.print(f"[bold green]Listening on port:[/bold green] {args.port}")
        console.print("[yellow]Waiting for a peer to join...[/yellow]")

        if not network_manager.bind():
            sys.exit(1)
    else:
        console.print(f"[bold green]Mode:[/bold green] Join")
        console.print(f"[bold green]Connecting to:[/bold green] {args.ip}:{args.port}")
        network_manager.set_target(args.ip, args.port)

    if not audio_manager.start_streams():
        sys.exit(1)

    stop_event = threading.Event()

    # Start threads
    send_thread = threading.Thread(
        target=capture_and_send,
        args=(audio_manager, network_manager, stop_event),
        daemon=True,
    )
    recv_thread = threading.Thread(
        target=receive_and_play,
        args=(audio_manager, network_manager, stop_event),
        daemon=True,
    )

    send_thread.start()
    recv_thread.start()

    status_table = Table(box=box.SIMPLE)
    status_table.add_column("Status", style="bold magenta")
    status_table.add_column("Value", style="white")

    status_table.add_row("Audio", "[green]Streaming[/green]")
    status_table.add_row("Network", "[green]Active[/green]")
    status_table.add_row("Control", "Press [bold red]Ctrl+C[/bold red] to quit")

    try:
        with Live(status_table, refresh_per_second=4):
            while True:
                time.sleep(1)
                # Check if threads are still alive
                if not send_thread.is_alive() or not recv_thread.is_alive():
                    break
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")
    finally:
        stop_event.set()
        audio_manager.close()
        network_manager.close()
        console.print("[bold green]Goodbye![/bold green]")


if __name__ == "__main__":
    main()
