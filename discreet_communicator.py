
import subprocess
from gi.repository import GLib, Gst

def execute_command(command):
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    Gst.init(None)

    # Commandes GStreamer
    pipeline_str = 'alsasrc device="hw:1,0" ! audioconvert ! audioresample ! rtpL24pay ! meshsink host=239.0.0.1 port=5001 auto-multicast=true'
    pipeline = Gst.parse_launch(pipeline_str)

    command2_str = 'udpsrc port=5001 ! application/x-rtp,media=audio,payload=96,clock-rate=44100,encoding-name=L24 ! queue ! rtpL24depay ! audioconvert ! alsasink device=hw:1,0'
    command2 = Gst.parse_launch(command2_str)

    # Démarrer le pipeline
    pipeline.set_state(Gst.State.PLAYING)
    command2.set_state(Gst.State.PLAYING)

    thread2 = GLib.Thread(target=execute_command, args=('gst-launch-1.0 -v ' + command2_str,))
    thread2.start()

    thread2.join()

    # Arrêter le pipeline
    pipeline.set_state(Gst.State.NULL)
    command2.set_state(Gst.State.NULL)
