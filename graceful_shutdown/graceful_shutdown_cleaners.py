from multiprocessing.synchronize import Event

# Function to handle cleanup on exit
def cleanup(stop_event: Event):
    print("Performing cleanup...")
    stop_event.set()  # Signal the background task to exit
    print("Performed cleanup...")

# Function to handle signals
def signal_handler(sig, frame, stop_event: Event):
    print("Signal received: exiting application...")
    cleanup(stop_event)  # Call cleanup
    exit(0)