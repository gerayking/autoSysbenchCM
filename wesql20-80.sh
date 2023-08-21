kubectl create -f - <<EOF                                                                                                     
apiVersion: v1
kind: Pod
metadata:
  namespace: default
  generateName: test-vtgate-run-
spec:
  containers:
    - name: test-sysbench
      image: registry.cn-hangzhou.aliyuncs.com/apecloud/customsuites:latest
      env:
        - name: TYPE
          value: "2"
        - name: FLAG
          value: "0"
        - name: CONFIGS
          value: "mode:run,driver:mysql,host:172.16.251.240,user:root,port:15306,db:mydb,size:2000000,tables:50,times:200,type:oltp_read_write_pct,threads:4,others:--read-percent=20 --write-percent=80 --skip_trx=on --mysql-ignore-errors=1062 --db-ps-mode=disable"
  restartPolicy: Never
  tolerations:
    - key: kb-sysbench
      operator: Equal
      value: "true"
      effect: NoSchedule
EOF