#!/usr/bin/env python3
import alan

def test_defaults(qtbot):
    '''
    test to ensure settings pages are properly populated
    '''
    form = alan.AlanApp()
    form.show()
    qtbot.addWidget(form)
    assert form.listen_ip.toPlainText() == "127.0.0.2"
    assert form.remote_ip.toPlainText() == "127.0.0.1"
    assert form.listen_port.toPlainText() == "10000"
    assert form.remote_port.toPlainText() == "8000"
