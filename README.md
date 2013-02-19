vhosts
======

Virtual Host utility for exposing your projects with virtual hosts with Apache. It only works for linux now since it uses avahi-publish to expose projects via mDNS.

Setup
=====

Initialize the main vhosts setting directory by executing the init subcommand:

    user$ vhosts init

Include the following line in your apache configuration inside the VirtualHosts section:

    Include /home/username/.vhosts/apache2/vhosts.conf

You should now be ready to start up vhosts and start exposing projects.

    user$ vhosts start

*NOTE* by default the virtual hosts resolve to 127.0.0.1 for security reasons.
You can change the address setting in ~/.vhosts/vhosts.json to expose your
virtual hosts to your LAN. Restart vhosts after to correctly expose any
vhosts you've already configured.

    user$ vhosts stop
    user$ vhosts start

Usage
=====

To start up the daemon for DNS resolution:

    user$ vhosts start

To take them offline:

    user$ vhosts stop

To add a virtual host:

    user$ vhosts add [vhost] [documentroot]

Your project will now be accesible from https://vhost.local.

To remove a virtual host:

    user$ vhosts del [vhost]

Now the project is no longer accesible.

To list all the currently exposed virtual hosts:

    user$ vhosts list

