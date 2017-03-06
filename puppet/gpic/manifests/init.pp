class gpic {
 
  include ::gpic::collectd
  include ::gpic::influxdb
  include ::gpic::grafana
  include ::gpic::python
  include ::gpic::go

  # Hack around some dep issues
  Package['collectd'] -> Service['influxdb']

}
