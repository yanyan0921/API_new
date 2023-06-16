#!/bin/bash


host="cloud-platform.migu.cn"
duration="600"
jmxfile="GetLog.jmx"

for threadNumber in 5 10 20 30; do
  jtl_file="${jmxfile}_threadcnt_${threadNumber}_duration_${duration}.jtl"
  ~/apache-jmeter-5.5/bin/jmeter -n -t ${jmxfile} -Jhost="$host" -Jport=443 -JthreadNumber="$threadNumber" -Jduration="$duration" -l "$jtl_file"
  echo "Finished running ${jmxfile} with threadNumber=$threadNumber, results saved to $jtl_file"
done

tar czf ${jmxfile}_jtl_reuslts.tar.gz ${jmxfile}_*.jtl
echo "All jtl files have been place into tar file"

