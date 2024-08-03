# Example Scripts for Wickie

## Directory Structure

Aside from the configuration folder ("mongodb"), this repositry also contains three empty folders.

`wke` will populate `./logs` with output from machines when you run experiments.
It will collect data into CSV files and write them to `./results`.
Finally, it will also create plots automatically and store them in `./plots`.

## Setting up the Cluster

First, create an experiment on Cloudlab using the profile from `cloudlab_profile.toml`.
Note, you can also create your own profile like so `wke-cloudlab generate-profile --num-nodes=2`.

Then, download its manifest and store it as `manifest.xml`.
Finally, run `wke-cloudlab extract-config manifest.xml`

Alternatively, you can create a cluster anywhere and set up the `cluster.toml` file manually.

## MongoDB

In this example, we use one machine as the server and one as the client.
To run MongoDB on the server you first need to build it from soiurce or install it from a package.

To build MongoDB on the first machine (which will be our server), run:
```
wke run mongodb [0] install-packages,build-mongodb 
```
`install-packages` is a built in target that installs all Debian packages needed by the configuration, while `build-mongodb` is a custom target stored in `./mongodb/targets/install-mongodb`

To install a pre-built version of mongod instead, run:
```
wke run mongodb [0] install-packages,install-mongodb
```

`install-mongodb` is a custom target that pulls the required debian package from MongoDB's repositories.
