#Make the tsk 0 under puppet
exec {'Upgrade apt':
    command => "apt-get -y update"
}
exec { 'Install Nginx':
    require => Exec['Upgrade apt']
    command => "apt-get -y install nginx"
}
exec { 'Create Dic1':
    require => Exec['Install Nginx']
    command => "mkdir -p /data/web_static/releases/test"
}
exec { 'Create Dict2':
    require => Exec['Create Dic1']
    command => "mkdir -p /data/web_static/shared"
}
exec { 'Fill data':
    require => Exec['Create Dic2']
    command => "echo "Hello world" > /data/web_static/releases/test/index.html"
}
exec { 'Create symb link':
    require => Exec['Fill data']
    command => "ln -sf /data/web_static/releases/test/ /data/web_static/current"
}
exec { 'Change permission':
    require => Exec['Create symb link']
    command => "chown -hR ubuntu:ubuntu /data/"
}
exec { 'Open locations':
    require => Exec['Change permission']
    command => "sed -i "38i\\\tlocation /hbnb_static/ {\n\t\t alias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default"
}
exec { 'Nginx restart':
    require => Exec['Open locations']
    command => "service nginx restart"
}