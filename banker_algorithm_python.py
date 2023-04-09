import threading
import random

processes = int(input("Enter the number of processes: "))
resources = int(input("Enter the number of resources: "))
max_resources = [int(i) for i in input("Enter the maximum resources: ").split()]
allocated = []
max_demand = [] 
need = []  
available = max_resources[:] 
lock = threading.Lock() 


def calculate_need():
    global need
    need = [[0 for j in range(resources)] for i in range(processes)]
    for i in range(processes):
        for j in range(resources):
            need[i][j] = max_demand[i][j] - allocated[i][j]


def is_safe(process, request):
    global available, need
    
    for i in range(resources):
        if request[i] > need[process][i]:
            return False
    
    for i in range(resources):
        if request[i] > available[i]:
            return False
    
    temp_available = available[:]
    temp_need = need[:]
    for i in range(resources):
        temp_available[i] -= request[i]
        temp_need[process][i] -= request[i]
    
    work = temp_available[:]
    finish = [False for i in range(processes)]
    
    while True:
        found = False 
        for i in range(processes):
            if not finish[i]: 
                
                possible = True
                for j in range(resources):
                    if temp_need[i][j] > work[j]:
                        possible = False
                        break
                if possible:
                    
                    for j in range(resources):
                        work[j] += allocated[i][j]
                    finish[i] = True
                    found = True
        if not found:
            break
    
    for i in range(processes):
        if not finish[i]:
            return False 
    return True 


def allocate(process, request):
    global available, allocated, need
    
    for i in range(resources):
        available[i] -= request[i]
        allocated[process][i] += request[i]
        need[process][i] -= request[i]


def release(process, request):
    global available, allocated, need
    
    for i in range(resources):
        available[i] += request[i]
        allocated[process][i] -= request[i]
        need[process][i] += request[i]


def print_state():
    global max_resources, allocated, max_demand, need, available
    print("Maximum Resources: ", max_resources)
    print("Allocated Resources: ")
    for i in range(processes):
        print(allocated[i])
    print("Maximum Demand: ")
    for i in range(processes):
        print(max_demand[i])
    print("Remaining Need: ")
    for i in range(processes):
        print(need[i])
    print("Available Resources: ", available)

def run_process(process):
    global lock
    
    action = random.randint(0, 1)
    
    resource_vector = []
    if action == 0: 
        for i in range(resources):
            resource_vector.append(random.randint(0, need[process][i]))
    else: 
        for i in range(resources):
            resource_vector.append(random.randint(0, allocated[process][i]))
    
    print("Process", process, end=" ")
    if action == 0:
        print("requests", resource_vector)
    else:
        print("releases", resource_vector)
    
    lock.acquire()
    
    if action == 0: 
        if is_safe(process, resource_vector): 
            allocate(process, resource_vector) 
            print("Request granted.")
        else: 
            print("Request denied.")
    else: 
        release(process, resource_vector) 
        print("Resources released.")
    
    print_state()
    
    lock.release()


def main():
    global allocated, max_demand
    
    print("-- Allocated resources for each process --")
    for i in range(processes):
        allocated.append([int(i) for i in input().split()])
    print("-- Maximum demand for each process --")
    for i in range(processes):
        max_demand.append([int(i) for i in input().split()])
    
    calculate_need()
    
    threads = []
    for i in range(processes):
        threads.append(threading.Thread(target=run_process, args=(i,)))
        threads[i].start()
    
    for i in range(processes):
        threads[i].join()


if __name__ == "__main__":
    main()