Switchpub
=========

This is code that I use on [my website](https://cleverdevil.io) to publish daily
records of my gaming sessions on my Nintendo Switch. To create this code, I
needed to reverse engineer the API used by the
[Nintedo Switch Parental Controls app for iOS](https://itunes.apple.com/us/app/nintendo-switch-parental-cont/id1190074407).

In order for these scripts to talk to the API, a number of variables will need
to be discovered, including your device identifier, "smart" device identifier,
client identifier, and a session token. The best way to get these is to download
the parental controls app to an iOS device, and then to set up a network proxy
to inspect the traffic that the app sends during authentication. I personally
used [Charles Proxy](https://www.charlesproxy.com) for this purpose, which
provides the necssary [MITM
proxy](https://www.charlesproxy.com/documentation/proxying/ssl-proxying/)
features. 

Once you've got things configured properly in `conf.py`, you can first run
`fetch.py`, which will write out a `summary.json` file. Then, you can run
`process.py`, which will require some light editing for your use case.
Currently, `process.py` has some hardcoded variables that are specific to my
website. In addition, `process.py` is hardcoded to publish to my website through
my own custom webhook. You may want to use something like Micropub.

Note: all of this was inspired by [Eddie Hinkle](https://eddiehinkle.com), who
did this first!
