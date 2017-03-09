class gpic {
 
  include ::gpic::collectd
  include ::gpic::influxdb
  include ::gpic::grafana
  include ::gpic::python

  # Hack around some dep issues
  Package['collectd'] -> Service['influxdb']

}
