vhosts
======

Virtual Host utility for exposing your projects with virtual hosts with Apache. It only works for linux now since it uses avahi-publish to expose projects via mDNS.

Setup
=====

Create the directory $HOME/.vhosts with the following subdirectories:

    .vhosts/
        apache2/
        links/

Place the following file into $HOME/.vhosts/apache2/vhosts.conf:

<IfModule mod_vhost_alias.c>
  VirtualDocumentRoot /home/username/.vhosts/links/%1
</IfModule>

Include the following line in your apache configuration inside the VirtualHosts section:

    Include /home/username/.vhosts/apache2/vhosts.conf

Usage
=====

To start up the daemon for DNS resolution:

    user$ vhosts start

To take them offline:

    user$ vhosts stop

To add a virtual host:

    user$ vhosts add [vhost] [documentroot]

Your project will now be accesible from https://vhost.local.
