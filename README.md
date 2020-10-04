![](./images/banner.png)

This is the repo for all the challenges built for and run as the CTF mini-event
run at HackTheMidlands 2020 :tada: :tada:

It's also got a whole bunch of other stuff, like CTFd site resources,
deployment scripts, etc.

Checkout the writeups at the [wiki](https://github.com/jedevc/HackTheMidlandsCTF20/wiki).

Please feel free to play around with all the challenges, use them yourself or
let them be inspiration for your own challenges.

## Try it yourself

Running and building the challenges assumes a Linux machine along with a
number of common dependencies.

### Generate challenges

Compile and build all the different challenge files, such as images,
binaries, etc.

    $ ./infra/ctftool.py generate

To remove all compiled challenge files:

    $ ./infra/ctftool.py clean

### Run challenges

Run the docker containers.

    # Set PYTHONPATH to find the ctftool.py utility
    $ export PYTHONPATH=$PWD/infra

    # Build docker containers
    $ ./infra/deploy/build.py

    # Generate the docker-compose configuration
    $ mkdir -p build
    $ cp -R deploy/docker-compose/ build/
    $ ./build/docker-compose/generate.sh

    # Run docker-compose configuration
    $ (cd build/docker-compose && docker-compose up)

## Deployment

For more information on deployment, see [ctf-infra](https://github.com/jedevc/ctf-infra/).
