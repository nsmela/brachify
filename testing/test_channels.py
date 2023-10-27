import Application.BRep.Channel as channel
import testing.data.channels as data

channels_data = data.points()

def test_rounded_channel():
    assert channel.rounded_channel(channels_data[0]) is not None

def test_rounded_channel_bad_input():
    assert channel.rounded_channel([[0,0,0]]) is None

