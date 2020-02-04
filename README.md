# pluto
Watchdog **pluto** cares for your downloads-folder


### Table of Contents
[Setup](#setup)


<a name="#setup">
## setup
</a>
### cloning git
```
git clone https://github.com/Zadest/pluto
```
### creating pluto.cf
```
touch pluto.cf
$EDITOR pluto.cf
```
! Note ! :  pluto.cf is the configuration file for the pluto daemon and is written as JSON.
Example :
```
{
  'DIR' : '/path/to/monitored/DIR',
  'pdf' : '/path/to/DIR/for/pdf',
  .
  .
  .
  'jpg' : '/path/to/DIR/for/jpg'
}
```


## customizing pluto

##
