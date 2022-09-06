for k in `seq -w 10 -1 1`; do #k is number of pod
        ssh (master of K8s clsuter with wordpress yaml) "python3 /(path)/change.py ${k}" #change number of wordpress pod
        ssh (master of K8s clsuter with wordpress yaml) 'kubectl apply -f /(path of wordpress yaml)' #apply yaml
        for n in `seq 1 5`; do #n is times of test
                kubectl apply -f /(path)/master-pod.yaml -f /(path)/worker-deployment.yaml #execute locust
                sleep 2520s #locust executeing time
                ssh  (locust nfs server ip address) "rename \"s/01/$k$n/;\" /mnt/locust/test/01*" #locust csv rename　
                kubectl delete -f /(path)/master-pod.yaml -f /(path)/worker-deployment.yaml #delete locust pod
                sleep 60s
        done
        ssh (ip address of nfs server) "mv /mnt/locust/test/* ~/data11/" #move csv of locust data
done
