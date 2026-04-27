<h1 align="center"> welcome to qwave!! </h1>

<p align=center>
    <img src="logo_lg.png">
</p>

## what is this?
qWave is a locally hosted media server designed for music! that is to say, it's like spotify or any other streaming service, ran on your own network under your control with your media files. That way you can stream your personal media files from anywhere instead of just on one device!

## installation
qWave is designed to run on Linux only. I recommend you run it on a dedicated server machine (as simple as a rpi), but it will work just fine running in the background on your desktop machine, as long as you're okay with it being the dependency for all your devices.



## setup for development
- first: `git clone https://github.com/qwikster/qwave.git && cd qwave`.
- you'll need to create a venv: `python3 -m venv .venv` then `source .venv/bin/activate`
- install qwave as a package locally: `pip install -e ./qwave-server`
